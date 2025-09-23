<template>
  <div class="container mx-auto my-12 px-4 pb-12">
    <div
      class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 mb-12 text-center"
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
        <div
          v-for="video in weeklyPopularVideos"
          :key="video.id"
          class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 hover:shadow-xl transition-all duration-300"
        >
          <router-link :to="{ name: 'video-detail', params: { id: video.id } }">
            <img
              :src="video.thumbnail"
              :alt="video.title"
              class="w-full h-40 object-cover"
            />
          </router-link>
          <div class="p-4">
            <h3
              class="text-md font-semibold text-gray-900 dark:text-gray-200 truncate"
              :title="video.title"
            >
              {{ video.title }}
              <span
                class="text-sm font-normal text-blue-500 dark:text-blue-400"
              >
                (조회수: {{ video.view_count }})
              </span>
            </h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
              {{ video.uploader_username }}
            </p>
          </div>
        </div>
      </div>
      <div
        v-else
        class="text-center text-gray-500 dark:text-gray-400 py-10 bg-gray-50 dark:bg-gray-800 rounded-lg"
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
          class="text-blue-500 hover:underline dark:text-blue-400"
          >더보기 &rarr;</router-link
        >
      </div>
      <div
        v-if="latestVideos.length > 0"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        <div
          v-for="video in latestVideos"
          :key="video.id"
          class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 hover:shadow-xl transition-all duration-300"
        >
          <router-link :to="{ name: 'video-detail', params: { id: video.id } }">
            <img
              :src="video.thumbnail"
              :alt="video.title"
              class="w-full h-40 object-cover"
            />
          </router-link>
          <div class="p-4">
            <h3
              class="text-md font-semibold text-gray-900 dark:text-gray-200 truncate"
              :title="video.title"
            >
              {{ video.title }}
            </h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
              {{ video.uploader_username }}
            </p>
          </div>
        </div>
      </div>
      <div
        v-else
        class="text-center text-gray-500 dark:text-gray-400 py-10 bg-gray-50 dark:bg-gray-800 rounded-lg"
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
          class="text-blue-500 hover:underline dark:text-blue-400"
          >더보기 &rarr;</router-link
        >
      </div>
      <div v-if="latestPosts.length > 0" class="space-y-4">
        <div
          v-for="post in latestPosts"
          :key="post.id"
          class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200 cursor-pointer"
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
        class="text-center text-gray-500 dark:text-gray-400 py-10 bg-gray-50 dark:bg-gray-800 rounded-lg"
      >
        <p>아직 작성된 게시글이 없습니다.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "@/api";

const latestVideos = ref([]);
const latestPosts = ref([]);
const weeklyPopularVideos = ref([]);

onMounted(async () => {
  try {
    // 세 가지 API 요청을 동시에 보냅니다.
    const [videosResponse, postsResponse, popularResponse] = await Promise.all([
      api.getVideos(),
      api.getPosts(),
      api.getWeeklyPopularVideos(),
    ]);

    // 비디오 목록은 최신순으로 정렬하여 4개만 잘라옵니다.
    latestVideos.value = videosResponse.data
      .sort((a, b) => b.id - a.id)
      .slice(0, 4);

    // 게시글 목록도 최신순으로 정렬하여 5개만 잘라옵니다.
    latestPosts.value = postsResponse.data
      .sort((a, b) => b.id - a.id)
      .slice(0, 5);

    weeklyPopularVideos.value = popularResponse.data;
  } catch (error) {
    console.error("메인 페이지 데이터 로딩 실패:", error);
  }
});
</script>
