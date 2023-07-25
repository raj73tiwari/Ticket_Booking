<script setup>
import { onMounted } from 'vue';
import axios from 'axios';
onMounted( async()=>{
  const response=await axios.get('/check')
  console.log(response)
})
</script>

<template>

  <h1>Profile</h1>
</template>

<style scoped>

</style>