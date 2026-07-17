<template>
  <main class="min-h-screen bg-zinc-950 text-zinc-100">
    <nav class="border-b border-white/10">
      <!-- nav的框 -->
      <div class="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
        <a href="/" class="text-lg font-semibold">My Website</a>
      <!-- nav的內容 --> 
        <div class="flex gap-4 text-sm text-zinc-300">
          <a href="#" class="hover:text-white">我看過的動漫</a>
          <a href="#contact" class="hover:text-white">我聽過的歌</a>
        </div>
      </div>
    </nav>

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

</script>