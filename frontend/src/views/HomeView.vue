<template>
  <div
    v-if="isLoading"
    class="flex justify-center items-center"
    style="height: 80vh"
  >
    <Spinner />
  </div>

  <div v-else-if="error" class="text-center py-20">
    <p class="text-red-500">{{ error }}</p>
  </div>

  <div v-else class="container mx-auto my-12 space-y-16 px-4 pb-12">
    <div
      class="bg-white dark:bg-dark-card rounded-lg shadow-lg p-8 text-center"
    >
      <h1
        class="text-4xl font-display text-gray-800 dark:text-gray-100 mb-2 tracking-wider"
      >
        XINFLIX
      </h1>
      <p class="text-gray-600 dark:text-gray-400">
        최신 동영상과 게시글을 확인해보세요.
      </p>
    </div>

    <div class="space-y-4">
      <h2 class="text-3xl font-bold text-gray-800 dark:text-gray-100">
        주간 인기 영상 🔥
      </h2>
      <div
        v-if="weeklyPopularVideos.length > 0"
        class="flex overflow-x-auto space-x-6 pb-4"
      >
        <VideoCard
          v-for="video in weeklyPopularVideos"
          :key="video.id"
          :video="video"
          class="w-72 flex-shrink-0"
        />
      </div>
      <div v-else class="text-center text-gray-500 ...">
        <p>아직 주간 인기 영상이 없습니다.</p>
      </div>
    </div>

    <div class="space-y-4">
      <div class="flex justify-between items-center">
        <h2 class="text-3xl font-bold text-gray-800 dark:text-gray-100">
          최신 동영상
        </h2>
        <router-link to="/videos" class="text-primary hover:underline ..."
          >더보기 &rarr;</router-link
        >
      </div>
      <div
        v-if="latestVideos.length > 0"
        class="flex overflow-x-auto space-x-6 pb-4"
      >
        <VideoCard
          v-for="video in latestVideos"
          :key="video.id"
          :video="video"
          class="w-72 flex-shrink-0"
        />
      </div>
      <div v-else class="text-center text-gray-500 ...">
        <p>아직 업로드된 동영상이 없습니다.</p>
      </div>
    </div>

    <div></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "@/api";
import VideoCard from "@/components/VideoCard.vue"; // 👈 컴포넌트 import
import Spinner from "@/components/BaseSpinner.vue";

const isLoading = ref(true);
const error = ref(null);

const latestVideos = ref([]);
const latestPosts = ref([]);
const weeklyPopularVideos = ref([]);

onMounted(async () => {
  try {
    const [videosResponse, postsResponse, popularResponse] = await Promise.all([
      api.getVideos(),
      api.getPosts(),
      api.getWeeklyPopularVideos(),
    ]);
    latestVideos.value = videosResponse.data
      .sort((a, b) => b.id - a.id)
      .slice(0, 4);
    latestPosts.value = postsResponse.data
      .sort((a, b) => b.id - a.id)
      .slice(0, 5);
    weeklyPopularVideos.value = popularResponse.data;
  } catch (error) {
    error.value =
      "데이터를 불러오는데 실패했습니다. 잠시ㅣ 후 다시 시도해주세요.";
    console.error("메인 페이지 데이터 로딩 실패:", error);
  } finally {
    isLoading.value = false;
  }
});
</script>
