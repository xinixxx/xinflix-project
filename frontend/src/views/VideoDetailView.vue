<template>
  <div class="video-detail-container" v-if="video">
    <h1>{{ video.title }}</h1>
    <p class="meta">
      업로더 : {{ video.uploader_username }} | 게시일:
      {{ new Date(video.created_at).toLocaleDateString() }}
    </p>
    <video
      :src="video.video_file"
      controls
      autoplay
      class="video-player"
    ></video>
    <div class="description">
      <p>{{ video.description }}</p>
    </div>
  </div>
  <div v-else>
    <p>동영상을 불러오는 중...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import api from "@/api";

const route = useRoute(); // 현재 라우트 정보를 가져오기 위한 훅
const video = ref(null);

// 컴포넌트가 마운트(생성)되면 실행됩니다.
onMounted(async () => {
  try {
    const videoId = route.params.id; // URL 주소에 포함된 :id 값을 가져옵니다.
    const response = await api.getVideoDetail(videoId); // 해당 ID의 비디오 정보를 API로 요청
    video.value = response.data; // 응답 데이터를 video 변수에 저장
  } catch (error) {
    console.error("동영상 정보를 불러오는데 실패했습니다.", error);
  }
});
</script>
<style scoped>
.video-detail-container {
  max-width: 960px;
  margin: 40px auto;
  padding: 20px;
}
.video-player {
  width: 100%;
  border-radius: 8px;
  margin-bottom: 20px;
  background-color: #000;
}
.meta {
  color: #666;
  margin-bottom: 20px;
}
.description {
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
  line-height: 1.7;
  white-space: pre-wrap; /* \n 같은 줄바꿈 문자를 그대로 표시 */
}
</style>
