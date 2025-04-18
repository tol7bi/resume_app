<template>
  <div class="register">
    <h2>Register</h2>
    <input v-model="form.email" placeholder="Email" />
    <input v-model="form.username" placeholder="Username" />
    <input v-model="form.password" type="password" placeholder="Password" />
    <button @click="register">Register</button>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()

const form = reactive({
  email: '',
  username: '',
  password: ''
})

const register = async () => {
  try {
    await auth.register(form)
  } catch (err) {
    alert('Registration failed')
  }
}
</script>
