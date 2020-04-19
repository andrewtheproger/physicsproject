<template>
  <div id="app">
    <header>
        <md-tabs md-sync-route>
          <md-tab id="tab-home" md-label="3800" to="/search" exact></md-tab>
          <md-tab id="tab-about" md-label="О проекте" to="/about" exact></md-tab>
          <md-tab id="tab-registration" md-icon="face" to="/user" exact></md-tab>
        </md-tabs>

        <div>
          <ul class="ph-warnings">
            <li :class="this.isApiOk ? 'ph-hidden' : ''">Что-то не работает, мы уже чиним.</li>
          </ul>
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
      isApiOk: null
    };
  },

  methods: {
    checkApiOk() {
      axios({
        url: config.apiPrefix + "/health",
        method: "GET",
      }).then(
        result => {
          this.isApiOk = result.data.status === "ok";
          console.log('api is ' + this.isApiOk)
        },
        error => {
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

.ph-hidden {
  display: none;
}

.ph-warnings {
  list-style: none;

  color: #fa5;
}

div.md-tabs.md-theme-default {
  .md-tabs {
    width: 100%;
  }

  padding: 0.5em;
  display: flex;
  justify-content: space-between;

  font-size: 150%;

  .md-tabs-navigation {
    a:last-of-type {
      margin-left: auto;
    }

    background-color: #555;

    .md-button {
      color: #ccc;

      .md-icon {
        color: #ccc;
      }
    }

    .md-button.md-active {
      color: white;

      .md-icon {
        color: white;
      }
    }
  }

  .md-tabs-indicator {
    background-color: #ccf;
  }
}

.title {
  flex: 9;
  text-align: center;
  height: 40px;
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
