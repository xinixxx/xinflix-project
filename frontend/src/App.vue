<template>
  <div id="app" class="bg-gray-100 min-h-screen">
    <header class="bg-white shadow">
      <nav
        class="container mx-auto px-6 py-4 flex justify-between items-center"
      >
        <router-link to="/" class="text-xl font-bold text-gray-800"
          >XINFLIX</router-link
        >
        <div class="flex items-center space-x-4">
          <router-link to="/board" class="text-gray-600 hover:text-blue-500"
            >게시판</router-link
          >
          <router-link to="/videos" class="text-gray-600 hover:text-blue-500"
            >동영상</router-link
          >
          <template v-if="!authStore.isLoggedIn">
            <router-link
              to="/signup"
              class="bg-gray-200 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-300"
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
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useAuthStore } from "@/store/auth";
import { useRouter } from "vue-router";

const authStore = useAuthStore();
const router = useRouter();

const handleLogout = () => {
  authStore.logout();
  alert("로그아웃 되었습니다.");
  router.push("/"); //메인 페이지로 이동
};
</script>
