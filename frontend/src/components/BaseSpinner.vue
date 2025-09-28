<template>
  <div class="spinner-container">
    <div
      class="w-16 h-16 border-blue-500 border-solid rounded-full animate-spin"
      style="border-top-color: transparent"
    ></div>
    <p class="mt-4 text-gray-600 dark:text-gray-300">로딩중...</p>
  </div>
</template>

<style scoped>
.spinner-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
