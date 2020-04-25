<template>
  <div>
    <h2 style="color: white;">Добавить задачу</h2>
    <form v-on:submit.prevent="sendTask">
      <p>Укажите номер задачи:</p>
      <md-field>
        <md-input type="text" v-model="number" />
        <br />
      </md-field>
      <p>Укажите издание задачника</p>
      <md-field>
        <md-input type="text" v-model="isbn" />
        <br />
      </md-field>
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
        <md-field>
          <md-input type="text" name="" id="" v-model="hrefs[item - 1]" />
        </md-field>
      </div>
      <p>Укажите решение в формате LaTeX:</p>
      <md-field>
        <md-textarea cols="30" rows="15" v-model="latex"> </md-textarea
      ></md-field>
      <br />
      <md-field>
        <md-input type="submit" value="Отправить" />
      </md-field>
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
      isbn: "",
    };
  },
  methods: {
    ...mapActions(["sendProblem"]),
    sendTask() {
      this.sendProblem(this.hrefs, this.number, this.latex);
    },
  },
};
</script>
<style lang="scss" scoped>
p {
  color: white;
}
</style>
