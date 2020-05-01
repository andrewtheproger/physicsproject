import Vue from "vue";
import Vuex from "vuex";
import VuexPersistence from "vuex-persist";

Vue.use(Vuex);

const vuexLocal = new VuexPersistence({
  key: 'physicsproject',
  storage: window.localStorage,
  reducer: state => ({
    jwt: state.jwt
  })
});

export default new Vuex.Store({
  state: {
    jwt: null
  },
  getters: {
    get_jwt: state => {
      return state.jwt
    }
  },
  mutations: {
    set_jwt(state, jwt) {
      state.jwt = jwt
    }
  },
  plugins: [vuexLocal.plugin]
});
