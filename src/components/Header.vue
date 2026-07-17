<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <nav class="border-b border-white/10">
    <div class="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
      <RouterLink to="/" class="text-lg font-semibold">
        My Website
      </RouterLink>

      <div class="flex gap-4 text-sm text-zinc-300">
        <RouterLink to="/anime" class="hover:text-white">
          我看過的動漫
        </RouterLink>

        <RouterLink to="/music" class="hover:text-white">
          我有聽過的歌
        </RouterLink>
      </div>
    </div>
  </nav>
</template>