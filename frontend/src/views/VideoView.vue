<template>
  <div class="container mx-auto my-12 px-4">
    <h1
      class="text-4xl font-bold text-center mb-10 text-gray-800 dark:text-gray-100"
    >
      동영상
    </h1>

    <div
      v-if="authStore.isLoggedIn"
      class="upload-form bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md mb-12 max-w-2xl mx-auto"
    >
      <h3 class="text-2xl font-semibold mb-4 text-gray-700 dark:text-gray-200">
        새 동영상 업로드
      </h3>
      <form @submit.prevent="submitVideo" class="space-y-4">
        <input
          type="text"
          v-model="newVideo.title"
          placeholder="제목"
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <textarea
          v-model="newVideo.description"
          placeholder="설명"
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
        ></textarea>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label
              for="thumbnail"
              class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
              >썸네일 이미지:</label
            >
            <input
              id="thumbnail"
              type="file"
              @change="handleThumbnailUpload"
              accept="image/*"
              required
              class="w-full text-sm text-gray-500 dark:text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 dark:file:bg-blue-900 dark:file:text-blue-200 dark:hover:file:bg-blue-800"
            />
          </div>
          <div>
            <label
              for="video"
              class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
              >동영상 파일:</label
            >
            <input
              id="video"
              type="file"
              @change="handleVideoUpload"
              accept="video/*"
              required
              class="w-full text-sm text-gray-500 dark:text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-50 file:text-violet-700 hover:file:bg-violet-100 dark:file:bg-violet-900 dark:file:text-violet-200 dark:hover:file:bg-violet-800"
            />
          </div>
        </div>

        <button
          type="submit"
          class="w-full bg-violet-500 text-white font-bold py-2 px-4 rounded-md hover:bg-violet-600 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:ring-opacity-50 transition-colors duration-300"
        >
          업로드
        </button>
      </form>
    </div>
    <hr
      v-if="authStore.isLoggedIn"
      class="my-12 border-t border-gray-200 dark:border-gray-700"
    />

    <div class="video-list">
      <h2 class="text-3xl font-bold mb-6 text-gray-800 dark:text-gray-100">
        전체 동영상
      </h2>
      <div
        v-if="videos.length > 0"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
      >
        <div
          v-for="video in videos"
          :key="video.id"
          class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 hover:shadow-xl transition-all duration-300"
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
      </div>
      <div
        v-else
        class="text-center text-gray-500 dark:text-gray-400 py-10 bg-gray-50 dark:bg-gray-800 rounded-lg"
      >
        <p>아직 업로드된 동영상이 없습니다.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
// <script setup> 내용은 수정할 필요가 없습니다.
import { ref, reactive, onMounted } from "vue";
import api from "@/api";
import { useAuthStore } from "@/store/auth";

const authStore = useAuthStore();
const videos = ref([]);
const newVideo = reactive({
  title: "",
  description: "",
  thumbnail: null,
  video_file: null,
});

const fetchVideos = async () => {
  try {
    const response = await api.getVideos();
    videos.value = response.data;
  } catch (error) {
    console.error("동영상 목록 로딩 실패:", error);
  }
};

const handleThumbnailUpload = (event) => {
  newVideo.thumbnail = event.target.files[0];
};
const handleVideoUpload = (event) => {
  newVideo.video_file = event.target.files[0];
};

const submitVideo = async () => {
  if (!newVideo.thumbnail || !newVideo.video_file) {
    alert("썸네일과 동영상 파일을 모두 선택해주세요.");
    return;
  }

  const formData = new FormData();
  formData.append("title", newVideo.title);
  formData.append("description", newVideo.description);
  formData.append("thumbnail", newVideo.thumbnail);
  formData.append("video_file", newVideo.video_file);

  try {
    await api.uploadVideo(formData);
    alert("동영상이 성공적으로 업로드되었습니다.");
    Object.assign(newVideo, {
      title: "",
      description: "",
      thumbnail: null,
      video_file: null,
    });
    document
      .querySelectorAll('input[type="file"]')
      .forEach((input) => (input.value = ""));
    fetchVideos();
  } catch (error) {
    console.error("동영상 업로드 실패:", error);
    alert("동영상 업로드에 실패했습니다.");
  }
};

onMounted(fetchVideos);
</script>

<style scoped>
/* Tailwind CSS가 모든 스타일을 처리하므로 비워둡니다. */
</style>
