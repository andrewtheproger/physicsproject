import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../components/Home";
import About from "../components/About";
import User from "../components/User";
//import TaskUpsert from "../components/TaskUpsert";
import Reg from "../components/Reg"
import TaskUpsert from "../components/TaskUpsert";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/about",
    name: "About",
    component: About
  },
  {
    path: "/add",
    name: "Add",
    component: TaskUpsert
  },
  {
    path: "/user",
    name: "User",
    component: User
  },
  {
   path: "/reg",
   name: "Reg",
   component: Reg,
  },
];

const router = new VueRouter({
  routes
});

export default router;
