import { defineStore } from "pinia";
import { jwtDecode } from "jwt-decode";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    accessToken: localStorage.getItem("accessToken") || null,
    refreshToken: localStorage.getItem("refreshToken") || null,
    user: null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.accessToken, // accessToken 이 있으면 true, 없으면 false 반환
  },
  actions: {
    // 로그인 성공 시 토큰을 저장하는 액션
    setTokens(accessToken, refreshToken) {
      this.accessToken = accessToken;
      this.refreshToken = refreshToken;
      // 브라우저 저장소에 토큰을 저장하여 새로고침해도 유지되게 하기
      localStorage.setItem("accessToken", accessToken);
      localStorage.setItem("refreshToken", refreshToken);

      try {
        const decoded = jwtDecode(accessToken);
        this.user = decoded;
      } catch (e) {
        console.error("Error decoding token", e);
        this.user = null;
      }
    },
    // 로그아웃 시 토큰을 삭제하는 액션
    logout() {
      this.accessToken = null;
      this.refreshToken = null;
      this.user = null;
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
    },

    initialize() {
      if (this.accessToken) {
        try {
          const decoded = jwtDecode(this.accessToken);
          this.user = decoded;
        } catch (e) {
          console.error("Error decoding token on init", e);
          this.logout(); // 토큰이 유효하지 않으면 로그아웃 처리
        }
      }
    },
  },
});
