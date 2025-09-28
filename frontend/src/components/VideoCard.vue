<template>
  <div
    class="bg-white dark:bg-dark-card rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 hover:shadow-xl transition-all duration-300"
  >
    <router-link :to="{ name: 'video-detail', params: { id: video.id } }">
      <img
        :src="video.thumbnail"
        :alt="video.title"
        class="w-full h-48 object-cover"
      />
    </router-link>
    <div class="p-4">
      <h3
        class="text-lg font-semibold text-gray-900 dark:text-gray-200 truncate"
        :title="video.title"
      >
        {{ video.title }}
      </h3>
      <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
        {{ video.uploader_username }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from "vue";

defineProps({
  video: {
    type: Object,
    required: true,
  },
});
</script>
