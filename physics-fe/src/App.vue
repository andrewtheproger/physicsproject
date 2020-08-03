<template>
  <div id="app" :style="getClass_body">
    <header>
      <md-tabs class="ph-menu" md-sync-route>
        <md-tab id="tab-home" md-label="3800" to="/" exact></md-tab>
        <md-tab
          :md-disabled="this.user.is_token_expired"
          id="tab-add"
          md-icon="add"
          to="/add"
          exact
        ></md-tab>
        <md-tab
          id="tab-latex"
          md-icon="create"
          to="/latex"
          exact
        ></md-tab>
        <md-tab id="tab-about" md-icon="question_answer" to="/about" exact></md-tab>


        <md-tab id="tab-github" md-icon="/github.svg" to="/github"></md-tab>
        <md-tab id="tab-user" md-icon="face" to="/user" exact> </md-tab>
      </md-tabs>

      <div>
        <Message
          v-if="this.isApiOk === false"
          text="Что-то не работает, мы уже чиним"
          severity="error"
        ></Message>
      </div>
    </header>

    <router-view />
  </div>
</template>

<script>
import config from "./config/api.js";
import http_helper from "./lib/http";

const Message = () =>
  import(
    /* webpackChunkName: "components_Message_Message" */ "./components/Message/Message"
  );
const axios = () => import(/* webpackChunkName: "axios" */ "axios");

export default {
  name: "App",
  components: { Message },
  data() {
    return {
      isApiOk: null,
      user: config.defaultUser
    };
  },
  computed: {
    getClass_body() {
      const parse = require("parse-color");
      const toColor = color => {
        if (!color) {
          return {
            rgb: null,
            r: null,
            b: null,
            c: null
          };
        }
        const rgb = parse(color).rgb;
        return {
          rgb: color,
          r: rgb[0],
          g: rgb[1],
          b: rgb[2]
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
      const styles = {};
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
        "--action-background-color",
        this.user.color_background_action
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
      patchWithCssVariables(
        styles,
        "--action-foreground-color",
        this.user.color_foreground_action
      );
      patchWithCssVariables(
        styles,
        "--background-success-color",
        this.user.color_background_success
      );
      patchWithCssVariables(
        styles,
        "--background-warning-color",
        this.user.color_background_warning
      );
      patchWithCssVariables(
        styles,
        "--background-error-color",
        this.user.color_background_error
      );
      patchWithCssVariables(
        styles,
        "--foreground-success-color",
        this.user.color_foreground_success
      );
      patchWithCssVariables(
        styles,
        "--foreground-warning-color",
        this.user.color_foreground_warning
      );
      patchWithCssVariables(
        styles,
        "--foreground-error-color",
        this.user.color_foreground_error
      );
      return styles;
    }
  },
  methods: {
    checkApiOk() {
      axios().then(ax =>
        ax
          .request({
            url: config.apiPrefix + "/health",
            method: "GET"
          })
          .then(
            result => {
              this.isApiOk = result.data.status === "ok";
            },
            error => {
              this.isApiOk = false;
              throw error;
            }
          )
      );
    }
  },
  mounted() {
    this.checkApiOk();
    http_helper
      .getMeAsUser(this.$store.getters.get_jwt)
      .then(user => {
        this.$store.commit("set_user", user);
        this.user = this.$store.getters.get_user;
      })
      .catch(error => throw error);
  }
};
</script>
<style lang="scss">
a.md-button[disabled] {
  cursor: not-allowed;
  opacity: 38%;
}
.md-tabs-navigation a.md-button {
  min-width: 2em;
}
.md-tooltip.md-tooltip-bottom.md-theme-default#isbn_help {
  height: 5em;
}
a {
  color: var(--foreground-secondary-color);
}
.md-button {
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
button.md-button.md-theme-default.md-raised:not([disabled]).md-primary {
  color: var(--action-foreground-color);
  background-color: var(--action-background-color);
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
    a:nth-last-of-type(2) {
      margin-left: auto;
    }
    background-color: var(--background-secondary-color);
    .md-button {
      color: var(--foreground-primary-color);

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

// idk how to fix these transition props once for all so todo
#app,
div.md-card.md-theme-default,
.ph-color-field,
i.md-icon.md-theme-default.md-icon-font {
  transition: background-color 0.5s linear, color 0.5s linear;
}

div.md-card.md-theme-default {
  color: inherit;
  background-color: var(--background-secondary-color);
}
i.md-icon.md-theme-default.md-icon-font {
  color: var(--foreground-secondary-color);
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
    min-width: 1em;
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

  .md-button.md-theme-default {
    i.md-icon.md-theme-default.md-icon-font {
      color: var(--foreground-secondary-color);
    }
  }

  button.md-button.md-theme-default.md-raised:not([disabled]).md-primary {
    color: var(--foreground-action-color);
    background-color: var(--background-action-color);
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
  -webkit-text-fill-color: var(--foreground-success-color);
}

.ph-failure {
  background-color: var(--background-error-color);
  color: var(--foreground-error-color);
  -webkit-text-fill-color: var(--foreground-error-color);
}

.md-menu-content-container {
  height: 25em;
}
</style>
