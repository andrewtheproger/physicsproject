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
        <md-tab id="tab-about" md-label="О проекте" to="/about" exact></md-tab>

        <md-tab id="tab-user" md-icon="face" to="/user" exact> </md-tab>
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
import config from "./config/api";
import http_helper from "./lib/http";

export default {
  name: "App",

  data() {
    return {
      isApiOk: null,
      user: {
        is_token_expired: null,
        color_background_primary: '#252525',
        color_background_secondary: '#555',
        color_foreground_primary: '#ccc',
        color_foreground_secondary: '#ccf'
      }
    };
  },
    computed: {
        getClass_body() {
            const parse = require('parse-color');
            const default_rgb = {
                r: null,
                b: null,
                c: null
            };
            let background_primary_rgb = default_rgb;
            let background_secondary_rgb = default_rgb;
            let foreground_primary_rgb = default_rgb;
            let foreground_secondary_rgb = default_rgb;
            if (this.user.color_background_primary) {
                background_primary_rgb = parse(this.user.color_background_primary).rgb;
            }

            if (this.user.color_background_secondary) {
                background_secondary_rgb = parse(this.user.color_background_secondary).rgb;
            }

            if (this.user.color_foreground_primary) {
                foreground_primary_rgb = parse(this.user.color_foreground_primary).rgb;
            }

            if (this.user.color_foreground_secondary) {
                foreground_secondary_rgb = parse(this.user.color_foreground_secondary).rgb;
            }
            console.log(background_primary_rgb);
            console.log(background_secondary_rgb);
            console.log(foreground_primary_rgb);
            console.log(foreground_secondary_rgb);

            return {
                '--background-primary-color': this.user.color_background_primary,
                '--background-primary-color-r': background_primary_rgb[0],
                '--background-primary-color-g': background_primary_rgb[1],
                '--background-primary-color-b': background_primary_rgb[2],

                '--background-secondary-color': this.user.color_background_secondary,
                '--background-secondary-color-r': background_secondary_rgb[0],
                '--background-secondary-color-g': background_secondary_rgb[1],
                '--background-secondary-color-b': background_secondary_rgb[2],

                '--foreground-primary-color': this.user.color_foreground_primary,
                '--foreground-primary-color-r': foreground_primary_rgb[0],
                '--foreground-primary-color-g': foreground_primary_rgb[1],
                '--foreground-primary-color-b': foreground_primary_rgb[2],

                '--foreground-secondary-color': this.user.color_foreground_secondary,
                '--foreground-secondary-color-r': foreground_secondary_rgb[0],
                '--foreground-secondary-color-g': foreground_secondary_rgb[1],
                '--foreground-secondary-color-b': foreground_secondary_rgb[2],

                '--background-success-color': '#050',
                '--background-warning-color': '#550',
                '--background-error-color': '#500',
                '--foreground-success-color': '#0f0',
                '--foreground-warning-color': '#ff0',
                '--foreground-error-color': '#f00',
            }
        }
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
    http_helper
      .getMeAsUser(this.$store.getters.get_jwt)
      .then(response => this.user = response.data);
  }
};
</script>

<style lang="scss">
@import "config/variables.scss";

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
    fill: var(--foreground-primary-color);;
  }
}

.md-field.md-theme-default label {
  padding-left: 1em;
}
</style>
