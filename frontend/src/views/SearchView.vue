<script setup>
import TheatreForm from '../components/TheatreForm.vue';
import { useToast } from 'vue-toastification';
const toast  = useToast();

function showToast() {
  toast.success('Hello, this is a toast message!');
}
</script>

<template>
  <button @click="showToast">Show Toast</button>
  <TheatreForm/>
</template>

<style scoped>

</style>