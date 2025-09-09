import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    accessToken: null,
    refreshToken: null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.accessToken, // accessToken 이 있으면 true, 없으면 false 반환
  },
  actions: {
    // 로그인 성공 시 토큰을 저장하는 액션
    setTokens(accessToken, refreshToken) {
      this.accessToken = accessToken;
      this.refreshToken = refreshToken;
      // 브라우저 저장소에 토큰을 저장하여 새로고친해도 유지되게 하기
      localStorage.setItem("accessToken", accessToken);
    },
    // 로그아웃 시 토큰을 삭제하는 액션
    logout() {
      this.accessToken = null;
      this.refreshToken = null;
      localStorage.removeItem("accessToken");
    },
  },
});
