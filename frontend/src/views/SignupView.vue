<template>
  <div class="signup-container">
    <h1>회원가입</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="username">아이디:</label>
        <input type="text" id="username" v-model="form.username" required />
      </div>
      <div class="form-group">
        <label for="password">비밀번호:</label>
        <input type="password" id="password" v-model="form.password" required />
      </div>
      <div class="form-group">
        <label for="nickname">닉네임:</label>
        <input type="text" id="nickname" v-model="form.nickname" />
      </div>
      <button type="submit">가입하기</button>
    </form>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import api from "@/api"; // 2단계에서 만든 API 클라이언트 import
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
    // api.signup 함수를 호출하여 백엔드에 요청을 보냅니다.
    const response = await api.signup(form);
    console.log(response.data.message); // "회원가입이 성공적으로 완료되었습니다."
    alert("회원가입에 성공했습니다! 로그인 페이지로 이동합니다.");
    router.push("/login"); // 성공 시 /login 경로로 이동 (나중에 로그인 페이지 만들 예정)
  } catch (error) {
    console.error("회원가입 실패:", error.response.data);
    // Django에서 보내주는 에러 메시지를 표시합니다.
    errorMessage.value = Object.values(error.response.data).join(" ");
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
