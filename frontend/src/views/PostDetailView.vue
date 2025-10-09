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

  <div v-else-if="post" class="container mx-auto my-12 px-4 pb-12">
    <div
      class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 max-w-3xl mx-auto"
    >
      <div v-if="!isEditing">
        <h1 class="text-4xl font-bold text-gray-900 dark:text-gray-100 mb-4">
          {{ post.title }}
        </h1>
        <p class="text-md text-gray-500 dark:text-gray-400 mb-8">
          작성자:
          <span class="font-medium text-gray-700 dark:text-gray-300">{{
            post.author_username
          }}</span>
          | 게시일: {{ new Date(post.created_at).toLocaleDateString() }}
        </p>
        <div class="prose dark:prose-invert max-w-none">
          <p
            class="text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-wrap"
          >
            {{ post.content }}
          </p>
        </div>
      </div>

      <div v-else class="space-y-4">
        <input
          type="text"
          v-model="editableTitle"
          class="w-full text-4xl font-bold ..."
        />
        <textarea
          v-model="editableContent"
          rows="10"
          class="w-full ..."
        ></textarea>
      </div>

      <div
        v-if="post.is_author"
        class="mt-8 flex items-center justify-end space-x-4"
      >
        <template v-if="!isEditing">
          <button @click="startEditing" class="text-sm ...">수정</button>
          <button @click="removePost" class="text-sm ...">삭제</button>
        </template>
        <template v-else>
          <button @click="savePost" class="text-sm ...">저장</button>
          <button @click="cancelEditing" class="text-sm ...">취소</button>
        </template>
      </div>
      d
    </div>

    <div
      class="comments-section mt-10 bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 max-w-3xl mx-auto"
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
          class="w-full ..."
        ></textarea>
        <button type="submit" class="mt-2 ...">등록</button>
      </form>
      <ul class="comment-list space-y-4">
        <li v-for="comment in comments" :key="comment.id" class="border-t ...">
          <p class="font-semibold ...">{{ comment.author_username }}</p>
          <p class="text-gray-600 ...">{{ comment.content }}</p>
          <span class="text-xs ...">{{
            new Date(comment.created_at).toLocaleString()
          }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/api";
import { useAuthStore } from "@/store/auth"; // authStore import
import BaseSpinner from "@/components/BaseSpinner.vue";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore(); // authStore 선언

const post = ref(null);
const postId = ref(route.params.id);
const comments = ref([]);
const newComment = reactive({ content: "" });

const isLoading = ref(true);
const error = ref(null);

const isEditing = ref(false);
const editableTitle = ref("");
const editableContent = ref("");

// 게시글과 댓글 데이터를 모두 불러오는 함수
const fetchData = async (id) => {
  try {
    isLoading.value = true;
    error.value = null;

    // 게시글 상세 정보와 댓글 목록을 동시에 요청
    const [postResponse, commentsResponse] = await Promise.all([
      api.getPostDetail(id),
      api.getPostComments(id),
    ]);

    post.value = postResponse.data;
    comments.value = commentsResponse.data;

    // 수정용 데이터 초기화
    editableTitle.value = post.value.title;
    editableContent.value = post.value.content;
  } catch (err) {
    error.value = "데이터를 불러오는데 실패했습니다.";
    console.error(err);
  } finally {
    isLoading.value = false;
  }
};

// 댓글 작성 함수
const submitComment = async () => {
  try {
    await api.createPostComment(postId.value, newComment);
    newComment.content = "";
    // 댓글 작성 후 댓글 목록만 새로고침
    const response = await api.getPostComments(postId.value);
    comments.value = response.data;
  } catch (error) {
    console.error("댓글 작성에 실패했습니다.", error);
    alert("댓글 작성에 실패했습니다.");
  }
};

const removePost = async () => {
  if (confirm("정말로 이 게시글을 삭제하시겠습니까?")) {
    try {
      await api.deletePost(postId.value);
      alert("게시글이 삭제되었습니다.");
      router.push("/board");
    } catch (error) {
      alert("삭제에 실패했습니다. 권한이 있는지 확인해주세요.");
      console.error(error);
    }
  }
};

const startEditing = () => {
  isEditing.value = true;
};

const cancelEditing = () => {
  isEditing.value = false;
  editableTitle.value = post.value.title;
  editableContent.value = post.value.content;
};

const savePost = async () => {
  try {
    await api.updatePost(postId.value, {
      title: editableTitle.value,
      content: editableContent.value,
    });
    alert("게시글이 수정되었습니다.");
    isEditing.value = false;
    fetchData(postId.value); // 데이터 새로고침
  } catch (error) {
    alert("수정에 실패했습니다. 권한이 있는지 확인해주세요.");
    console.error(error);
  }
};

onMounted(() => {
  fetchData(postId.value);
});

watch(
  () => route.params.id,
  (newId) => {
    if (newId) {
      postId.value = newId;
      fetchData(newId);
    }
  }
);
</script>
