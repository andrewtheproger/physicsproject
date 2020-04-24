<template>
  <div class="ph-main">
    <h1>Войти:</h1>
    <div class="ph-reg">
      <form v-on:submit.prevent="getTask">
        <p>Введите логин:</p>
        <md-field>
        <md-input type="text" v-model="login" /></md-field>
        <p>Введите пароль</p>
        <md-field>
        <md-input type="password" v-model="password" />
        </md-field>
        <md-field>
        <md-input type="submit" />
        </md-field>
      </form>
    </div>
  </div>
</template>
<script>
import { mapActions } from "vuex";
export default {
  name: "User",
  data() {
    return { login: "", password: "" };
  },
  methods: {
    ...mapActions(["getUser"]),
    getTask() {
      this.getUser(this.login, this.password);
    }
  }
};
</script>
<style lang="scss" scoped>
p {
  color: white;
}
.ph-reg {
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
.ph-main {
  margin: auto;
  margin-top: 150px;
  width: 300px;
  border: 1px solid lightgray;
  width: 200px;
  text-align: center;
}
</style>
