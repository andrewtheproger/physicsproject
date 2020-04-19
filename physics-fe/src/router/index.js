import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../components/Home";
import Main from "../components/Main";
import About from "../components/About";
import User from "../components/User";

Vue.use(VueRouter);

const routes = [
  {
    path: "/search",
    name: "Home",
    component: Home
  },
  {
    path: "/",
    name: "Main",
    component: Main
  },
  {
    path: "/about",
    name: "About",
    component: About
  },
  {
    path: "/user",
    name: "User",
    component: User
  }
];

const router = new VueRouter({
  routes
});

export default router;
