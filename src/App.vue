<script setup lang="ts">
import { RouterView } from 'vue-router'
import Header from './components/Header.vue'
</script>

<template>
  <main class="min-h-screen bg-zinc-950 text-zinc-100">
    <Header />
    <RouterView />
  </main>
</template>