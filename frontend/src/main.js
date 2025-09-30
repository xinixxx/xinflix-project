import { createApp } from "vue";
import { createPinia } from "pinia"; // Pinia 추가
import { useAuthStore } from "./store/auth";
import App from "./App.vue";
import router from "./router";
import "./assets/tailwind.css";

const app = createApp(App);
const pinia = createPinia();
app.use(pinia);
app.use(router);

// useAuthStore는 Pinia가 앱에 등록된 후에 호출되어야 합니다.
const authStore = useAuthStore();
authStore.initialize();

app.mount("#app");
