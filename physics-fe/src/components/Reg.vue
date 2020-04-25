<template>
  <div class="ph-main">
    <h1>Зарегистрироваться:</h1>
    <div class="ph-reg">
      <form v-on:submit.prevent="getTask">
        <p>Введите вашу почту:</p>
        <md-field> <md-input type="text" v-model="login"/></md-field>
        <p>Введите пароль:</p>
        <md-field>
          <md-input type="password2" v-model="password" />
        </md-field>
        <p>Введите пароль еще раз:</p>
        <md-field>
          <md-input type="password1" v-model="password" />
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
    return { login: "", password1: "", password2: "" };
  },
  methods: {
    ...mapActions(["regUser"]),
    getTask() {
      this.regUser(this.login, this.password);
    }
  }
};
</script>
<style lang="scss" scoped>
@import "../config/variables.scss";
.md-field,
.md-field.md-theme-default.md-focused,
.md-field.md-theme-default.md-focused,
.md-field.md-theme-default.md-has-value {
  border-bottom: 1px solid $primary-fg-color;
  input.md-input {
    color: inherit;
    -webkit-text-fill-color: $primary-fg-color;
  }
  textarea.md-textarea {
    color: inherit;
    -webkit-text-fill-color: $primary-fg-color;
    border: 1px solid $primary-fg-color;
  }
  label {
    padding-left: 1em;
    color: $secondary-bg-color;
  }
}
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
  width: 400px;
  border: 3px solid lightgray;
  text-align: center;
}
</style>
