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
        <div data-vjs-player>
          <video
            ref="videoPlayer"
            class="video-js vjs-big-play-centered w-full rounded-lg shadow-lg"
          ></video>
        </div>
        <div class="quality-selector mt-4">
          <label
            for="quality-select"
            class="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >화질 선택:</label
          >
          <select
            id="quality-select"
            @change="changeQuality"
            class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200"
          >
            <option
              v-for="source in sortedSources"
              :key="source.label"
              :value="source.src"
            >
              {{ source.label }}
            </option>
          </select>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mt-6">
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
import {
  ref,
  reactive,
  onMounted,
  onBeforeUnmount,
  computed,
  watch,
  nextTick,
} from "vue";
import { useRoute } from "vue-router";
import api from "@/api";
import { useAuthStore } from "@/store/auth";
import BaseSpinner from "@/components/BaseSpinner.vue";
import videojs from "video.js";
import "video.js/dist/video-js.css";

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

const videoPlayer = ref(null);
let player = null;

const likeButtonClass = computed(() => {
  return video.value?.is_liked
    ? "bg-blue-100 text-blue-600 border border-blue-300 dark:bg-blue-900 dark:text-blue-200 dark:border-blue-700"
    : "bg-gray-100 text-gray-600 border border-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:border-gray-600 hover:bg-gray-200 dark:hover:bg-gray-600";
});

const sortedSources = computed(() => {
  if (!video.value || !video.value.files) return [];
  return video.value.files
    .map((file) => ({
      src: file.file,
      type: "video/mp4",
      label: file.resolution,
      res: parseInt(file.resolution),
    }))
    .sort((a, b) => parseInt(a.label) - parseInt(b.label)); // Sort ascending for display
});

const changeQuality = (event) => {
  const selectedSrc = event.target.value;
  if (player && selectedSrc) {
    player.src({ src: selectedSrc, type: "video/mp4" });
    player.play();
  }
};

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

const initializePlayer = (videoData) => {
  if (player) {
    player.dispose();
  }
  // nextTick을 사용해 DOM이 업데이트된 후 플레이어를 초기화합니다.
  nextTick(() => {
    const options = {
      autoplay: true,
      controls: true,
      responsive: true,
      fluid: true,
      poster: videoData.thumbnail,
      controlBar: {
        children: [
          "playToggle",
          "volumePanel",
          "currentTimeDisplay",
          "timeDivider",
          "durationDisplay",
          "progressControl",
          "liveDisplay",
          "remainingTimeDisplay",
          "customControlSpacer",
          "playbackRateMenuButton",
          "chaptersButton",
          "descriptionsButton",
          "subtitlesButton",
          "captionsButton",
          "audioTrackButton",
          "fullscreenToggle",
        ],
      },
    };
    const sources = videoData.files
      .map((file) => ({
        src: file.file,
        type: "video/mp4",
        label: file.resolution,
        res: parseInt(file.resolution), // Add res property
      }))
      .sort((a, b) => parseInt(b.label) - parseInt(a.label));

    if (videoPlayer.value) {
      player = videojs(videoPlayer.value, options, () => {
        console.log("Player is ready");
        player.src(sources);
        player.on("play", handlePlay);

        // Set the default selected quality in the dropdown to match the playing video
        // The 'sources' array is sorted descending, so the first element is the highest quality
        if (sources.length > 0) {
          const highestQualitySrc = sources[0].src;
          const qualitySelectElement =
            document.getElementById("quality-select");
          if (qualitySelectElement) {
            qualitySelectElement.value = highestQualitySrc;
          }
        }
      });
    }
  });
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
    error.value.error = "데이터를 불러오는데 실패했습니다.";
    console.error(err);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchData(videoId.value);
});

onBeforeUnmount(() => {
  if (player) {
    player.dispose();
  }
});

watch(
  () => video.value,
  (newVideo) => {
    if (newVideo) {
      nextTick(() => {
        initializePlayer(newVideo);
      });
    }
  }
);

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
