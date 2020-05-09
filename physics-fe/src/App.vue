<template>
  <div id="app" :style="getClass_body">
    <header>
      <md-tabs class="ph-menu" md-sync-route>
        <md-tab id="tab-home" md-label="3800" to="/" exact></md-tab>
        <md-tab
          :md-disabled="user.is_token_expired"
          id="tab-add"
          md-label="Добавить задачу"
          to="/add"
          exact
        ></md-tab>
        <md-tab
          id="tab-latex"
          md-label="Редактор LaTeX"
          to="/latex"
          exact
        ></md-tab>
        <md-tab id="tab-about" md-label="О проекте" to="/about" exact></md-tab>

        <md-tab id="tab-user" md-icon="face" to="/user" exact> </md-tab>
      </md-tabs>

      <div>
        <ul class="ph-warnings">
          <li :class="getApiInfoClass">
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
import config from "./config/api";
import http_helper from "./lib/http";
export default {
  name: "App",
  data() {
    return {
      isApiOk: null,
      user: {
        is_token_expired: null,
        color_background_primary: "#252525",
        color_background_secondary: "#555",
        color_foreground_primary: "#ccc",
        color_foreground_secondary: "#ccf",
        link_color: "violet",
        icon_color: "yellow",
      },
    };
  },
  computed: {
    getApiInfoClass() {
      if (this.isApiOk === null) {
        return "ph-hidden";
      }

      return this.isApiOk ? "ph-hidden" : "fart";
    },
    getClass_body() {
      const parse = require("parse-color");
      const toColor = (color) => {
        if (!color) {
          return {
            rgb: null,
            r: null,
            b: null,
            c: null,
          };
        }
        const rgb = parse(color).rgb;
        return {
          rgb: color,
          r: rgb[0],
          g: rgb[1],
          b: rgb[2],
        };
      };
      const patchWithCssVariables = (slave, colorName, colorValue) => {
        const color = toColor(colorValue);
        slave[colorName] = color.rgb;
        slave[`${colorName}-r`] = color.r;
        slave[`${colorName}-g`] = color.g;
        slave[`${colorName}-b`] = color.b;
        return slave;
      };
      const styles = {
        "--background-success-color": "#050",
        "--background-warning-color": "#550",
        "--background-error-color": "#500",
        "--background-action-color": "#448aff",
        "--foreground-success-color": "#0f0",
        "--foreground-warning-color": "#ff0",
        "--foreground-error-color": "#f00",
        "--foreground-action-color": "#fff",
      };
      patchWithCssVariables(
        styles,
        "--background-primary-color",
        this.user.color_background_primary
      );
      patchWithCssVariables(
        styles,
        "--background-secondary-color",
        this.user.color_background_secondary
      );
      patchWithCssVariables(
        styles,
        "--foreground-primary-color",
        this.user.color_foreground_primary
      );
      patchWithCssVariables(
        styles,
        "--foreground-secondary-color",
        this.user.color_foreground_secondary
      );
      patchWithCssVariables(styles, "--link-color", "violet");

      patchWithCssVariables(styles, "--icon-color", "yellow");
      return styles;
    },
  },
  methods: {
    checkApiOk() {
      axios({
        url: config.apiPrefix + "/health",
        method: "GET",
      }).then(
        (result) => {
          this.isApiOk = result.data.status === "ok";
          console.log("api is " + this.isApiOk);
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
    http_helper
      .getMeAsUser(this.$store.getters.get_jwt)
      .then((response) => (this.user = response.data));
  },
};
</script>

<style lang="scss">
@import "config/variables.scss";
@import "~vue-material/dist/theme/engine"; // Import the theme engine

@include md-register-theme(
  "default",
  (
    primary: yellow // The primary color of your application,,
  )
);

@import "~vue-material/dist/components/MdButton/theme";
@import "~vue-material/dist/components/MdIcon/theme";
a {
  color: violet !important;
  .md-tab-nav-button {
    color: var(--foreground-primary-color) !important;
  }
}

.md-button {
  background-color: var(--icon-color) !important;;
  color: var(--foreground-primary-color);
  
}
.ph-hidden {
  display: none;
}
.ph-warnings {
  list-style: none;
  background-color: var(--background-warning-color);
  color: var(--foreground-warning-color);
}
.ph-failure {
  color: var(--foreground-error-color);
}
div.md-field.md-theme-default {
  &.md-invalid .md-error {
    -webkit-text-fill-color: var(--foreground-error-color);
    color: var(--foreground-error-color);
  }
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
    background-color: var(--background-secondary-color);
    .md-button {
      color: var(--foreground-primary-color) !important;

      background-color: var(--background-secondary-color) !important;
      .md-icon {
        color: var(--foreground-primary-color);
      }
    }
    .md-button.md-active {
      color: var(--foreground-primary-color);
      .md-icon {
        color: var(--foreground-primary-color);
      }
    }
  }
  .md-tabs-indicator {
    background-color: var(--foreground-secondary-color);
  }
}
// that's the most root component because
// that's the only one we can inline css variables
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: var(--background-primary-color);
  color: var(--foreground-secondary-color);
  min-height: 100vh;
  margin: 0;
  padding: 0;
}
div.md-card.md-theme-default {
  color: inherit;
  background-color: var(--background-secondary-color);
}
i.md-icon.md-theme-default.md-icon-font {
  color: var(--foreground-secondary-color);
}
button.md-button.md-theme-default.md-raised:not([disabled]).md-primary {
  color: var(--foreground-action-color);
  background-color: var(--background-action-color);
}
div.md-field,
div.md-field.md-theme-default.md-has-textarea,
div.md-field.md-theme-default,
div.md-field.md-theme-default.md-focused,
div.md-field.md-theme-default.md-focused textarea.md-textarea,
div.md-field.md-theme-default.md-has-value,
div.md-field.md-theme-default.md-has-value textarea.md-textarea {
  -webkit-text-fill-color: var(--foreground-primary-color);
  .md-input,
  label {
    color: var(--foreground-primary-color);
    -webkit-text-fill-color: var(--foreground-primary-color);
  }
  &:after,
  &:before,
  &:not(.md-autogrow):after,
  &:not(.md-autogrow):before {
    background-color: var(--foreground-primary-color);
    transition: all 0.3s;
  }
  &:hover:after {
    background-color: var(--foreground-secondary-color);
    transition: all 0.3s;
  }
  &:hover {
    transition: all 0.3s;
  }
  .md-icon.md-theme-default.md-icon-font svg {
    fill: var(--foreground-primary-color);
  }
}
.md-field.md-theme-default label {
  padding-left: 1em;
}

.ph-success {
  background-color: var(--background-success-color);
  color: var(--foreground-success-color);
}

.ph-failure {
  background-color: var(--background-error-color);
  color: var(--foreground-error-color);
}
</style>
