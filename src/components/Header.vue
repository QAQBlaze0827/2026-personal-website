<template>
  <!-- 頁面最上方導覽列，border-b 是底線，border-white/10 是低透明度白色 -->
  <nav class="border-b border-white/10">
    <!-- mx-auto + max-w-5xl 讓內容置中並限制寬度；flex 用來左右排列網站名稱與選單 -->
    <div class="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
      <a href="/" class="text-lg font-semibold">
        My Website
      </a>

      <!-- gap-4 控制連結間距，text-zinc-300 是偏淡的文字色，hover:text-white 是滑過變白 -->
      <div class="flex gap-4 text-sm text-zinc-300">
        <a href="#" class="hover:text-white">我看過的動漫</a>
        <a href="#" class="hover:text-white">我有聽過的歌</a>
      </div>
    </div>
  </nav>
</template>