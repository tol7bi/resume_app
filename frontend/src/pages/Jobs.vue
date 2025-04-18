<template>
  <div class="jobs">
    <h2>Job Listings</h2>
    <div v-for="job in jobs" :key="job.id">
      <h3>{{ job.title }}</h3>
      <p>{{ job.description }}</p>
      <button @click="matchResumes(job.id)">Match Resumes</button>
      <div v-if="matches[job.id]">
        <h4>Matches:</h4>
        <ul>
          <li v-for="resume in matches[job.id]" :key="resume.id">{{ resume.filename }} (Score: {{ resume.score }})</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../api/axios'

const jobs = ref([])
const matches = ref({})

const fetchJobs = async () => {
  const res = await axios.get('/jobs/')
  jobs.value = res.data
}

const matchResumes = async (jobId) => {
  const res = await axios.get(`/jobs/match/${jobId}/`)
  matches.value[jobId] = res.data
}

onMounted(() => {
  fetchJobs()
})
</script>