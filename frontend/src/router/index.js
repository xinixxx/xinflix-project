import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

// SignupView 를 import
import SignupView from "../views/SignupView.vue";
// LoginView 를 import
import LoginView from "../views/LoginView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
  {
    // SignupView 경로 추가
    path: "/signup",
    name: "signup",
    component: SignupView,
  },
  {
    // login 경로 추가
    path: "/login",
    name: "login",
    component: LoginView,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
