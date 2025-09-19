import { defineStore } from "pinia";

export const useThemeStore = defineStore("theme", {
  // 1. state : 현재 다크모드 여부를 저장
  state: () => ({
    isDarkMode: false,
  }),
  // 2. actions: 상태를 변경하는 로직입니다.
  actions: {
    // 테마를 토글하는 액션
    toggleTheme() {
      this.isDarkMode = !this.isDarkMode;

      // 실제 html 문서의 최상단에 dark 클래스를 추가하거나 제거
      if (this.isDarkMode) {
        document.documentElement.classList.add("dark");
        localStorage.setItem("theme", "dark"); // 선택을 브라우저에 저장
      } else {
        document.documentElement.classList.remove("dark");
        localStorage.setItem("theme", "light"); // 선택을 브라우저에 저장
      }
    },
    // 페이지를 새로고침해도 이전 설정을 유지하는 세션
    initTheme() {
      const saveTheme = localStorage.getItem("theme");
      if (saveTheme === "dark") {
        this.isDarkMode = true;
        document.documentElement.classList.add("dark");
      } else {
        this.isDarkMode = false;
        document.documentElement.classList.remove("dark");
      }
    },
  },
});
