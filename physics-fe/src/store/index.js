import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    showingTask: undefined
  },
  mutations: {
    changeShowing(state, problem) {
      state.showingTask = problem;
    },
    goesWellReg() {},
    goesWellLog() {},
    goesBadReg() {},
    goesBadLog() {},
    goesWell() {
      document.cookie = "user=admin; path=/; expires=60*60*24*365";
    },
    goesBad() {}
  },
  actions: {
    async getTaskByNum(ctx, num) {
      const res = await fetch(
        `http://127.0.0.1:5000/api/tasks?page=0&count=10&order=number&filter_by_number=${num}`
      );
      const problem = await res.json();
      ctx.commit("changeShowing", problem[0]);
    },
    async getUser(ctx) {
      //const res = (await fetch(`http://127.0.0.1:5000/api/tasks?page=0&count=10&order=number&filter_by_number=${login}`))
      //const problem = await res.json()
      const res = true;
      res ? ctx.commit("goesWellLog") : ctx.commit("goesBadLog");
    },
    async regUser(ctx) {
      //const res = (await fetch(`http://127.0.0.1:5000/api/tasks?page=0&count=10&order=number&filter_by_number=${login}`))
      //const problem = await res.json()
      const res = true;
      res ? ctx.commit("goesWellReg") : ctx.commit("goesBadPeg");
    },
    async sendProblem(ctx, image_hrefs, latex, number) {
      fetch(`http://127.0.0.1:5000/api/tasks`, {
        method: "POST",
        body: JSON.stringify({ number, body: { latex, image_hrefs } })
      });
      ctx.commit("goesBad");
    }
  },
  getters: {
    getShowing(state) {
      return state.showingTask;
    }
  }
});
