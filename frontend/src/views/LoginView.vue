<template>
  <div
    class="flex items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900"
  >
    <div
      class="w-full max-w-md p-8 space-y-8 bg-white rounded-lg shadow-lg dark:bg-gray-800"
    >
      <h1
        class="text-3xl font-bold text-center text-gray-800 dark:text-gray-100"
      >
        로그인
      </h1>
      <form @submit.prevent="submitForm" class="space-y-6">
        <div>
          <label
            for="username"
            class="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >사용자 이름</label
          >
          <div class="mt-1">
            <input
              type="text"
              id="username"
              v-model="form.username"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
        <div>
          <label
            for="password"
            class="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >비밀번호</label
          >
          <div class="mt-1">
            <input
              type="password"
              id="password"
              v-model="form.password"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
        <div>
          <button
            type="submit"
            class="w-full bg-blue-500 text-white font-bold py-2 px-4 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition-colors duration-300"
          >
            로그인
          </button>
        </div>
      </form>
      <p v-if="errorMessage" class="text-center text-red-500">
        {{ errorMessage }}
      </p>
    </div>
  </div>
</template>

<script setup>
// <script setup> 부분의 로직은 이미 완벽하므로 수정할 필요가 없습니다.
import { reactive, ref } from "vue";
import api from "@/api";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/auth";

const router = useRouter();
const authStore = useAuthStore();
const form = reactive({
  username: "",
  password: "",
});
const errorMessage = ref("");

const submitForm = async () => {
  try {
    const response = await api.login(form);
    authStore.setTokens(response.data.access, response.data.refresh);

    alert("로그인에 성공했습니다!");
    router.push("/"); // 로그인 성공 시 메인 페이지로 이동
  } catch (error) {
    console.error("로그인 실패:", error);
    errorMessage.value =
      "로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요.";
  }
};
</script>
