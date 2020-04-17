import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    showingTask: {},
  },
  mutations: {
    changeTasks(state, tasks) {
      state.showingTask = tasks
    },

  },
  actions: {
    getTask(ctx, num) {
      let tasks
      fetch('http://127.0.0.1:5000/api/tasks?page=0&count=3800&order=number').then((res) => { tasks = res.json() })
      for (let n of tasks) {
        if (n.number === num) {
          ctx.commit("changeTasks", n)
        }
      }
    },
    suggestTask(ctx, data) {
      fetch('http://127.0.0.1:5000/api/tasks', {
        method: 'POST',
        headers: {
          'Content-type': 'applicatioon/json; charset = utf-8'
        },
        body: JSON.stringify(data)
      })
    },
    suggestHint(ctx, data) {
      fetch('http://127.0.0.1:5000/api/tasks/' + data.id + '/hints', {
        method: 'POST',
        headers: {
          'Content-type': 'applicatioon/json; charset = utf-8'
        },
        body: JSON.stringify(data)
      })
    },
    suggestHintChange(ctx, data) {
      fetch(`http://127.0.0.1:5000/api/tasks/${data.idone}/hints/${data.idtwo}/suggestions`, {
        method: 'POST',
        headers: {
          'Content-type': 'applicatioon/json; charset = utf-8'
        },
        body: JSON.stringify(data)
      })
    },
    approveHintChange(ctx, data) {
      fetch(`http://127.0.0.1:5000/api/tasks/${data.idone}/hints/${data.idtwo}/suggestions/${data.idthree}/approve`, {
        method: 'POST',
        headers: {
          'Content-type': 'applicatioon/json; charset = utf-8'
        },
        body: JSON.stringify(data)
      })
    },
    declinehintChange(ctx, data) {
      fetch(`http://127.0.0.1:5000/api/tasks/${data.idone}/hints/${data.idtwo}/suggestions/${data.idthree}/decline`, {
        method: 'POST',
        headers: {
          'Content-type': 'applicatioon/json; charset = utf-8'
        },
        body: JSON.stringify(data)
      })
    },
    delTask(ctx, data) {
      fetch('http://127.0.0.1:5000/api/tasks/1', {
        method: 'DEL',
        headers: {
          'Content-type': 'applicatioon/json; charset = utf-8'
        },
        body: JSON.stringify(data)
      })
    },
    
  },
  getters: {
    getShowing(state) {
      return state.showingTask
    }
  },
  setters: {},
});
