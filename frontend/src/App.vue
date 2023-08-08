<script setup>
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue';

</script>

<template>
  <Navbar v-if="!['signin'].includes($route.name)" />
  <RouterView />
</template>

<style scoped></style>
