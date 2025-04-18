<template>
  <div class="login">
    <h2>Login</h2>
    <input v-model="form.email" placeholder="Email" />
    <input v-model="form.password" type="password" placeholder="Password" />
    <button @click="login">Login</button>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()

const form = reactive({
  email: '',
  password: ''
})

const login = async () => {
  try {
    await auth.login(form)
  } catch (err) {
    alert('Login failed')
  }
}
</script>