import { defineStore } from "pinia";
import { jwtDecode } from "jwt-decode";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    accessToken: localStorage.getItem("accessToken") || null,
    refreshToken: localStorage.getItem("refreshToken") || null,
    user: null,
  }),
  getters: {
    isLoggedIn: (state) => {
      if (!state.accessToken) {
        return false;
      }
      try {
        const decoded = jwtDecode(state.accessToken);
        return decoded.exp * 1000 > Date.now();
      } catch (e) {
        return false;
      }
    },
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
          if (decoded.exp * 1000 < Date.now()) {
            this.logout();
          } else {
            this.user = decoded;
          }
        } catch (e) {
          console.error("Error decoding token on init", e);
          this.logout();
        }
      }
    },
  },
});
