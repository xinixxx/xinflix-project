<template>
  <div class="board-container">
    <h1>자유 게시판</h1>

    <div v-if="authStore.isLoggedIn" class="post-form">
      <h3>새 글 작성</h3>
      <form @submit.prevent="submitPost">
        <input
          type="text"
          v-model="newPost.title"
          placeholder="제목"
          required
        />
        <textarea
          v-model="newPost.content"
          placeholder="내용"
          required
        ></textarea>
        <button type="submit">작성</button>
      </form>
    </div>

    <hr />

    <div class="post-list">
      <h2>게시글 목록</h2>
      <ul>
        <li v-for="post in posts" :key="post.id">
          <h3>{{ post.title }}</h3>
          <p>작성자: {{ post.author_username }}</p>
          <p>{{ post.content }}</p>
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
const posts = ref([]);
const newPost = reactive({
  title: "",
  content: "",
});

// 모든 게시글을 불러오는 함수
const fetchPosts = async () => {
  try {
    const response = await api.getPosts();
    posts.value = response.data;
  } catch (error) {
    console.error("게시글 목록을 불러오는데 실패했습니다.", error);
  }
};

// 새 게시글을 작성하는 함수
const submitPost = async () => {
  try {
    await api.createPost(newPost);
    alert("게시글이 성공적으로 작성되었습니다.");
    newPost.title = ""; // 폼 초기화
    newPost.content = ""; // 폼 초기화
    fetchPosts(); // 게시글 목록 새로고침
  } catch (error) {
    console.error("게시글 작성에 실패했습니다.", error);
    alert("글 작성은 로그인한 사용자만 가능합니다.");
  }
};

// 컴포넌트가 마운트될 때 게시글 목록을 불러옵니다.
onMounted(() => {
  fetchPosts();
});
</script>

<style scoped>
/* 전체 컨테이너에 그림자 효과와 부드러운 폰트를 적용합니다. */
.board-container {
  max-width: 600px; /* 너비를 조금 늘려 답답함을 해소합니다. */
  margin: 40px auto;
  padding: 30px;
  border: 1px solid #eaeaea;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
    Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
}

/* 제목(h1, h2, h3) 아래에 적절한 간격을 추가합니다. */
h1,
h2,
h3 {
  margin-top: 0;
  margin-bottom: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
}

/* 구분선 스타일을 깔끔하게 변경합니다. */
hr {
  border: none;
  border-top: 1px solid #eaeaea;
  margin: 30px 0;
}

/* 글쓰기 폼 스타일 */
.post-form {
  display: flex;
  flex-direction: column; /* 요소들을 세로로 정렬합니다. */
}

/* 입력 필드와 버튼에 통일된 스타일과 간격을 적용합니다. */
.post-form input,
.post-form textarea,
.post-form button {
  width: 100%;
  padding: 12px;
  margin-bottom: 15px; /* 각 요소 아래에 간격을 줍니다. */
  border-radius: 6px;
  border: 1px solid #ccc;
  box-sizing: border-box; /* 패딩과 테두리를 너비에 포함시킵니다. */
  font-size: 1em;
}

.post-form textarea {
  min-height: 120px; /* 텍스트 영역의 최소 높이를 지정합니다. */
  resize: vertical; /* 세로로만 크기 조절이 가능하도록 합니다. */
}

/* 버튼 스타일 및 호버 효과 */
.post-form button {
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.post-form button:hover {
  background-color: #36a473; /* 마우스를 올렸을 때 색상을 살짝 어둡게 합니다. */
}

/* 게시글 목록 스타일 */
.post-list ul {
  list-style: none;
  padding: 0;
}

/* 각 게시글을 카드 형태로 만듭니다. */
.post-list li {
  border: 1px solid #eaeaea;
  padding: 20px;
  margin-bottom: 15px;
  border-radius: 8px;
  background-color: #fafafa;
}

.post-list h3 {
  margin-bottom: 10px;
}

.post-list p {
  margin: 0;
  color: #555;
  line-height: 1.6;
}

.post-list p:first-of-type {
  font-size: 0.9em;
  color: #888;
  margin-bottom: 10px;
}
</style>
