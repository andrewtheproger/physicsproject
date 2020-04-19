import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
// import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css'
import { MdTabs, MdIcon, MdButton, MdField } from 'vue-material/dist/components'

Vue.use(MdTabs)
Vue.use(MdIcon)
Vue.use(MdButton)
Vue.use(MdField)

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
