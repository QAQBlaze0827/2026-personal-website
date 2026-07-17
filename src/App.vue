<template>
  <main class="min-h-screen bg-zinc-950 text-zinc-100">
    <Header />
    <section class="mx-auto max-w-5xl px-6 py-16">
      <p class="text-sm text-zinc-400">Personal Website</p>
      <h1 class="mt-3 text-4xl font-bold">Welcome to My Website</h1>
      <p class="mt-4 max-w-xl text-zinc-400">
        這裡應該會放我看過的動漫，如果有空的話會在放歌
      </p>
    </section>
  </main>
</template>

<script setup lang="ts">
import Header from './components/Header.vue'
</script>