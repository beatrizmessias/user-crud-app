<template>
    <div id="app">
        <nav class="navbar">
            <h1>User Management System</h1>
        </nav>

        <main class="main-content">
            <router-view />
        </main>

        <Toast />
        <ConfirmDialog />
    </div>
</template>

<script>
export default {
    name: 'App',

}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f8f9fa;
}

.navbar {
  background-color: #2c3e50;
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.navbar h1 {
  font-size: 1.5rem;
  font-weight: 600;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-link:hover {
  background-color: rgba(255,255,255,0.1);
}

.main-content {
  padding: 2rem;
  min-height: calc(100vh - 80px);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-header h2 {
  color: #2c3e50;
  font-size: 1.8rem;
}

.roles-badges {
  display: flex;
  gap: 0.25rem;
  flex-wrap: wrap;
}

.role-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
}

.role-admin {
  background-color: #e74c3c;
  color: white;
}

.role-manager {
  background-color: #f39c12;
  color: white;
}

.role-tester {
  background-color: #27ae60;
  color: white;
}

.status-active {
  color: #27ae60;
  font-weight: 500;
}

.status-inactive {
  color: #e74c3c;
  font-weight: 500;
}

.username-link {
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
}

.username-link:hover {
  text-decoration: underline;
}

.user-detail-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  max-width: 600px;
  margin: 0 auto;
}

.user-detail-field {
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.user-detail-field:last-child {
  border-bottom: none;
}

.user-detail-field label {
  font-weight: 600;
  color: #555;
  display: block;
  margin-bottom: 0.5rem;
}

.user-detail-field .value {
  color: #333;
  font-size: 1.1rem;
}

.user-actions {
  margin-top: 2rem;
  display: flex;
  gap: 1rem;
}

.form-field {
  margin-bottom: 1rem;
}

.form-field label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.p-button {
  margin-right: 0.5rem;
}

.p-datatable {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.p-dialog {
  min-width: 400px;
}

.p-button {
  background-color: #3498db;
  color: white;
  border-radius: 8px;
  padding: 0.6rem 1.2rem;
  font-weight: 600;
  box-shadow: 0 4px 8px rgba(52, 152, 219, 0.3);
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  border: none;
  cursor: pointer;
  user-select: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.p-button:hover {
  background-color: #2980b9;
  box-shadow: 0 6px 12px rgba(41, 128, 185, 0.5);
}

.p-button:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.6);
}

.p-button:active {
  background-color: #1c5980;
  box-shadow: 0 2px 4px rgba(28, 89, 128, 0.7);
}

.p-button.p-button-success {
  background-color: #27ae60;
  box-shadow: 0 4px 8px rgba(39, 174, 96, 0.3);
}

.p-button.p-button-success:hover {
  background-color: #1e8449;
  box-shadow: 0 6px 12px rgba(30, 132, 73, 0.5);
}

.p-button.p-button-warning {
  background-color: #f39c12;
  box-shadow: 0 4px 8px rgba(243, 156, 18, 0.3);
}

.p-button.p-button-warning:hover {
  background-color: #d68910;
  box-shadow: 0 6px 12px rgba(214, 137, 16, 0.5);
}

.p-button.p-button-danger {
  background-color: #e74c3c;
  box-shadow: 0 4px 8px rgba(231, 76, 60, 0.3);
}

.p-button.p-button-danger:hover {
  background-color: #c0392b;
  box-shadow: 0 6px 12px rgba(192, 57, 43, 0.5);
}


</style>