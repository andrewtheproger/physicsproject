import Vue from "vue";
import VueRouter from "vue-router";
const Home = () =>
  import(/* webpackChunkName: "components_Home" */ "../components/Home");
const About = () =>
  import(/* webpackChunkName: "components_About" */ "../components/About");
const User = () =>
  import(/* webpackChunkName: "components_User" */ "../components/User");
const TaskUpsert = () =>
  import(
    /* webpackChunkName: "components_TaskUpsert" */ "../components/TaskUpsert"
  );
const Latex = () =>
  import(/* webpackChunkName: "components_Latex" */ "../components/Latex");

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
    path: "/edit/:id",
    name: "Edit",
    component: TaskUpsert
  },
  {
    path: "/user",
    name: "User",
    component: User
  },
  {
    path: "/latex",
    name: "latex",
    component: Latex,
    props: {
      localStorageKey: "ph-3800-latex-live-editor"
    }
  },
  {
    path: '/github',
    name: 'github',
    component: () => { window.open(
      'https://github.com/andrewtheproger/physicsproject',
      '_blank'
    ); return null; }
  }
];

export default new VueRouter({
  routes
});
