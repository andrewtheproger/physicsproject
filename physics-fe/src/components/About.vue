<template>
  <div>
    <h2 style="color: white;">Добавить задачу</h2>
    <form v-on:submit.prevent="sendTask">
      <p>Укажите номер задачи:</p>
      <input type="text" v-model="number" /><br />
      <div
        @click="
          hrefAmount++;
          hrefs.push('');
        "
      >
      <p>Увеличить количество ссылок:</p>
        <md-icon>add</md-icon>
      </div>
      <div v-for="item in hrefAmount" :key="item">
        <p>Добавьте ссылку:</p>
        <input type="text" name="" id="" v-model="hrefs[item - 1]" />
      </div>
      <p>Укажите решение в формате LaTeX:</p>
      <textarea cols="30" rows="15" v-model="latex"> </textarea>
      <br />>
      <input type="submit" value="Отправить" />
    </form>
  </div>
</template>
<script>
import { mapActions } from "vuex";
export default {
  name: "About",
  data() {
    return {
      number: "",
      hrefs: [],
      hrefAmount: 0,
      latex: "", 
    };
  },
  methods: {
    ...mapActions(["sendProblem"]),
    sendTask() {
      let massive = [];
      if (this.href1 !== "") {
        massive.push(this.href1);
      }
      if (this.href2 !== "") {
        massive.push(this.href2);
      }
      if (this.href3 !== "") {
        massive.push(this.href3);
      }
      if (this.href4 !== "") {
        massive.push(this.href4);
      }
      if (this.href5 !== "") {
        massive.push(this.href5);
      }
      this.sendProblem(massive, this.number, this.latex);
    },
  },
};
</script>
<style lang="scss" scoped>
p {
  color: white;
}
</style>
