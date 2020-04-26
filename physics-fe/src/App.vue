<template>
  <div id="app">
    <header>
      <md-tabs md-sync-route>
        <md-tab id="tab-home" md-label="3800" to="/" exact></md-tab>
        <md-tab
          id="tab-add"
          md-label="Добавить задачу"
          to="/add"
          exact
        ></md-tab>
        <md-tab id="tab-about" md-label="О проекте" to="/about" exact></md-tab>
        <md-tab id="tab-registration" md-icon="face" to="/reg" exact></md-tab>
      </md-tabs>

      <div>
        <ul class="ph-warnings">
          <li :class="this.isApiOk ? 'ph-hidden' : ''">
            Что-то не работает, мы уже чиним.
          </li>
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
        method: "GET"
      }).then(
        result => {
          this.isApiOk = result.data.status === "ok";
          console.log("api is " + this.isApiOk);
        },
        error => {
          console.log(error);
          this.isApiOk = false;
        }
      );
    }
  },
  mounted() {
    this.checkApiOk();
  }
};
</script>

<style lang="scss">
@import "config/variables.scss";

body {
  color: $primary-fg-color;
}

.ph-hidden {
  display: none;
}

.ph-warnings {
  list-style: none;

  color: $warning-fg-color;
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

    background-color: $secondary-bg-color;

    .md-button {
      color: $primary-fg-color;

      .md-icon {
        color: $primary-fg-color;
      }
    }

    .md-button.md-active {
      color: $primary-fg-color;

      .md-icon {
        color: $primary-fg-color;
      }
    }
  }

  .md-tabs-indicator {
    background-color: $secondary-fg-color;
  }
}

body {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  background-color: $primary-bg-color;

  position: absolute;

  margin: 0;
  padding: 0;

  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}

div.md-field,
div.md-field.md-theme-default.md-has-textarea,
div.md-field.md-theme-default,
div.md-field.md-theme-default.md-focused,
div.md-field.md-theme-default.md-focused .md-textarea,
div.md-field.md-theme-default.md-has-value,
div.md-field.md-theme-default.md-has-value .md-textarea {
  .md-input,
  label {
    color: $primary-fg-color;
    -webkit-text-fill-color: $primary-fg-color;
  }

  &:after,
  &:before,
  &:not(.md-autogrow):after,
  &:not(.md-autogrow):before {
    background-color: $primary-fg-color;
    border-color: $primary-fg-color;
    transition: all 0.3s;
  }

  &:hover:after {
    background-color: $secondary-fg-color;
    transition: all 0.3s;
  }

  &:hover {
    border-color: $secondary-fg-color;
    transition: all 0.3s;
  }

  color: $primary-fg-color;
  -webkit-text-fill-color: $primary-fg-color;
}

.md-field.md-theme-default label,
.md-icon.md-theme-default.md-icon-font {
  color: inherit;
}

.md-field.md-theme-default label {
  padding-left: 1em;
}
</style>
