import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "vue-material/dist/vue-material.min.css";
import "vue-material/dist/theme/default.css";
import {
  MdTabs,
  MdIcon,
  MdButton,
  MdField,
  MdContent,
  MdProgress,
  MdTooltip,
  MdAutocomplete,
  MdMenu,
  MdList,
  MdCard,
  MdCheckbox
} from "vue-material/dist/components";
import gallery from "img-vuer";
import { Photoshop } from "vue-color";
import VueClipboard from 'vue-clipboard2'

Vue.use(MdTabs);
Vue.use(MdIcon);
Vue.use(MdButton);
Vue.use(MdField);
Vue.use(MdContent);
Vue.use(MdProgress);
Vue.use(MdTooltip);
Vue.use(MdAutocomplete);
Vue.use(MdMenu);
Vue.use(MdList);
Vue.use(MdCard);
Vue.use(MdCheckbox);
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
