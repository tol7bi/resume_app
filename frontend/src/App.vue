<template>
  <div id="app">
    <Navbar v-if="auth.token" />
    <router-view />
  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue'
import { useAuthStore } from './stores/auth'
const auth = useAuthStore()
</script>
