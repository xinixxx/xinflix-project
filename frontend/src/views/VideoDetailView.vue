<template>
  <div
    v-if="isLoading"
    class="flex justify-center items-center"
    style="height: 80vh"
  >
    <BaseSpinner />
  </div>

  <div v-else-if="error" class="text-center py-20">
    <p class="text-red-500">{{ error }}</p>
  </div>

  <div v-else-if="video" class="container mx-auto my-12 px-4 pb-12">
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <div class="bg-black rounded-lg shadow-lg overflow-hidden mb-6">
          <video
            :src="video.stream_url"
            controls
            autoplay
            class="w-full"
            @play="handlePlay"
          ></video>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">
            {{ video.title }}
          </h1>
          <p class="text-md text-gray-500 dark:text-gray-400 mb-4">
            업로더:
            <span class="font-medium text-gray-700 dark:text-gray-300">{{
              video.uploader_username
            }}</span>
            | 게시일: {{ new Date(video.created_at).toLocaleDateString() }}
          </p>
          <div class="actions mb-6">
            <button
              @click="pressLike"
              :class="likeButtonClass"
              class="flex items-center space-x-2 px-4 py-2 rounded-full font-semibold text-sm transition-colors duration-200"
            >
              <span v-if="video.is_liked">❤️</span><span v-else>🤍</span>
              <span>좋아요 ({{ video.like_count }})</span>
            </button>
          </div>
          <div class="description bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
            <p
              class="text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-wrap"
            >
              {{ video.description }}
            </p>
          </div>
        </div>

        <div
          class="comments-section mt-10 bg-white dark:bg-gray-800 rounded-lg shadow-md p-6"
        >
          <h2 class="text-2xl font-bold text-gray-800 dark:text-gray-100 mb-6">
            댓글 ({{ comments.length }})
          </h2>
          <form
            v-if="authStore.isLoggedIn"
            @submit.prevent="submitComment"
            class="comment-form mb-8"
          >
            <textarea
              v-model="newComment.content"
              placeholder="댓글을 추가하세요..."
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
            ></textarea>
            <button
              type="submit"
              class="mt-2 float-right bg-blue-500 text-white font-bold py-2 px-4 rounded-md hover:bg-blue-600 transition-colors duration-200"
            >
              등록
            </button>
          </form>
          <ul class="comment-list space-y-4">
            <li
              v-for="comment in comments"
              :key="comment.id"
              class="border-t border-gray-200 dark:border-gray-700 pt-4"
            >
              <p class="font-semibold text-gray-800 dark:text-gray-200">
                {{ comment.author_username }}
              </p>
              <p class="text-gray-600 dark:text-gray-300 my-1">
                {{ comment.content }}
              </p>
              <span class="text-xs text-gray-500 dark:text-gray-400">{{
                new Date(comment.created_at).toLocaleString()
              }}</span>
            </li>
          </ul>
        </div>
      </div>

      <div class="lg:col-span-1 space-y-4">
        <h2 class="text-2xl font-bold text-gray-800 dark:text-gray-100">
          관련 동영상
        </h2>
        <div
          v-for="relatedVideo in relatedVideos"
          :key="relatedVideo.id"
          class="bg-white dark:bg-gray-800 rounded-lg shadow-sm overflow-hidden flex hover:shadow-lg transition-shadow duration-200"
        >
          <router-link
            :to="{ name: 'video-detail', params: { id: relatedVideo.id } }"
            class="flex w-full"
          >
            <img
              :src="relatedVideo.thumbnail"
              :alt="relatedVideo.title"
              class="w-32 h-20 object-cover"
            />
            <div class="p-3">
              <h3
                class="text-sm font-semibold text-gray-900 dark:text-gray-200 leading-snug truncate"
                :title="relatedVideo.title"
              >
                {{ relatedVideo.title }}
              </h3>
              <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">
                {{ relatedVideo.uploader_username }}
              </p>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from "vue";
import { useRoute } from "vue-router";
import api from "@/api";
import { useAuthStore } from "@/store/auth";
import BaseSpinner from "@/components/BaseSpinner.vue";

const route = useRoute();
const authStore = useAuthStore();
const video = ref(null);
const comments = ref([]);
const newComment = reactive({ content: "" });
const relatedVideos = ref([]);
const videoId = ref(route.params.id);

const isLoading = ref(true);
const error = ref(null);
const hasBeenViewed = ref(false);

const likeButtonClass = computed(() => {
  return video.value?.is_liked
    ? "bg-blue-100 text-blue-600 border border-blue-300 dark:bg-blue-900 dark:text-blue-200 dark:border-blue-700"
    : "bg-gray-100 text-gray-600 border border-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:border-gray-600 hover:bg-gray-200 dark:hover:bg-gray-600";
});

const fetchComments = async (currentVideoId) => {
  try {
    const response = await api.getComments(currentVideoId);
    comments.value = response.data;
  } catch (error) {
    console.error("댓글을 불러오는데 실패했습니다.", error);
  }
};

const pressLike = async () => {
  if (!authStore.isLoggedIn) {
    alert("로그인이 필요합니다.");
    return;
  }
  try {
    await api.toggleLike(video.value.id);
    if (video.value.is_liked) {
      video.value.like_count -= 1;
    } else {
      video.value.like_count += 1;
    }
    video.value.is_liked = !video.value.is_liked;
  } catch (error) {
    console.error("좋아요 처리에 실패했습니다.", error);
    alert("좋아요 처리에 실패했습니다.");
  }
};

const submitComment = async () => {
  try {
    await api.createComment(videoId.value, newComment);
    newComment.content = "";
    fetchComments(videoId.value);
  } catch (error) {
    console.error("댓글 작성에 실패했습니다.", error);
    alert("댓글 작성에 실패했습니다.");
  }
};

const handlePlay = () => {
  if (!hasBeenViewed.value && video.value) {
    api.incrementViewCount(video.value.id);
    hasBeenViewed.value = true;
  }
};

const fetchData = async (id) => {
  try {
    isLoading.value = true;
    error.value = null;

    const [videoResponse, relatedVideosResponse] = await Promise.all([
      api.getVideoDetail(id),
      api.getRelatedVideos(id),
    ]);

    video.value = videoResponse.data;
    relatedVideos.value = relatedVideosResponse.data;
    fetchComments(id);
  } catch (err) {
    error.value = "데이터를 불러오는데 실패했습니다.";
    console.error(err);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchData(videoId.value);
});

watch(
  () => route.params.id,
  (newId) => {
    if (newId && newId !== videoId.value) {
      videoId.value = newId;
      fetchData(newId);
    }
  }
);
</script>
