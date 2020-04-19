import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
// import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css'
import { MdTabs, MdIcon, MdButton, MdField, MdContent } from 'vue-material/dist/components'
import VueMathjax from 'vue-mathjax'

Vue.use(VueMathjax)
Vue.use(MdTabs)
Vue.use(MdIcon)
Vue.use(MdButton)
Vue.use(MdField)
Vue.use(MdContent)

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
