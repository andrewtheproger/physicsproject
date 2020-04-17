import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    showingTask: undefined
  },
  mutations: {
    changeShowing(state, problem) {
      state.showingTask = problem
    }
  },
  actions: {
    async getTaskByNum(ctx, num) {
      const res = (await fetch(`http://127.0.0.1:5000/api/tasks?page=0&count=10&order=number&filter_by_number=${num}`))
      const problem = await res.json()
      ctx.commit("changeShowing", problem[0])
    }
  },
  getters: {
    getShowing(state){
      return state.showingTask
    }
  }
});
