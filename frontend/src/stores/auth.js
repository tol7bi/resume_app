import { defineStore } from 'pinia'
import axios from '../api/axios'
import router from '../router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
  }),
  actions: {
    async login(form) {
      const res = await axios.post('/auth/login/', form)
      this.token = res.data.access
      localStorage.setItem('token', this.token)
      await this.fetchUser()
      router.push('/dashboard')
    },
    async register(form) {
      const res = await axios.post('/auth/register/', form)
      this.token = res.data.access
      localStorage.setItem('token', this.token)
      await this.fetchUser()
      router.push('/dashboard')
    },
    async fetchUser() {
      const res = await axios.get('/auth/me/')
      this.user = res.data
    },
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      router.push('/login')
    }
  }
})
