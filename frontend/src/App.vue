<template>
  <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/board">게시판</router-link> |

    <span v-if="!authStore.isLoggedIn">
      <router-link to="/signup">회원가입</router-link> |
      <router-link to="/login">로그인</router-link>
    </span>

    <span v-else>
      <button @click="handleLogout">로그아웃</button>
    </span>
  </nav>
  <router-view />
</template>

<script setup>
import { useAuthStore } from "./store/auth";
import { useRouter } from "vue-router";

const authStore = useAuthStore();
const router = useRouter();

const handleLogout = () => {
  authStore.logout();
  alert("로그아웃 되었습니다.");
  router.push("/"); //메인 페이지로 이동
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}

nav button {
  background: none;
  border: none;
  color: #2c3e50;
  text-decoration: underline;
  cursor: pointer;
  padding: 0;
  font-size: 1em;
}
nav button.router-link-exact-active {
  color: #42b983;
}
</style>
