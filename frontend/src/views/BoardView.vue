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
          class="bg-gray-50 dark:bg-gray-700 p-6 rounded-lg shadow-sm transition-all duration-300"
        >
          <div v-if="!post.isEditing">
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
            <p
              class="text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-wrap"
            >
              {{ post.content }}
            </p>
          </div>

          <div v-else class="space-y-2">
            <input
              type="text"
              v-model="post.editableTitle"
              class="w-full px-3 py-2 border border-gray-300 rounded-md dark:bg-gray-600 dark:border-gray-500 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <textarea
              v-model="post.editableContent"
              rows="5"
              class="w-full px-3 py-2 border border-gray-300 rounded-md dark:bg-gray-600 dark:border-gray-500 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
            ></textarea>
          </div>

          <div
            v-if="post.is_author"
            class="mt-4 flex items-center justify-end space-x-4"
          >
            <template v-if="!post.isEditing">
              <button
                @click="startEditing(post)"
                class="text-sm font-medium text-blue-600 dark:text-blue-400 hover:underline"
              >
                수정
              </button>
              <button
                @click="removePost(post.id)"
                class="text-sm font-medium text-red-600 dark:text-red-400 hover:underline"
              >
                삭제
              </button>
            </template>
            <template v-else>
              <button
                @click="savePost(post)"
                class="text-sm font-medium text-green-600 dark:text-green-400 hover:underline"
              >
                저장
              </button>
              <button
                @click="cancelEditing(post)"
                class="text-sm font-medium text-gray-600 dark:text-gray-400 hover:underline"
              >
                취소
              </button>
            </template>
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

const removePost = async (postId) => {
  if (confirm("정말로 이 게시글을 삭제하시겠습니까?")) {
    try {
      await api.deletePost(postId);
      alert("게시글이 삭제되었습니다.");
      fetchPosts(); // 목록 새로고침
    } catch (error) {
      alert("삭제에 실패했습니다. 권한이 있는지 확인해주세요.");
      console.error(error);
    }
  }
};

const startEditing = (post) => {
  post.isEditing = true;
};

const cancelEditing = (post) => {
  post.isEditing = false;
  // 수정 취소 시, 원래 내용으로 되돌립니다.
  post.editableTitle = post.title;
  post.editableContent = post.content;
};

const savePost = async (post) => {
  try {
    await api.updatePost(post.id, {
      title: post.editableTitle,
      content: post.editableContent,
    });
    alert("게시글이 수정되었습니다.");
    post.isEditing = false;
    fetchPosts(); // 목록 새로고침
  } catch (error) {
    alert("수정에 실패했습니다. 권한이 있는지 확인해주세요.");
    console.error(error);
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
