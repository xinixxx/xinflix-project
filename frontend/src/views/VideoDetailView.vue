<template>
  <div class="video-detail-container" v-if="video">
    <h1>{{ video.title }}</h1>
    <p class="meta">
      업로더: {{ video.uploader_username }} | 게시일:
      {{ new Date(video.created_at).toLocaleDateString() }}
    </p>
    <video
      :src="video.video_file"
      controls
      autoplay
      class="video-player"
    ></video>
    <div class="actions">
      <button @click="pressLike" :class="{ liked: video.is_liked }">
        👍 좋아요 ({{ video.like_count }})
      </button>
    </div>
    <div class="description">
      <p>{{ video.description }}</p>
    </div>

    <hr />
    <div class="comments-section">
      <h2>댓글 ({{ comments.length }})</h2>

      <div v-if="authStore.isLoggedIn" class="comment-form">
        <form @submit.prevent="submitComment">
          <textarea
            v-model="newComment.content"
            placeholder="댓글을 입력하세요..."
            required
          ></textarea>
          <button type="submit">등록</button>
        </form>
      </div>

      <ul class="comment-list">
        <li v-for="comment in comments" :key="comment.id">
          <p>
            <strong>{{ comment.author_username }}</strong>
          </p>
          <p>{{ comment.content }}</p>
          <span class="comment-date">{{
            new Date(comment.created_at).toLocaleString()
          }}</span>
        </li>
      </ul>
    </div>
  </div>
  <div v-else>
    <p>동영상을 불러오는 중입니다...</p>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { useRoute } from "vue-router";
import api from "@/api";
import { useAuthStore } from "@/store/auth"; // authStore import 추가

const route = useRoute();
const authStore = useAuthStore(); // authStore 사용
const video = ref(null);
const comments = ref([]); // 댓글 목록을 담을 ref
const newComment = reactive({ content: "" }); // 새 댓글 내용을 담을 reactive 객체
const videoId = route.params.id; // videoId를 script setup 최상위에서 접근 가능하도록 변경

// 댓글 목록을 불러오는 함수
const fetchComments = async () => {
  try {
    const response = await api.getComments(videoId);
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

  console.log('"좋아요" 버튼 클릭! API에 전달할 비디오 ID:', video.value.id);

  try {
    await api.toggleLike(video.value.id);
    // 좋아요 성공 후, 화면을 새로고침하지 않고 바로 UI에 반영
    if (video.value.is_liked) {
      video.value.like_count -= 1; // 좋아요 취소
    } else {
      video.value.like_count += 1; // 좋아요
    }
    video.value.is_liked = !video.value.is_liked; // is_liked 상태 반전
  } catch (error) {
    console.error("좋아요 처리에 실패했습니다.", error);
    alert("좋아요 처리에 실패했습니다.");
  }
};

// 새 댓글을 작성하는 함수
const submitComment = async () => {
  try {
    await api.createComment(videoId, newComment);
    newComment.content = ""; // 폼 초기화
    fetchComments(); // 댓글 목록 새로고침
  } catch (error) {
    console.error("댓글 작성에 실패했습니다.", error);
    alert("댓글 작성에 실패했습니다.");
  }
};

onMounted(async () => {
  try {
    const response = await api.getVideoDetail(videoId);
    video.value = response.data;
    // 동영상 정보를 불러온 후, 댓글 목록도 함께 불러옵니다.
    fetchComments();
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
hr {
  border: none;
  border-top: 1px solid #eaeaea;
  margin: 40px 0;
}
.comments-section h2 {
  margin-bottom: 20px;
}
.comment-form textarea {
  width: 100%;
  min-height: 80px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-bottom: 10px;
  resize: vertical;
}
.comment-form button {
  padding: 10px 15px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  float: right;
}
.comment-list {
  list-style: none;
  padding: 0;
  margin-top: 60px; /* 폼과의 간격 확보 */
}
.comment-list li {
  border-bottom: 1px solid #eaeaea;
  padding: 15px 0;
}
.comment-list p {
  margin: 0 0 5px 0;
}
.comment-list strong {
  font-size: 1.1em;
}
.comment-date {
  font-size: 0.8em;
  color: #888;
}
.actions {
  margin-bottom: 20px;
}
.actions button {
  padding: 10px 15px;
  border: 1px solid #ccc;
  border-radius: 20px;
  background-color: #f5f5f5;
  cursor: pointer;
  font-size: 1em;
}
/* 좋아요를 눌렀을 때의 스타일 */
.actions button.liked {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}
</style>
