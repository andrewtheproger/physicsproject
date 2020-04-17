<template>
  <div id="app">
    <header>
      <div class = "header">
        <div class="title">
          <router-link to="/">3800 онлайн</router-link>
        </div>
        <div class="container">
          <div>
            <router-link to="/search">Главная</router-link>
          </div>
          <div>
            <router-link to="/about">О проекте</router-link>
          </div>
        </div>
      </div>
    </header>
    <router-view />
  </div>
</template>

<script>
import axios from "axios";
import config from "@/config/api";
export default {
  name: "App",
  data() {
    return {
      isApiOk: null,
    };
  },
  methods: {
    checkApiOk() {
      axios({
        url: config.apiPrefix + "/health",
        method: "GET",
      }).then(
        (result) => {
          this.isApiOk = result.data.status === "ok";
        },
        (error) => {
          console.log(error);

          this.isApiOk = false;
        }
      );
    },
  },
  mounted() {
    this.checkApiOk();
  },
};
</script>

<style lang="scss">
.header {
  display: flex;
  flex-direction: column;
}
.container {
  flex: 1;
  display: flex;
  div {
    flex: 1;
    border: 1px solid lightgray;
    text-align: center;
    height: 50px;
    font-size: 32px;
  }
}
.title {
  flex: 1;
  border: 1px solid lightgray;
  text-align: center;
  height: 25px;
  font-size: 32px;
  color: white;
}
body {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #252525;
  margin: 0;
  padding: 0;
  p {
    color: white;
  }
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}

header {
  a {
    font-weight: bold;
    color: white;

    &.router-link-exact-active {
      color: white;
    }
  }
}
</style>
