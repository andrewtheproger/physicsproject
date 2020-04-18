<template>
  <div>
    <h2 style="color: white">Добавить задачу</h2>
    <form v-on:submit.prevent="sendTask">
      <p>Укажите номер задачи:</p>
      <input type="text" v-model="number" /><br />
      <p>Укажите количество ссылок на картинки:</p>
      <input type="text" v-model="hrefs" /><br />
      <p>Укажите ссылки:</p>
      <input type="text" v-model="href1" v-if="Number(hrefs) >= 1" /><br
        v-if="Number(hrefs) >= 1"
      />
      <input type="text" v-model="href2" v-if="Number(hrefs) >= 2" /><br
        v-if="Number(hrefs) >= 2"
      />
      <input type="text" v-model="href3" v-if="Number(hrefs) >= 3" /><br
        v-if="Number(hrefs) >= 3"
      />
      <input type="text" v-model="href4" v-if="Number(hrefs) >= 4" /><br
        v-if="Number(hrefs) >= 4"
      />
      <input type="text" v-model="href5" v-if="Number(hrefs) >= 5" /><br
        v-if="Number(hrefs) >= 5"
      />
      <p>Укажите решение в формате LaTeX:</p>
      <textarea cols="30" rows="15" v-model="latex"> </textarea>
      <br/>>
      <input type="submit" value="Отправить">
    </form>
  </div>
</template>
<script>
import { mapActions } from "vuex";
export default {
  data() {
    return {
      number: "",
      hrefs: "1",
      href1: "",
      href2: "",
      href3: "",
      href4: "",
      href5: "",
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
<style lang="scss" scoped></style>
