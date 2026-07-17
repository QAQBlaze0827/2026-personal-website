<script setup lang="ts">
import Header from './components/Header.vue'
</script>

<template>
  <main class="min-h-screen bg-zinc-950 text-zinc-100">
    <Header />

    <!-- 首頁主要內容：max-w-5xl 限制寬度，mx-auto 讓內容置中 -->
    <section class="mx-auto max-w-5xl px-6 py-16">
      <p class="text-sm text-zinc-400">Personal Website</p>

      <h1 class="mt-3 text-4xl font-bold">
        我的個人網站
      </h1>

      <p class="mt-4 max-w-xl text-zinc-400">
        這裡會慢慢整理我看過的動漫，以及我有聽過的歌。
      </p>

      <!-- grid 用來排列卡片；md:grid-cols-2 代表中等螢幕以上變成兩欄 -->
      <div class="mt-10 grid gap-4 md:grid-cols-2">
        <a
          href="#"
          class="rounded-lg border border-white/10 bg-white/5 p-6 transition hover:border-white/20 hover:bg-white/10"
        >
          <p class="text-sm text-zinc-400">Anime</p>
          <h2 class="mt-2 text-2xl font-semibold">我看過的動漫</h2>
          <p class="mt-3 text-zinc-400">
            之後可以放看過的作品、心得、評分或分類。
          </p>
        </a>

        <a
          href="#"
          class="rounded-lg border border-white/10 bg-white/5 p-6 transition hover:border-white/20 hover:bg-white/10"
        >
          <p class="text-sm text-zinc-400">Music</p>
          <h2 class="mt-2 text-2xl font-semibold">我有聽過的歌</h2>
          <p class="mt-3 text-zinc-400">
            之後可以整理歌名、歌手、喜歡的段落或播放連結。
          </p>
        </a>
      </div>
    </section>
  </main>
</template>