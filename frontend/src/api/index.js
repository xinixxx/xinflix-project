import axios from "axios";
import { useAuthStore } from "@/store/auth";

const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
  headers: {
    "Content-Type": "application/json",
  },
});

// Axios 요청 인터셉터 추가
apiClient.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    const token = authStore.accessToken;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default {
  // 사용자 API
  signup(data) {
    return apiClient.post("users/signup/", data);
  },
  login(data) {
    return apiClient.post("token/", data);
  },

  // 게시판 API
  getPosts() {
    return apiClient.get("posts/");
  },
  createPost(data) {
    return apiClient.post("posts/", data);
  },
  updatePost(postId, data) {
    return apiClient.put(`posts/${postId}/`, data);
  },
  deletePost(postId) {
    return apiClient.delete(`posts/${postId}/`);
  },

  // 동영상 API
  getVideos() {
    return apiClient.get("videos/");
  },
  getVideoDetail(id) {
    return apiClient.get(`videos/${id}/`);
  },
  getRelatedVideos(videoId) {
    return apiClient.get(`videos/${videoId}/related/`);
  },
  uploadVideo(formData) {
    return apiClient.post("videos/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  },
  deleteVideo(videoId) {
    return apiClient.delete(`videos/${videoId}/`);
  },

  // 댓글 API
  getComments(videoId) {
    return apiClient.get(`videos/${videoId}/comments/`);
  },
  createComment(videoId, data) {
    return apiClient.post(`videos/${videoId}/comments/`, data);
  },

  // 좋아요 API
  toggleLike(videoId) {
    return apiClient.post(`videos/${videoId}/like/`);
  },

  // 주간 인기 동영상 API
  getWeeklyPopularVideos() {
    return apiClient.get("videos/weekly-popular/");
  },

  // 조회수 증가 API 함수
  incrementViewCount(videoId) {
    return apiClient.post(`videos/${videoId}/view/`);
  },
};
