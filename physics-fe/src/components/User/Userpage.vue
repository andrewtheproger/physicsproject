<template>
  <div class="ph-userpage">
    <div class="ph-failure" v-if="flowFailed">
      {{
        this.flowFailed.http_code
          ? "Произошла ошибка на стороне сервера"
          : "Вы ошиблись"
      }}: {{ this.flowFailed.message }}
    </div>

    <md-progress-bar
      md-mode="indeterminate"
      v-if="this.isLoading"
    ></md-progress-bar>

    <md-card>
      <md-card-header>
        <span class="md-title">Вы</span>

        <md-checkbox v-if="user.isAdmin" v-model="user.isAdmin" disabled>
          Админ
        </md-checkbox>
      </md-card-header>

      <span class="ph-registration-date">
        Дата регистрации: {{ this.formatDate(this.user.created_date) }}
      </span>

      <md-card-actions>
        <Logout></Logout>
      </md-card-actions>

      <md-card-content>
        <div class="ph-main-info md-layout-item md-small-size-100">
          <md-field>
            <label>Почта</label>
            <md-input
              name="form-email"
              id="form-email"
              autocomplete="given-name"
              v-model="user.email"
              :disabled="true"
            />
          </md-field>

          <md-field>
            <label for="color-schema-select"
              >Изменить цветовую схему на...</label
            >
            <md-select
              v-model="colorSchema"
              name="color-schema-select"
              id="color-schema-select"
              @md-selected="setColorSchema"
            >
              <md-option value="dark">...тёмную</md-option>
              <md-option value="light">...светлую</md-option>
            </md-select>
          </md-field>
        </div>

        <form class="ph-color-fields" @submit.prevent="onSubmit">
          <color-field
            @color_changed="color_changed"
            @color_changing="color_changing"
            @reset="reset"
            id="background_primary"
            title="Главный цвет фона"
            :value="this.user.color_background_primary"
          ></color-field>
          <color-field
            @color_changed="color_changed"
            @color_changing="color_changing"
            @reset="reset"
            id="background_secondary"
            title="Дополнительный цвет фона"
            :value="this.user.color_background_secondary"
          ></color-field>
          <color-field
            @color_changed="color_changed"
            @color_changing="color_changing"
            @reset="reset"
            id="action_background"
            title="Цвет фона кнопки действия"
            :value="this.user.color_background_action"
          ></color-field>
          <color-field
            @color_changed="color_changed"
            @color_changing="color_changing"
            @reset="reset"
            id="foreground_primary"
            title="Главный цвет шрифта"
            :value="this.user.color_foreground_primary"
          ></color-field>
          <color-field
            @color_changed="color_changed"
            @color_changing="color_changing"
            @reset="reset"
            id="foreground_secondary"
            title="Дополнительный цвет шрифта"
            :value="this.user.color_foreground_secondary"
          ></color-field>
          <color-field
            @color_changed="color_changed"
            @color_changing="color_changing"
            @reset="reset"
            id="action_foreground"
            title="Цвет шрифта кнопки действия"
            :value="this.user.color_foreground_action"
          ></color-field>

          <Message text="Пример успешного результата" severity="success" />
          <Message text="Пример предупреждения" severity="warning" />
          <Message text="Пример ошибки" severity="error" />

          <color-field
            @color_changed="color_changed"
            @color_changing="color_changing"
            @reset="reset"
            id="background_success"
            title="Цвет фона успешного результата"
            :value="this.user.color_background_success"
          ></color-field>
          <color-field
            @color_changed="color_changed"
            @color_changing="color_changing"
            @reset="reset"
            id="background_warning"
            title="Цвет фона предупреждения"
            :value="this.user.color_background_warning"
          ></color-field>
          <color-field
            @color_changed="color_changed"
            @color_changing="color_changing"
            @reset="reset"
            id="background_error"
            title="Цвет фона ошибки"
            :value="this.user.color_background_error"
          ></color-field>
          <color-field
            @color_changed="color_changed"
            @color_changing="color_changing"
            @reset="reset"
            id="foreground_success"
            title="Цвет шрифта успешного результата"
            :value="this.user.color_foreground_success"
          ></color-field>
          <color-field
            @color_changed="color_changed"
            @color_changing="color_changing"
            @reset="reset"
            id="foreground_warning"
            title="Цвет шрифта предупреждения"
            :value="this.user.color_foreground_warning"
          ></color-field>
          <color-field
            @color_changed="color_changed"
            @color_changing="color_changing"
            @reset="reset"
            id="foreground_error"
            title="Цвет шрифта ошибки"
            :value="this.user.color_foreground_error"
          ></color-field>
          <div class="ph-user-submit-controls">
            <md-progress-spinner
              v-if="!allowSubmit"
              md-mode="indeterminate"
              :md-diameter="30"
            >
            </md-progress-spinner>

            <md-snackbar
              md-position="center"
              :md-duration="700"
              :md-active="!allowSubmit && !isFlowFailed"
              md-persistent
            >
              <Message text="Изменения сохранены" severity="success"></Message>
            </md-snackbar>
            <md-snackbar
              md-position="center"
              :md-duration="2000"
              :md-active="!allowSubmit && isFlowFailed"
              md-persistent
            >
              <Message
                text="Произошла ошибка, и изменения не сохранились"
                severity="error"
              ></Message>
            </md-snackbar>
          </div>
        </form>
      </md-card-content>
    </md-card>
  </div>
</template>

<script>
import Message from "../Message/Message";
import Color_Field from "./Color_Field";
import config from "../../config/api.js";
import colorSchema from "../../config/colorSchema";

const axios = () => import(/* webpackChunkName: "axios" */ "axios");
const Logout = () =>
  import(/* webpackChunkName: "components_Logout" */ "./Logout");

export default {
  name: "Userpage",
  components: {
    Logout,
    Message,
    "color-field": Color_Field
  },
  data() {
    return {
      isLoading: false,
      isFlowFailed: null,
      flowFailed: null,
      colorSchema: null,
      allowSubmit: true // todo to dict [child_id, locks_count]
    };
  },
  computed: {
    user() {
      return this.$store.getters.get_user;
    }
  },
  methods: {
    setColorSchema(e) {
      switch (e) {
        case "dark":
          this.user.color_background_primary =
            colorSchema.dark.color_background_primary;
          this.user.color_background_secondary =
            colorSchema.dark.color_background_secondary;
          this.user.color_background_action =
            colorSchema.dark.color_background_action;
          this.user.color_foreground_primary =
            colorSchema.dark.color_foreground_primary;
          this.user.color_foreground_secondary =
            colorSchema.dark.color_foreground_secondary;
          this.user.color_foreground_action =
            colorSchema.dark.color_foreground_action;
          this.user.color_background_success =
            colorSchema.dark.color_background_success;
          this.user.color_background_warning =
            colorSchema.dark.color_background_warning;
          this.user.color_background_error =
            colorSchema.dark.color_background_error;
          this.user.color_foreground_success =
            colorSchema.dark.color_foreground_success;
          this.user.color_foreground_warning =
            colorSchema.dark.color_foreground_warning;
          this.user.color_foreground_error =
            colorSchema.dark.color_foreground_error;
          break;
        case "light":
          this.user.color_background_primary =
            colorSchema.light.color_background_primary;
          this.user.color_background_secondary =
            colorSchema.light.color_background_secondary;
          this.user.color_background_action =
            colorSchema.light.color_background_action;
          this.user.color_foreground_primary =
            colorSchema.light.color_foreground_primary;
          this.user.color_foreground_secondary =
            colorSchema.light.color_foreground_secondary;
          this.user.color_foreground_action =
            colorSchema.light.color_foreground_action;
          this.user.color_background_success =
            colorSchema.light.color_background_success;
          this.user.color_background_warning =
            colorSchema.light.color_background_warning;
          this.user.color_background_error =
            colorSchema.light.color_background_error;
          this.user.color_foreground_success =
            colorSchema.light.color_foreground_success;
          this.user.color_foreground_warning =
            colorSchema.light.color_foreground_warning;
          this.user.color_foreground_error =
            colorSchema.light.color_foreground_error;
          break;
        default:
          break;
      }

      this.onSubmit();
    },
    formatDate(timestamp) {
      const date = new Date(timestamp);

      return date.toLocaleDateString("ru-RU", config.datetime_format);
    },
    reset(id) {
      switch (id) {
        case "background_primary":
          this.user.color_background_primary =
            config.defaultUser.color_background_primary;
          break;
        case "background_secondary":
          this.user.color_background_secondary =
            config.defaultUser.color_background_secondary;
          break;
        case "action_background":
          this.user.color_background_action =
            config.defaultUser.color_background_action;
          break;
        case "foreground_primary":
          this.user.color_foreground_primary =
            config.defaultUser.color_foreground_primary;
          break;
        case "foreground_secondary":
          this.user.color_foreground_secondary =
            config.defaultUser.color_foreground_secondary;
          break;
        case "action_foreground":
          this.user.color_foreground_action =
            config.defaultUser.color_foreground_action;
          break;
        case "background_success":
          this.user.color_background_success =
            config.defaultUser.color_background_success;
          break;
        case "background_warning":
          this.user.color_background_warning =
            config.defaultUser.color_background_warning;
          break;
        case "background_error":
          this.user.color_background_error =
            config.defaultUser.color_background_error;
          break;
        case "foreground_success":
          this.user.color_foreground_success =
            config.defaultUser.color_foreground_success;
          break;
        case "foreground_warning":
          this.user.color_foreground_warning =
            config.defaultUser.color_foreground_warning;
          break;
        case "foreground_error":
          this.user.color_foreground_error =
            config.defaultUser.color_foreground_error;
          break;
        default:
          throw "This should not happens";
      }

      this.onSubmit();
    },
    color_changing() {
      this.allowSubmit = false;
    },
    color_changed({ id, hex }) {
      switch (id) {
        case "background_primary":
          this.user.color_background_primary = hex;
          break;
        case "background_secondary":
          this.user.color_background_secondary = hex;
          break;
        case "action_background":
          this.user.color_background_action = hex;
          break;
        case "foreground_primary":
          this.user.color_foreground_primary = hex;
          break;
        case "foreground_secondary":
          this.user.color_foreground_secondary = hex;
          break;
        case "action_foreground":
          this.user.color_foreground_action = hex;
          break;
        case "background_success":
          this.user.color_background_success = hex;
          break;
        case "background_warning":
          this.user.color_background_warning = hex;
          break;
        case "background_error":
          this.user.color_background_error = hex;
          break;
        case "foreground_success":
          this.user.color_foreground_success = hex;
          break;
        case "foreground_warning":
          this.user.color_foreground_warning = hex;
          break;
        case "foreground_error":
          this.user.color_foreground_error = hex;
          break;
        default:
          throw "This should not happens";
      }

      this.allowSubmit = true;
      this.onSubmit();
    },
    onSubmit() {
      const url = config.apiPrefix + "/users/me";
      this.isLoading = true;
      this.allowSubmit = false;

      axios().then(ax =>
        ax
          .request({
            url: url,
            method: "POST",
            data: {
              color_background_primary: this.user.color_background_primary,
              color_background_secondary: this.user.color_background_secondary,
              color_background_action: this.user.color_background_action,
              color_foreground_primary: this.user.color_foreground_primary,
              color_foreground_secondary: this.user.color_foreground_secondary,
              color_foreground_action: this.user.color_foreground_action,
              color_background_success: this.user.color_background_success,
              color_background_warning: this.user.color_background_warning,
              color_background_error: this.user.color_background_error,
              color_foreground_success: this.user.color_foreground_success,
              color_foreground_warning: this.user.color_foreground_warning,
              color_foreground_error: this.user.color_foreground_error
            },
            headers: {
              Authorization: this.$store.getters.get_jwt
            }
          })
          .then(
            () => {
              this.isLoading = false;
              this.isFlowFailed = false;
              this.flowFailed = null;
              this.allowSubmit = true;
            },
            error => {
              this.isLoading = false;
              this.isFlowFailed = true;
              this.flowFailed = null; // todo
              this.allowSubmit = true;

              throw error;
            }
          )
      );
    }
  }
};
</script>

<style lang="scss" scoped>
.md-snackbar.md-theme-default {
  .md-snackbar-content {
    background-color: inherit;
    color: inherit;
  }
}

.md-card-header {
  display: flex;

  .md-checkbox {
    margin-left: 3em;
  }
}

.ph-user-submit-controls {
  display: flex;
  width: 100%;
  flex-direction: row-reverse;
  align-items: baseline;
}

.md-card-content {
  display: flex;
  flex-direction: column;

  .ph-main-info {
    display: flex;

    @media (max-width: 1024px) {
      flex-direction: column;
    }

    .md-field {
      @media (min-width: 1024px) {
        margin: 0 1em;
      }
    }
  }
}

.ph-color-fields {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;

  .ph-message,
  .ph-color-field {
    width: 30%;
    @media (max-width: 1024px) {
      width: 100%;
    }
  }
}

.md-checkbox {
  display: flex;
}

.ph-userpage {
  display: flex;
  align-items: center;
  justify-content: center;
}

.md-card {
  width: 70%;
}

.ph-registration-date {
  margin-left: 1em;
}
</style>
