<template>
    <Dialog
        :visible="visible"
        :modal="true"
        :header="isEdit ? 'Edit User' : 'Create User'"
        :style="{ width: '450px' }"
        @update:visible="$emit('update:visible', $event)"
    >
        <form @submit.prevent="handleSubmit">
            <div class="form-field">
                <label for="username">Username:</label>
                <InputText
                    id="username"
                    v-model="formData.username"
                    :class="{ 'p-invalid': errors.username }"
                    required
                />
                <small class="p-error" v-text="errors.username"></small>
            </div>

            <div class="form-field">
                <label for="password">Password:</label>
                <InputText
                    id="password"
                    type="password"
                    v-model="formData.password"
                    :class="{ 'p-invalid': errors.password }"
                    :required="!isEdit"
                />
                <small class="p-error" v-text="errors.password"></small>
                <small v-if="isEdit" class="p-help">Leave blank to keep current password.</small>
            </div>

            <div class="form-field">
                <label>Roles:</label>
                <div class="roles-selection">
                    <div class="p-field-checkbox">
                        <Checkbox
                            id="role-admin"
                            v-model="formData.roles"
                            value="admin" 
                        />
                        <label for="role-admin">Admin</label>
                    </div>
                    <div class="p-field-checkbox">
                        <Checkbox
                            id="role-manager"
                            v-model="formData.roles"
                            value="manager" 
                        />
                        <label for="role-manager">Manager</label>
                    </div>
                    <div class="p-field-checkbox">
                        <Checkbox
                            id="role-tester"
                            v-model="formData.roles"
                            value="tester" 
                        />
                        <label for="role-tester">Tester</label>
                    </div>
                </div>
            </div>

            <div class="form-field">
                <label for="timezone">Timezone:</label>
                <InputText
                    id="timezone"
                    v-model="formData.timezone"
                    placeholder="e.g: America/Sao_Paulo"
                    :class="{ 'p-invalid': errors.timezone }"
                    required
                />
                <small class="p-error" v-text="errors.timezone"></small>
            </div>

            <div class="form-field">
                <div class="p-field-checkbox">
                    <Checkbox 
                        id="active" 
                        v-model="formData.active" 
                        :binary="true" 
                    />
                    <label for="active">Active User</label>
                </div>
            </div>
        
            <div class="form-actions">
                <Button 
                    type="submit"
                    label="Save"
                    :loading="loading"
                    class="p-button-success"
                />
                <Button 
                    type="button"
                    label="Cancel"
                    class="p-button-secondary"
                    @click="$emit('update:visible', false)"
                />
            </div>
        </form>
    </Dialog>
</template>

<script>
import { ref, watch, reactive } from 'vue'
import { useToast } from 'primevue/usetoast'
import axios from 'axios'

export default {
    name: 'UserForm',
    props: {
        visible: Boolean,
        user: Object,
        isEdit: Boolean
    },
    emits: ['update:visible', 'user-saved'],
    setup(props, { emit }) {
        const toast = useToast()
        const loading = ref(false)

        const formData = reactive({
            username: '',
            password: '',
            roles: [],
            timezone: '',
            active: true
        })

        const errors = reactive({
            username: '',
            password: '',
            timezone: ''
        })

        const resetForm = () => {
            formData.username = ''
            formData.password = ''
            formData.roles = []
            formData.timezone = ''
            formData.active = true

            Object.keys(errors).forEach(key => {
                errors[key] = ''
            })
        }

        const fillForm = (user) => {
            if (user) {
                formData.username = user.username || ''
                formData.password = '' // Don't pre-fill password for security
                formData.roles = user.roles ? [...user.roles] : []
                formData.timezone = user.preferences?.timezone || ''
                formData.active = user.active !== undefined ? user.active : true
            }
        }

        const validateForm = () => {
            let isValid = true

            Object.keys(errors).forEach(key => {
                errors[key] = ''
            })

            if (!formData.username.trim()) {
                errors.username = 'Username is required'
                isValid = false
            }

            if (!props.isEdit && !formData.password.trim()) {
                errors.password = 'Password is required'
                isValid = false
            }

            if (!formData.timezone.trim()) {
                errors.timezone = 'Timezone is required'
                isValid = false
            }

            return isValid
        }

        const handleSubmit = async () => {
            if (!validateForm()) {
                return
            }

            loading.value = true

            try {
                const userData = {
                    username: formData.username,
                    roles: formData.roles,
                    timezone: formData.timezone,
                    active: formData.active
                }

                // Only include password if it's provided
                if (formData.password.trim()) {
                    userData.password = formData.password
                }

                if (props.isEdit) {
                    await axios.put(`http://localhost:5000/users/${props.user._id}`, userData)
                    toast.add({
                        severity: 'success',
                        summary: 'Success',
                        detail: 'User updated successfully.'
                    })
                } else {
                    await axios.post('http://localhost:5000/users', userData)
                    toast.add({
                        severity: 'success',
                        summary: 'Success',
                        detail: 'User created successfully.'
                    })
                }

                emit('user-saved')
                emit('update:visible', false)
            } catch (error) {
                toast.add({
                    severity: 'error',
                    summary: 'Error',
                    detail: error.response?.data?.error || 'Save failed.'
                })
            } finally {
                loading.value = false
            }
        }

        watch(() => props.visible, (newVal) => {
            if (newVal) {
                if (props.isEdit && props.user) {
                    fillForm(props.user)
                } else {
                    resetForm()
                }
            }
        })

        return {
            formData,
            errors,
            loading,
            handleSubmit
        }
    }
}
</script>

<style scoped>
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 1.5rem;
}

.roles-selection {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.p-field-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.p-help {
  color: #6c757d;
  font-size: 0.875rem;
}

form {
  background-color: #fefefe;
  padding: 1.5rem;
  border-radius: 8px;
}
</style>