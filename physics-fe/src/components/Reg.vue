<template>
  <div class="main">
    <h1>Войти:</h1>
    <div class="reg">
      <form v-on:submit.prevent="getTask">
        <p>Введите логин:</p>
        <input type="text" v-model="login" />
        <p>Введите пароль</p>
        <input type="password" v-model="password" />

        <input type="submit" />
      </form>
    </div>
  </div>
</template>
<script>
import { mapActions } from "vuex";
export default {
  name: "Reg",
  data() {
    return { login: "", password: "" };
  },
  methods: {
    ...mapActions(["getUser"]),
    getTask() {
      this.getUser(this.login, this.password);
    },
  },
};
</script>
<style lang="scss" scoped>
.reg {
  text-align: center;
}
h1 {
  color: white;
}
input {
  color: white;
  border: 1px solid lightgray;
  background-color: #252525;
  margin: 5px;
}
.main {
  margin: auto;
  margin-top: 150px;
  width: 300px;
  border: 1px solid lightgray;
  width: 200px;
  text-align: center;
}
</style>
