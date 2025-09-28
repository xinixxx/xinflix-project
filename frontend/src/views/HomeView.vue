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

  <div v-else class="container mx-auto my-12 px-4 pb-12">
    <div
      class="bg-white dark:bg-dark-card rounded-lg shadow-lg p-8 mb-12 text-center"
    >
      <h1 class="text-4xl font-bold text-gray-800 dark:text-gray-100 mb-2">
        XINFLIX
      </h1>
      <p class="text-gray-600 dark:text-gray-400">
        최신 동영상과 게시글을 확인해보세요.
      </p>
    </div>

    <div class="mb-12">
      <h2 class="text-3xl font-bold text-gray-800 dark:text-gray-100 mb-6">
        주간 인기 영상 🔥
      </h2>
      <div
        v-if="weeklyPopularVideos.length > 0"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        <VideoCard
          v-for="video in weeklyPopularVideos"
          :key="video.id"
          :video="video"
        />
      </div>
      <div
        v-else
        class="text-center text-gray-500 dark:text-gray-400 py-10 bg-gray-50 dark:bg-dark-card rounded-lg"
      >
        <p>아직 주간 인기 영상이 없습니다.</p>
      </div>
    </div>

    <div class="mb-12">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-3xl font-bold text-gray-800 dark:text-gray-100">
          최신 동영상
        </h2>
        <router-link
          to="/videos"
          class="text-primary hover:underline dark:text-blue-400"
          >더보기 &rarr;</router-link
        >
      </div>
      <div
        v-if="latestVideos.length > 0"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        <VideoCard
          v-for="video in latestVideos"
          :key="video.id"
          :video="video"
        />
      </div>
      <div
        v-else
        class="text-center text-gray-500 dark:text-gray-400 py-10 bg-gray-50 dark:bg-dark-card rounded-lg"
      >
        <p>아직 업로드된 동영상이 없습니다.</p>
      </div>
    </div>

    <div>
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-3xl font-bold text-gray-800 dark:text-gray-100">
          최신 게시글
        </h2>
        <router-link
          to="/board"
          class="text-primary hover:underline dark:text-blue-400"
          >더보기 &rarr;</router-link
        >
      </div>
      <div v-if="latestPosts.length > 0" class="space-y-4">
        <div
          v-for="post in latestPosts"
          :key="post.id"
          class="bg-white dark:bg-dark-card rounded-lg shadow-sm p-4 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200 cursor-pointer"
        >
          <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200">
            {{ post.title }}
          </h3>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            작성자: {{ post.author_username }}
          </p>
        </div>
      </div>
      <div
        v-else
        class="text-center text-gray-500 dark:text-gray-400 py-10 bg-gray-50 dark:bg-dark-card rounded-lg"
      >
        <p>아직 작성된 게시글이 없습니다.</p>
      </div>
    </div>
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
