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
        회원가입
      </h1>
      <form @submit.prevent="submitForm" class="space-y-6">
        <div>
          <label
            for="username"
            class="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >아이디</label
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
          <label
            for="nickname"
            class="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >닉네임</label
          >
          <div class="mt-1">
            <input
              type="text"
              id="nickname"
              v-model="form.nickname"
              class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
        <div>
          <button
            type="submit"
            class="w-full bg-green-500 text-white font-bold py-2 px-4 rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50 transition-colors duration-300"
          >
            가입하기
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
// <script setup> 부분의 로직은 수정할 필요가 없습니다.
import { reactive, ref } from "vue";
import api from "@/api";
import { useRouter } from "vue-router";

const router = useRouter();
const form = reactive({
  username: "",
  password: "",
  nickname: "",
});
const errorMessage = ref("");

const submitForm = async () => {
  try {
    const response = await api.signup(form);
    console.log(response.data.message);
    alert("회원가입에 성공했습니다! 로그인 페이지로 이동합니다.");
    router.push("/login");
  } catch (error) {
    console.error("회원가입 실패:", error.response.data);
    errorMessage.value = Object.values(error.response.data).join(" ");
  }
};
</script>
