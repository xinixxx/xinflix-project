import axios from "axios";
import { useAuthStore } from "@/store/auth"; // Pinia 스토어 import

const apiClient = axios.create({
  // Django API 서버의 기본 URL 설정
  // 클라우드 서버 업로드시 변경 필요
  baseURL: "http://127.0.0.1:8000/api/",
  headers: {
    "Content-Type": "application/json",
  },
});

// Axios 요청 인터셉터 추가
apiClient.interceptors.request.use(
  (config) => {
    // 요청을 보내기 전에 Pinia 스토어에서 토큰을 가져옵니다.
    const authStore = useAuthStore();
    const token = authStore.accessToken;

    // 토큰이 존재하면 Authorization 헤더에 추가합니다.
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

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
  // 게시판 API 함수들을 추가합니다
  getPosts() {
    return apiClient.get("community/posts/");
  },
  createPost(data) {
    return apiClient.post("community/posts/", data);
  },
  // 영상 리스트 불러오기
  getVideos() {
    return apiClient.get("videos/");
  },
  // 영상 파일 업로드
  uploadVideo(formData) {
    return apiClient.post("videos/", formData, {
      headers: {
        "Content-Type": "multipart/form-data", // 헤더를 'multipart/form-data' 로 명시
      },
    });
  },
};
