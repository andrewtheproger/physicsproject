<template>
  <div class="ph-task-upsert">
    <form class="ph-form" @submit.prevent="onSubmit">
      <div class="ph-params-wrapper">
        <md-field :class="getValidationClass('number')">
          <label>Номер задачи...</label>

          <md-input
            type="text"
            @change="onNumberChange"
            v-model.trim="form.number"
            name="form-number"
            id="form-number"
          />
          <span class="md-error" v-if="!$v.form.number.required"
            >У задачи должен быть номер</span
          >
          <span class="md-error" v-if="!$v.form.number.mustBeTaskNumber"
            >Номер задачи должен быть записан через точку</span
          >
          <span class="md-error" v-if="!$v.form.number.mustBeUniqueNumber"
            >Такая задача уже есть</span
          >

          <span>
            <md-icon>help_outline</md-icon>

            <md-tooltip id="number_help">Например, "2.27"</md-tooltip>
          </span>
        </md-field>
      </div>

      <md-field
        :class="getValidationClass('latex')"
        class="ph-task-upsert-latex"
      >
        <label>LaTeX...</label>
        <md-textarea
          cols="30"
          rows="15"
          v-model.trim="form.latex"
          name="form-latex"
          id="form-latex"
        >
        </md-textarea>

        <span class="md-error" v-if="!$v.form.latex.required"
          >Задача должна иметь условие</span
        >
        <span class="md-error" v-if="!$v.form.latex.mustSeemOk"
          >В задаче из 3800 не может идти речь про LaTeX</span
        >

        <div>
          <vue-mathjax
            class="ph-mathjax"
            :formula="this.form.latex"
          ></vue-mathjax>
        </div>
      </md-field>

      <multiple-file-uploader
        class="ph-filelink-input"
        :postURL="url"
        ref="multipleFileUploader"
        successMessagePath=""
        errorMessagePath=""
      ></multiple-file-uploader>

      <md-progress-bar
        md-mode="indeterminate"
        v-if="this.isLoading"
      ></md-progress-bar>

      <div class="ph-task-upsert-submit-controls">
        <md-button
          type="submit"
          class="md-raised md-primary "
          :disabled="this.isLoading"
          style = "background-color: var(--background-secondary-color)"
        >
          Добавить
        </md-button>

        <div class="ph-success" v-if="isFlowFailed === false">
          Задача добавлена, спасибо
        </div>

        <div class="ph-failure" v-if="flowFailed">
          {{
            this.flowFailed.http_code
              ? "Произошла ошибка на стороне сервера"
              : "Вы ошиблись"
          }}: {{ this.flowFailed.message }}
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import MultipleFileUploader from "./MultipleFileUploader/MultipleFileUploader";
import config from "../config/api.js";
import axios from "axios";
{
  axios;
}
import { required } from "vuelidate/lib/validators";
import { validationMixin } from "vuelidate";
import http_helper from "../lib/http";

export default {
  name: "User",
  mixins: [validationMixin],
  data() {
    return {
      form: {
        latex: "Привет, это текст на $ \\LaTeX $, да. ",
        number: null,
        isbn: null,
      },
      url: `${config.apiPrefix}/images`,
      isLoading: false,
      existing_numbers: [],
      isFlowFailed: null,
      flowFailed: null,
    };
  },
  validations: {
    form: {
      latex: {
        required,
        mustSeemOk(v) {
          if (v) {
            return !v.includes("LaTeX");
          }

          return true;
        },
      },
      number: {
        required,
        mustBeTaskNumber(v) {
          if (v) {
            return !!v.match(/\d+[., ]\d+/);
          }

          return true;
        },
        mustBeUniqueNumber(v) {
          if (v) {
            return !this.existing_numbers.includes(v);
          }

          return true;
        },
      },
    },
  },
  components: {
    MultipleFileUploader,
  },
  created() {
    const url = config.apiPrefix + "/tasks/predicate_numbers";

    axios({
      url: url,
      method: "GET",
    }).then(
      (result) => {
        this.existing_numbers = result.data.map(
          (x) => x.base_number + "." + x.task_number
        );
      },
      (error) => {
        console.log(error);
      }
    );
  },
  methods: {
    onNumberChange() {
      if (!this.form.number.includes(".")) {
        this.form.number = this.form.number
          .replace(",", ".")
          .replace(" ", ".")
          .replace("-", ".");
      }

      this.$v.$touch();
    },

    getValidationClass(fieldName) {
      const field = this.$v.form[fieldName];

      if (field) {
        return {
          "md-invalid": field.$invalid && field.$dirty,
        };
      }
    },

    reset() {
      this.form.latex = "";
      this.form.number = null;
      this.form.isbn = null;
      this.$v.$reset();
    },
    onSubmit() {
      this.isLoading = true;
      this.$v.$touch();

      if (this.$v.$invalid) {
        this.isLoading = false;
        return;
      }

      this.$refs.multipleFileUploader
        .onSubmit()
        .then((result) => {
          if (result.status !== 200) {
            throw new TypeError("General error");
          }

          this.send(result.data.ids)
            .then((result) => {
              this.loadStatus = result.status;
              this.isLoading = false;
              this.isFlowFailed = false;
              this.existing_numbers = [
                ...this.existing_numbers,
                this.form.number,
              ];
              this.reset();
            })
            .catch((error) => {
              this.isFlowFailed = true;

              const data = error.response.data;

              this.flowFailed = {
                http_code: error.response.code,
                internal_code: data.code,
                message: http_helper.get_error_message(data.code),
              };

              this.isLoading = false;
            });
        })
        .catch((error) => {
          this.isFlowFailed = true;

          const data = error.response.data;

          this.flowFailed = {
            http_code: error.response.code,
            internal_code: data.code,
            message: http_helper.get_error_message(data.code),
          };

          this.isLoading = false;
        });
    },
    send(images_ids) {
      const numbers = this.form.number.split(".");
      const base_number = numbers[0];
      const task_number = numbers[1];

      return axios({
        url: `${config.apiPrefix}/tasks`,
        method: "POST",
        data: {
          base_number: base_number,
          task_number: task_number,
          body: {
            latex: this.form.latex,
            image_ids: images_ids,
          },
        },
        headers: {
          Authorization: this.$store.getters.get_jwt,
        },
      })
        .then(function(response) {
          return response;
        })
        .catch(function(error) {
          console.log(error);
        });
    },
  },
};
</script>

<style lang="scss">
.md-tooltip.md-tooltip-bottom.md-theme-default#isbn_help {
  height: 5em;
}
</style>

<style lang="scss" scoped>
@import "../config/variables.scss";

.ph-task-upsert {
  padding: 2em;

  div.md-field.md-theme-default {
    &.md-invalid .md-error {
      -webkit-text-fill-color: var(--foreground-error-color);
      color: var(--foreground-error-color);
    }

    label.ph-task-exists {
      -webkit-text-fill-color: var(--foreground-error-color);
    }

    label.ph-task-not-exists {
      -webkit-text-fill-color: var(--foreground-success-color);
    }
  }

  .ph-form {
    display: flex;
    flex-wrap: wrap;

    .md-field {
      width: 100%;
    }

    .ph-params-wrapper {
      display: flex;
      flex-wrap: wrap;
      width: 100%;

      .md-field {
        margin-left: 1em;
        margin-right: 1em;

        width: 100%;

        @media (min-width: 756px) {
          width: 46%;
        }
      }
    }
  }

  .ph-task-upsert-submit-controls {
    display: flex;
    width: 100%;
    flex-direction: row-reverse;
    align-items: baseline;
  }

  .ph-task-upsert-latex {
    display: flex;
    flex-direction: column;

    textarea {
      border-right: none;
      border-bottom: 2px dotted var(--background-secondary-color);
    }

    textarea,
    div {
      width: 100%;
    }

    div {
      display: block;
      padding: 1em;
      height: 10em;
      width: 100%;

      overflow: overlay;
    }
  }

  @media (min-width: 756px) {
    .ph-task-upsert-latex {
      display: flex;
      flex-direction: row;

      textarea.md-textarea {
        border-right: 2px dotted var(--background-secondary-color);
        border-bottom: none;
      }

      textarea,
      div {
        width: 50%;
      }

      div {
        display: inline;
        padding: 1em;
      }
    }
  }
}
</style>
