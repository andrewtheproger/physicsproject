import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "vue-material/dist/vue-material.css";
import "vue-material/dist/theme/default.css";
import VueMaterial from "vue-material";
import gallery from "img-vuer";
import { Photoshop } from "vue-color";
import VueClipboard from "vue-clipboard2";

Vue.use(VueMaterial);
Vue.use(gallery);
Vue.use(VueClipboard);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App),
  components: {
    "photoshop-picker": Photoshop
  }
}).$mount("#app");
