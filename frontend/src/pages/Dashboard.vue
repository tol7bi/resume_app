<template>
  <div class="dashboard">
    <h2>Your Resumes</h2>
    <div v-for="resume in resumes" :key="resume.id">
      <h3>{{ resume.filename }}</h3>
      <p>Score: {{ resume.score }}</p>
      <p>Skills: {{ resume.skills.join(', ') }}</p>
      <p>Feedback: {{ resume.feedback }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../api/axios'

const resumes = ref([])

const fetchResumes = async () => {
  const res = await axios.get('/resumes/my/')
  resumes.value = res.data
}

onMounted(() => {
  fetchResumes()
})
</script>