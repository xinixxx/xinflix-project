<template>
  <div class="video-container">
    <h1>동영상</h1>

    <div v-if="authStore.isLoggedIn" class="upload-form">
      <h3>새 동영상 업로드</h3>
      <form @submit.prevent="submitVideo">
        <input
          type="text"
          v-model="newVideo.title"
          placeholder="제목"
          required
        />
        <textarea
          v-model="newVideo.description"
          placeholder="설명"
          required
        ></textarea>

        <div>
          <label for="thumbnail">썸네일 이미지:</label>
          <input
            type="file"
            @change="handleThumbnailUpload"
            accept="image/*"
            required
          />
        </div>

        <div>
          <label for="video">동영상 파일:</label>
          <input
            type="file"
            @change="handleVideoUpload"
            accept="video/*"
            required
          />
        </div>

        <button type="submit">업로드</button>
      </form>
    </div>
    <hr />

    <div class="video-list">
      <h2>동영상 목록</h2>
      <ul>
        <li v-for="video in videos" :key="video.id">
          <img :src="video.thumbnail" :alt="video.title" class="thumbnail" />
          <div class="video-info">
            <h3>{{ video.title }}</h3>
            <p>업로더: {{ video.uploader_username }}</p>
            <video
              :src="video.video_file"
              controls
              class="video-player"
            ></video>
            <!-- day 9 때는 세부 페이지로 영상 옮길 예정이라 video 란 삭제 예정 -->
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
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

  // FormData 객체를 생성하여 데이터를 담습니다.
  const formData = new FormData();
  formData.append("title", newVideo.title);
  formData.append("description", newVideo.description);
  formData.append("thumbnail", newVideo.thumbnail);
  formData.append("video_file", newVideo.video_file);

  try {
    await api.uploadVideo(formData);
    alert("동영상이 성공적으로 업로드되었습니다.");
    // 폼 초기화 및 목록 새로고침
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
.video-container {
  max-width: 800px;
  margin: 40px auto; /* ... */
}
.upload-form div {
  margin-bottom: 15px;
}
.video-list li {
  display: flex;
  align-items: flex-start;
  margin-bottom: 20px;
}
.thumbnail {
  width: 160px;
  height: 90px;
  object-fit: cover;
  margin-right: 15px;
  border-radius: 4px;
}
.video-info {
  flex-grow: 1;
} /* 추가: 제목 등이 비디오 옆 공간을 채우도록 함 */
.video-player {
  width: 100%; /* 부모 요소 너비에 맞춤 */
  max-width: 640px; /* 너무 커지지 않도록 최대 너비 지정 */
  margin-top: 10px;
  border-radius: 4px;
}
</style>
