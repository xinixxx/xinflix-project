<template>
  <div id="app" class="flex flex-col bg-gray-100 min-h-screen dark:bg-gray-900">
    <header class="bg-white shadow dark:bg-gray-800">
      <nav
        class="container mx-auto px-6 py-4 flex justify-between items-center"
      >
        <router-link
          to="/"
          class="text-xl font-bold text-gray-800 dark:text-gray-100"
          >XINFLIX</router-link
        >
        <div class="flex items-center space-x-4">
          <button
            @click="themeStore.toggleTheme"
            class="p-2 rounded-full text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700"
          >
            <span v-if="themeStore.isDarkMode">☀️</span>
            <span v-else>🌙</span>
          </button>

          <router-link
            to="/board"
            class="text-gray-600 hover:text-blue-500 dark:text-gray-300"
            >게시판</router-link
          >
          <router-link
            to="/videos"
            class="text-gray-600 hover:text-blue-500 dark:text-gray-300"
            >동영상</router-link
          >

          <template v-if="!authStore.isLoggedIn">
            <router-link
              to="/signup"
              class="bg-gray-200 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600"
              >회원가입</router-link
            >
            <router-link
              to="/login"
              class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
              >로그인</router-link
            >
          </template>
          <template v-else>
            <button
              @click="handleLogout"
              class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600"
            >
              로그아웃
            </button>
          </template>
        </div>
      </nav>
    </header>
    <main class="flex-grow">
      <router-view />
    </main>
  </div>
</template>

<script setup>
// 스크립트 부분은 수정할 필요 없이 완벽합니다.
import { useAuthStore } from "@/store/auth";
import { useRouter } from "vue-router";
import { useThemeStore } from "@/store/theme";
import { onMounted } from "vue";

const authStore = useAuthStore();
const router = useRouter();
const themeStore = useThemeStore();

const handleLogout = () => {
  authStore.logout();
  alert("로그아웃 되었습니다.");
  router.push("/");
};

onMounted(() => {
  themeStore.initTheme();
});
</script>
