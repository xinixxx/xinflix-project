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

  <div
    v-else
    class="container mx-auto my-12 p-8 bg-white dark:bg-gray-800 rounded-lg shadow-lg max-w-3xl"
  >
    <h1
      class="text-4xl font-bold text-center mb-8 text-gray-800 dark:text-gray-100"
    >
      자유 게시판
    </h1>

    <div v-if="authStore.isLoggedIn" class="mb-10">
      <h3 class="text-2xl font-semibold mb-4 text-gray-700 dark:text-gray-300">
        새 글 작성
      </h3>
      <form @submit.prevent="submitPost" class="space-y-4">
        <input
          type="text"
          v-model="newPost.title"
          placeholder="제목을 입력하세요"
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <textarea
          v-model="newPost.content"
          placeholder="내용을 입력하세요"
          required
          rows="5"
          class="w-full px-4 py-2 border border-gray-300 rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
        ></textarea>
        <button
          type="submit"
          class="w-full bg-blue-500 text-white font-bold py-2 px-4 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition-colors duration-300"
        >
          작성
        </button>
      </form>
    </div>

    <hr class="my-10 border-t border-gray-200 dark:border-gray-700" />

    <div class="post-list">
      <h2 class="text-3xl font-bold mb-6 text-gray-800 dark:text-gray-100">
        게시글 목록
      </h2>
      <ul class="space-y-6">
        <li
          v-for="post in posts"
          :key="post.id"
          class="bg-gray-50 dark:bg-gray-700 p-6 rounded-lg shadow-sm hover:shadow-md dark:hover:bg-gray-600 transition-all duration-300"
        >
          <h3
            class="text-2xl font-semibold text-gray-900 dark:text-gray-100 mb-2"
          >
            {{ post.title }}
          </h3>
          <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">
            작성자:
            <span class="font-medium text-gray-700 dark:text-gray-300">{{
              post.author_username
            }}</span>
          </p>
          <p class="text-gray-700 dark:text-gray-300 leading-relaxed">
            {{ post.content }}
          </p>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import api from "@/api";
import { useAuthStore } from "@/store/auth";
import BaseSpinner from "@/components/BaseSpinner.vue";

const authStore = useAuthStore();
const posts = ref([]);
const newPost = reactive({
  title: "",
  content: "",
});

const isLoading = ref(true);
const error = ref(null);

const fetchPosts = async () => {
  try {
    isLoading.value = true;
    error.value = null;
    const response = await api.getPosts();
    posts.value = response.data;
  } catch (err) {
    error.value = "게시글 목록을 불러오는데 실패했습니다.";
    console.error(err);
  } finally {
    isLoading.value = false;
  }
};

const submitPost = async () => {
  try {
    await api.createPost(newPost);
    alert("게시글이 성공적으로 작성되었습니다.");
    newPost.title = "";
    newPost.content = "";
    fetchPosts();
  } catch (error) {
    console.error("게시글 작성에 실패했습니다.", error);
    alert("글 작성은 로그인한 사용자만 가능합니다.");
  }
};

onMounted(() => {
  fetchPosts();
});
</script>
