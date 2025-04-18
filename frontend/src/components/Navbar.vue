<template>
  <nav style="margin-bottom: 2rem;">
    <router-link to="/dashboard">Dashboard</router-link> |
    <router-link to="/upload">Upload</router-link> |
    <router-link to="/jobs">Jobs</router-link> |
    <button @click="logout" style="margin-left: 1rem;">Logout</button>
  </nav>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
const auth = useAuthStore()

const logout = () => auth.logout()
</script>
