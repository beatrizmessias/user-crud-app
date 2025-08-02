<template>
  <div>
    <div class="page-header">
      <h2>Users Management</h2>
      <Button 
        label="Create User"
        icon="pi pi-plus"
        class="p-button-success"
        @click="showCreateDialog"
      />
    </div>

    <DataTable 
      :value="users" 
      :loading="loading"
      dataKey="_id"
      :paginator="true"
      :rows="10"
      :rowsPerPageOptions="[5, 10, 20]"
      class="p-datatable-users"
    >
      <Column field="username" header="Username" sortable>
        <template #body="slotProps">
          <router-link 
            :to="`/user/${slotProps.data.username}`"
            class="username-link"
          >
            {{ slotProps.data.username }}
          </router-link>
        </template>
      </Column>

      <Column field="roles" header="Roles">
        <template #body="slotProps">
          <div class="roles-badges">
            <span
              v-for="role in slotProps.data.roles"
              :key="role"
              :class="`role-badge role-${role}`"
            >
              {{ role }}
            </span>
            <span 
              v-if="slotProps.data.roles.length === 0"
              class="no-roles"
            >
              No roles
            </span>
          </div>
        </template>
      </Column>

      <Column field="preferences.timezone" header="Timezone" sortable>
        <template #body="slotProps">
          {{ slotProps.data.preferences?.timezone || 'N/A' }}
        </template>
      </Column>

      <Column field="active" header="Is Active?" sortable>
        <template #body="slotProps">
          <span
            :class="slotProps.data.active ? 'status-active' : 'status-inactive'"
          >
            {{ slotProps.data.active ? 'Active' : 'Inactive' }}
          </span>
        </template>
      </Column>

      <Column field="updated_ts" header="Last Updated At" sortable>
        <template #body="slotProps">
          {{ formatDate(slotProps.data.updated_ts, slotProps.data.created_ts) }}
        </template>
      </Column>

      <Column field="created_ts" header="Created At" sortable>
        <template #body="slotProps">
          {{ formatDate(slotProps.data.created_ts) }}
        </template>
      </Column>

      <Column header="Actions" :exportable="false">
        <template #body="slotProps">
          <Button 
            icon="pi pi-pencil"
            class="p-button-rounded p-button-warning p-button-text"
            @click="editUser(slotProps.data)"
            v-tooltip.top="'Edit'"
          />
          <Button 
            icon="pi pi-trash"
            class="p-button-rounded p-button-danger p-button-text"
            @click="confirmDelete(slotProps.data)"
            v-tooltip.top="'Delete'"
          />
        </template>
      </Column>
    </DataTable>

    <UserForm 
      v-model:visible="dialogVisible"
      :user="selectedUser"
      :is-edit="isEdit"
      @user-saved="handleUserSaved"
    />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import axios from 'axios'
import UserForm from './UserForm.vue'

export default {
  name: 'UsersList',
  components: {
    UserForm
  },
  setup() {
    const users = ref([])
    const loading = ref(false)
    const dialogVisible = ref(false)
    const selectedUser = ref(null)
    const isEdit = ref(false)

    const toast = useToast()
    const confirm = useConfirm()

    const loadUsers = async () => {
      loading.value = true
      try {
        const response = await axios.get('http://localhost:5000/users')
        users.value = response.data
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to load users.'
        })
      } finally {
        loading.value = false
      }
    }

    const showCreateDialog = () => {
      selectedUser.value = null
      isEdit.value = false
      dialogVisible.value = true
    }

    const editUser = (user) => {
      selectedUser.value = { ...user }
      isEdit.value = true
      dialogVisible.value = true
    }

    const confirmDelete = (user) => {
      confirm.require({
        message: `Are you sure you want to delete the user "${user.username}"?`,
        header: 'Confirm Deletion',
        icon: 'pi pi-exclamation-triangle',
        accept: () => deleteUser(user)
      })
    }

    const deleteUser = async (user) => {
      try {
        await axios.delete(`http://localhost:5000/users/${user._id}`)
        toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'User deleted successfully.'
        })
        loadUsers()
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to delete user.'
        })
      }
    }

    const handleUserSaved = () => {
      dialogVisible.value = false
      loadUsers()
    }

    const formatDate = (timestamp, createdAt) => {
      if (!timestamp) {
        if (createdAt) {
          const createdDate = new Date(createdAt)
          if (!isNaN(createdDate)) {
            return createdDate.toLocaleDateString()
          }
        }
        return 'Invalid Date'
      }

      const date = new Date(timestamp)
      if (isNaN(date)) return 'Invalid Date'
      return date.toLocaleDateString()
    }

    onMounted(() => {
      loadUsers()
    })

    return {
      users,
      loading,
      dialogVisible,
      selectedUser,
      isEdit,
      showCreateDialog,
      editUser,
      confirmDelete,
      handleUserSaved,
      formatDate
    }
  }
}
</script>

<style scoped>
.p-datatable-users {
  margin-top: 1rem;
}

.no-roles {
  color: #6c757d;
  font-style: italic;
  font-size: 0.875rem;
}
</style>