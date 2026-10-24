<template>
  <section class="mx-auto max-w-5xl px-6 py-16">
    <p class="text-sm text-zinc-400">Anime</p>

    <h1 class="mt-3 text-4xl font-bold">我看過的動漫</h1>

    <p class="mt-4 text-zinc-400">
      這裡整理我再巴哈姆特動畫瘋收藏的動畫
    </p>

    <!-- 卡片 -->
    <div class="mt-10 grid grid-cols-2 gap-5 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6">
      <a v-for="anime in pagedAnimeItems" :key="anime.title" :href="anime.url" target="_blank" rel="noopener noreferreer"
        class="group overflow-hidden rounded-lg border border-white/10 bg-white/5 transition hover:border-white/20 hover:bg-white/10">
        <!-- 卡片內容 aspect-[3/4] 固定圖片比例；object-cover 讓圖片填滿但不變形 -->
        <div class="aspect-[3/4] overflow-hidden bg-zinc-900">
          <img :src="anime.image" :alt="anime.title"
            class="h-full w-full object-cover transition group-hover:scale-105">

        </div>
        <!-- break-words 避免常標題超出卡片 -->
        <div class="p-3">
          <h2 class="break-words text-sm font-medium text-zinc-100">
            {{ anime.title }}
          </h2>
        </div>
      </a>
    </div>
    <div class="mt-10 flex justify-center gap-2">
      <button v-for="page in totalPages" :key="page" type="button"
        class="h-9 min-w-9 rounded border px-3 text-sm transition" :class="page === currentPage
            ? 'border-white bg-white text-zinc-950'
            : 'border-white/10 bg-white/5 text-zinc-300 hover:border-white/20 hover:bg-white/10 hover:text-white'
          " @click="currentPage = page">
        {{ page }}
      </button>
    </div>
  </section>
</template>

<script setup lang="ts">
import bahamutAnimeList from '../data/anime-bahamut.json'
import manualAnimeList from '../data/anime-manual.json'
import { computed, ref } from 'vue'
type Anime = {
  title: string
  image: string
  url: string
  sourceImage?: string
}

// 使用展開運算子 ...，把爬蟲資料和手動資料合併成同一個陣列。
const animeItems: Anime[] = [
  ...(bahamutAnimeList as Anime[]),
  ...(manualAnimeList as Anime[]),
]

const currentPage = ref(1)
const pageSize = 24

const totalPages = computed(() => {
  return Math.ceil(animeItems.length / pageSize)
})

const pagedAnimeItems = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  const end = start + pageSize
  return animeItems.slice(start, end)
})
</script>
