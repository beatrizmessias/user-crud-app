import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

import PrimeVue from 'primevue/config'
import 'primevue/resources/themes/lara-light-blue/theme.css'
import 'primevue/resources/primevue.min.css'
import 'primeicons/primeicons.css'
import 'primeflex/primeflex.css'


import Button from 'primevue/button'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Dropdown from 'primevue/dropdown'
import MultiSelect from 'primevue/multiselect'
import Checkbox from 'primevue/checkbox'
import Toast from 'primevue/toast'
import ToastService from 'primevue/toastservice'
import Tooltip from 'primevue/tooltip'
import ConfirmDialog from 'primevue/confirmdialog'
import ConfirmationService from 'primevue/confirmationservice'


import UsersList from './components/UsersList.vue'
import UserDetail from './components/UserDetail.vue'


const routes = [
  {
    path: '/',
    name: 'Users List',
    component: UsersList
  },
  {
    path: '/user/:username',
    name: 'UserDetail',
    component: UserDetail,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)

app.use(router)
app.use(PrimeVue)
app.use(ToastService)
app.use(ConfirmationService)

app.component('Button', Button)
app.component('DataTable', DataTable)
app.component('Column', Column)
app.component('Dialog', Dialog)
app.component('InputText', InputText)
app.component('Dropdown', Dropdown)
app.component('MultiSelect', MultiSelect)
app.component('Checkbox', Checkbox)
app.component('Toast', Toast)
app.component('ConfirmDialog', ConfirmDialog)

app.directive('tooltip', Tooltip)

app.mount('#app')