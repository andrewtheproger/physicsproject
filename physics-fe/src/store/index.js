import Vue from "vue";
import Vuex from "vuex";
import VuexPersistence from "vuex-persist";

Vue.use(Vuex);

const vuexLocal = new VuexPersistence({
  key: "physicsproject",
  storage: window.localStorage,
  reducer: (state) => ({
    jwt: state.jwt,
    user: state.user,
  }),
}); 

export default new Vuex.Store({
  state: {
    jwt: null,
    user: {
      isAdmin: false,
      is_token_expired: true,
      role: null,
    },
  },
  getters: {
    get_jwt: (state) => {
      return state.jwt;
    },
  },
  mutations: {
    set_jwt(state, jwt) {
      if (jwt && !jwt.includes("Bearer")) {
        jwt = "Bearer " + jwt;
      }

      state.jwt = jwt;
    },
  },
  plugins: [vuexLocal.plugin],
});
