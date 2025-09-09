<template>
  <div class="signup-container">
    <h1>로그인</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="username">사용자 이름:</label>
        <input type="text" id="username" v-model="form.username" required />
      </div>
      <div class="form-group">
        <label for="password">비밀번호:</label>
        <input type="password" id="password" v-model="form.password" required />
      </div>
      <button type="submit">로그인</button>
    </form>
    <p v-if="errorMessage">{{ errorMessage }}</p>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import api from "@/api";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/auth"; // 방금 만든 Pinia 스토어 import

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
    // Pinia 스토어의 액션을 호출하여 토큰을 저장합니다.
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

<style scoped>
.signup-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
.form-group {
  margin-bottom: 15px;
}
label {
  display: block;
  margin-bottom: 5px;
}
input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}
button {
  width: 100%;
  padding: 10px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.error-message {
  color: red;
  margin-top: 15px;
}
</style>
