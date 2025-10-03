<template>
  <div
    v-if="isLoading"
    class="flex justify-center items-center"
    style="height: 80vh"
  >
    <baseSpinner />
  </div>

  <div v-else-if="error" class="text-center py-20">
    <p class="text-red-500">{{ error }}</p>
  </div>

  <div
    v-else-if="post"
    class="container mx-auto my-12 p-8 bg-white dark:bg-gray-800 rounded-lg shadow-lg max-w-3xl"
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
        class="w-full px-4 py-2 border border-gray-300 rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <textarea
        v-model="editableContent"
        rows="10"
        class="w-full px-4 py-2 border border-gray-300 rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
      ></textarea>
    </div>

    <div
      v-if="post.is_author"
      class="mt-8 flex items-center justify-end space-x-4"
    >
      <template v-if="!isEditing">
        <button
          @click="startEditing"
          class="text-sm font-medium text-blue-600 dark:text-blue-400 hover:underline"
        >
          수정
        </button>
        <button
          @click="removePost"
          class="text-sm font-medium text-red-600 dark:text-red-400 hover:underline"
        >
          삭제
        </button>
      </template>
      <template v-else>
        <button
          @click="savePost"
          class="text-sm font-medium text-green-600 dark:text-green-400 hover:underline"
        >
          저장
        </button>
        <button
          @click="cancelEditing"
          class="text-sm font-medium text-gray-600 dark:text-gray-400 hover:underline"
        >
          취소
        </button>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/api";
import BaseSpinner from "@/components/BaseSpinner.vue";

const route = useRoute();
const router = useRouter();
const post = ref(null);
const postId = ref(route.params.id);

const isLoading = ref(true);
const error = ref(null);

const isEditing = ref(false);
const editableTitle = ref("");
const editableContent = ref("");

const fetchData = async (id) => {
  try {
    isLoading.value = true;
    error.value = null;
    const response = await api.getPostDetail(id);
    post.value = response.data;
    editableTitle.value = post.value.title;
    editableContent.value = post.value.content;
  } catch (err) {
    error.value = "게시글을 불러오는데 실패했습니다.";
    console.error(err);
  } finally {
    isLoading.value = false;
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

// 다른 게시글로 이동할 경우를 대비한 watch
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
