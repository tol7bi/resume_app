<template>
  <div class="upload">
    <h2>Upload Resume</h2>
    <input type="file" @change="handleFile" />
    <button @click="uploadResume">Upload</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from '../api/axios'

const file = ref(null)

const handleFile = (e) => {
  file.value = e.target.files[0]
}

const uploadResume = async () => {
  const formData = new FormData()
  formData.append('file', file.value)
  try {
    await axios.post('/resumes/upload/', formData)
    alert('Resume uploaded successfully')
  } catch (err) {
    alert('Upload failed')
  }
}
</script>
