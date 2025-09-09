import axios from "axios";

const apiClient = axios.create({
  // Django API 서버의 기본 URL 설정
  // 클라우드 서버 업로드시 변경 필요
  baseURL: "http://127.0.0.1:8000/api/",
  headers: {
    "Content-Type": "application/json",
  },
});

// API 요청 함수들을 정의합니다

export default {
  signup(data) {
    // apiClient.post(url, data) 형식으로 요청을 보냅니다.
    return apiClient.post("users/signup/", data);
  },
  // 여기에 login, getPosts 등의 함수를 추가할 예정
  login(data) {
    return apiClient.post("token/", data); // simplejwt 의 기본 토큰 발급 URL
  },
};
