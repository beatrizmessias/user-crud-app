<template>
  <div>
    <div class="page-header">
      <Button 
        label="Return"
        icon="pi pi-arrow-left"
        class="p-button-secondary"
        @click="$router.push('/')"
      />
      <h2>User Details</h2>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="loading-spinner">Loading...</div>
    </div>

    <div v-else-if="user" class="user-detail-card">
      <div class="user-header">
        <h3 v-text="user.username"></h3>
        <div class="user-status">
          <span
            :class="user.active ? 'status-active' : 'status-inactive'"
            v-text="user.active ? 'Active' : 'Inactive'"
          >
          </span>
        </div>
      </div>

      <div class="user-detail-field">
        <label>Username:</label>
        <div class="value" v-text="user.username"></div>
      </div>

      <div class="user-detail-field">
        <label>Roles:</label>
        <div class="value">
          <div class="roles-badges">
            <span
              v-for="role in user.roles"
              :key="role"
              :class="`role-badge role-${role}`"
              v-text="role"
            >
            </span>
            <span 
              v-if="user.roles.length === 0"
              class="no-roles"
            >
              No roles assigned.
            </span>
          </div>
        </div>
      </div>

      <div class="user-detail-field">
        <label>Timezone:</label>
        <div class="value" v-text="user.preferences.timezone"></div>
      </div>

      <div class="user-detail-field">
        <label>Is Active?</label>
        <div class="value">
          <span
            :class="user.active ? 'status-active' : 'status-inactive'"
            v-text="user.active ? 'Active' : 'Inactive'"
          >
          </span>
        </div>
      </div>

      <div class="user-detail-field">
        <label>Created At:</label>
        <div
          class="value"
          v-text="formatDate(user.created_ts)"
        >
        </div>
      </div>

      <div class="user-detail-field">
        <label>Last Updated At:</label>
        <div
          class="value"
          v-text="formatDate(user.updated_ts, user.created_ts)"
        >
        </div>
      </div>

      <div class="user-actions">
        <Button 
          label="Edit"
          icon="pi pi-pencil"
          class="p-button-warning"
          @click="editUser"
        />
        <Button 
          label="Delete"
          icon="pi pi-trash"
          class="p-button-danger"
          @click="confirmDelete"
        />
      </div>
    </div>

    <div v-else class="error-container">
      <h3>User not found.</h3>
      <p>The requested user could not be found.</p>
    </div>

    <UserForm 
      v-model:visible="dialogVisible"
      :user="user"
      :is-edit="true"
      @user-saved="handleUserSaved"
    />

  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import axios from 'axios'
import UserForm from '../components/UserForm.vue'

export default {
  name: 'UserDetail',
  components: {
    UserForm
  },
  props: {
    username: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const user = ref(null)
    const loading = ref(false)
    const dialogVisible = ref(false)

    const route = useRoute()
    const router = useRouter()
    const toast = useToast()
    const confirm = useConfirm()

    const loadUser = async () => {
      loading.value = true
      try {
        const response = await axios.get(`http://localhost:5000/users/username/${props.username}`)
        user.value = response.data
      } catch (error) {
        if (error.response?.status === 404) {
          toast.add({
            severity: 'warn',
            summary: 'User not found',
            detail: `User "${props.username}" was not found.`
          })
        } else {
          toast.add({
            severity: 'error',
            summary: 'Error',
            detail: `Failed to load user.`
          })
        }
      } finally {
        loading.value = false
      }
    }

    const editUser = () => {
      dialogVisible.value = true
    }

    const confirmDelete = () => {
      confirm.require({
        message: `Are you sure you want to delete user "${user.value.username}"?`,
        header: 'Confirm Deletion',
        icon: 'pi pi-exclamation-triangle',
        accept: deleteUser
      })
    }

    const deleteUser = async () => {
      try {
        await axios.delete(`http://localhost:5000/users/${user.value._id}`)
        toast.add({
          severity: 'success',
          summary: 'Success',
          detail: `User deleted successfully.`
        })
        router.push('/')
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
      loadUser()
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
      loadUser()
    })

    return {
      user,
      loading,
      dialogVisible,
      editUser,
      confirmDelete,
      handleUserSaved,
      formatDate
    }
  }
}
</script>

<style scoped>
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.loading-spinner {
  font-size: 1.2rem;
  color: #666;
}

.error-container {
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.error-container h3 {
  color: #e74c3c;
  margin-bottom: 1rem;
}

.user-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #eee;
}

.user-header h3 {
  color: #2c3e50;
  font-size: 2rem;
  margin: 0;
}

.user-status {
  font-size: 1.1rem;
}

.no-roles {
  color: #666;
  font-style: italic;
}
</style>