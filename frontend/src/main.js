import { createApp } from "vue";
import { createPinia } from "pinia"; // Pinia 추가
import App from "./App.vue";
import router from "./router";

const app = createApp(App);

app.use(createPinia()); // Pinia 등록
app.use(router);

app.mount("#app");
