<template>
  <div class="ph-task-upsert">
    <form class="ph-form" @submit.prevent="onSubmit">
      <div class="ph-params-wrapper">
        <md-field :class="getValidationClass('number')">
          <label>Номер задачи...</label>

          <md-input
            type="text"
            @change="onFormChange"
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

      <h4 class="ph-task-body-header">Условие</h4>
      <md-field
        :class="getValidationClass('latex')"
        class="ph-task-upsert-latex"
      >
        <Latex
          @onLatexChange="this.onTaskChange"
          localStorageKey="ph-3800-latex-task"
          :initial_latex="form.latex"
          :created_date="form.created_date"/>

          <span class="md-error" v-if="!$v.form.latex.required">
            Задача должна иметь условие
          </span>
      </md-field>

      <div class="ph-task-additional-data">
        <div class="ph-task-answer">
          <h4>Ответ</h4>

          <Latex
            @onLatexChange="this.onAnswerChange"
            localStorageKey="ph-3800-latex-answer"
            :initial_latex="form.answer"
            :created_date="form.answer_created_date"/>
        </div>

        <div class="ph-task-images">
          <h4>Иллюстрации</h4>

          <multiple-file-uploader
            class="ph-filelink-input"
            :postURL="url"
            ref="multipleFileUploader"
            successMessagePath=""
            errorMessagePath=""
            :links="this.form.images.map(x => x.url)"
          ></multiple-file-uploader>
        </div>
      </div>

      <md-progress-bar
        md-mode="indeterminate"
        v-if="this.isLoading"
      ></md-progress-bar>

      <div v-if="!this.$route.params.id" class="ph-task-upsert-submit-controls">
        <md-button
          type="submit"
          class="md-raised md-primary "
          :disabled="this.isLoading"
        >
          Добавить
        </md-button>

        <md-snackbar
          md-position="center"
          :md-duration="700"
          :md-active.sync="this.isFlowFailed === false"
          md-persistent
        >
          <Message
            v-if="!this.isFlowFailed"
            text="Задача добавлена, спасибо"
            severity="success"
          ></Message>
        </md-snackbar>

        <md-snackbar
          md-position="center"
          :md-duration="700"
          :md-active.sync="this.isFlowFailed === true"
          md-persistent
        >
          <Message
            v-if="this.isFlowFailed"
            :text="
              (this.flowFailed.http_code
                ? 'Произошла ошибка на стороне сервера'
                : 'Вы ошиблись') +
                ' : ' +
                this.flowFailed.message
            "
            severity="success"
          ></Message>
        </md-snackbar>

        <div class="ph-failure" v-if="isFlowFailed === true"></div>
      </div>

      <div v-if="this.$route.params.id" class="ph-task-upsert-submit-controls">
        <md-button
          type="submit"
          class="md-raised md-primary"
          :disabled="this.isLoading"
        >
          Сохранить
        </md-button>

        <md-button
          type="button"
          @click="remove"
          class="md-raised md-accent"
          :disabled="this.isLoading"
        >
          Удалить
        </md-button>

        <div class="ph-success" v-if="isFlowFailed === false">
          Успешно
        </div>

        <div class="ph-failure" v-if="isFlowFailed === true">
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
import Latex from "./Latex";
import { required } from "vuelidate/lib/validators";
import { validationMixin } from "vuelidate";
import config from "../config/api.js";
import http_helper from "../lib/http";

const Message = () =>
  import(
    /* webpackChunkName: "components_Message_Message" */ "./Message/Message"
  );
const axios = () => import(/* webpackChunkName: "axios" */ "axios");

export default {
  name: "User",
  mixins: [validationMixin],
  data() {
    return {
      form: {
        latex: "Привет, это текст на $ \\LaTeX $, да. ",
        answer: "",
        answer_created_date: null,
        created_date: null,
        number: null,
        isbn: null,
        images: []
      },
      url: `${config.apiPrefix}/images`,
      originalData: {}, // cached task from server
      isLoading: false,
      id: null,
      existing_numbers: [],
      isFlowFailed: null,
      flowFailed: null
    };
  },
  validations: {
    form: {
      latex: {
        required
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
            const isEditingSameTask =
              v ===
              `${this.originalData.base_number}.${this.originalData.task_number}`;
            const isCreatingNewTask = !this.existing_numbers.includes(v);

            return isEditingSameTask || isCreatingNewTask;
          }

          return true;
        }
      }
    }
  },
  components: {
    MultipleFileUploader,
    Latex,
    Message
  },
  watch: {
    $route() {
      this.init();
    }
  },
  mounted() {
    this.init();
  },
  methods: {
    onAnswerChange(newLatex) {
      this.form.answer = newLatex;
    },
    onTaskChange(newLatex) {
      this.form.latex = newLatex;
    },
    restoreLatex(localStorageKey) {
      const s = localStorage.getItem(localStorageKey);

      if (s) {
        console.log(`found ${s}`)
        return JSON.parse(s);
      } else {
        return { latex: 'Сохранённой версии $ \\LaTeX $ не найдено', created_date: null  }
      }
    },
    onFormChange() {
      if (!this.form) {
        return;
      }

      if (this.form.number) {
        if (!this.form.number.includes(".")) {
          this.form.number = this.form.number
            .replace(",", ".")
            .replace(" ", ".")
            .replace("-", ".");
        }
      }

      this.$v.$touch();
    },
    remove() {
      const url = config.apiPrefix + "/tasks/" + this.$route.params.id;
      this.isLoading = true;
      this.isFlowFailed = null;

      return axios().then(ax =>
        ax
          .request({
            url: url,
            method: "DELETE",
            headers: {
              Authorization: this.$store.getters.get_jwt
            }
          })
          .then(
            () => {
              this.isLoading = false;
              this.isFlowFailed = false;
            },
            error => {
              console.log(error);

              this.isLoading = false;
              this.isFlowFailed = true;
            }
          )
      );
    },
    init() {
      http_helper
        .predicate_numbers()
        .then(numbers => {
          if (!numbers || !numbers.length) {
            this.existing_numbers = [];
            return;
          }

          this.existing_numbers = numbers.map(
            x => x.base_number + "." + x.task_number
          );
        })
        .catch(error => console.log(error));

      if (this.$route.params.id) {
        const url = config.apiPrefix + "/tasks/" + this.$route.params.id;

        return axios().then(ax =>
          ax
            .request({
              url: url,
              method: "GET"
            })
            .then(
              result => {
                const data = result.data;

                this.originalData = data;
                this.form = {
                  latex: data.body.latex,
                  answer: data.body.answer,
                  number: `${data.base_number}.${data.task_number}`,
                  images: data.body.images,
                }
              },
              error => {
                console.log(error);
              }
            )
        );
      } else {
        this.form.latex = "Привет, это текст на $ \\LaTeX $, да";
        this.form.number = null;
        this.form.answer = "";
        this.form.images = [];
      }
    },
    getValidationClass(fieldName) {
      const field = this.$v.form[fieldName];

      if (field) {
        return {
          "md-invalid": field.$invalid && field.$dirty
        };
      }
    },

    reset() {
      this.form.latex = "";
      this.form.answer = "";
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

      this.$refs.multipleFileUploader.onSubmit().then(result => {
        if (result.status !== 200) {
          throw new TypeError("General error");
        }

        this.send(result.data.ids)
          .then(() => {
            this.isLoading = false;
            this.isFlowFailed = false;
            this.existing_numbers = [
              ...this.existing_numbers,
              this.form.number
            ];
            this.reset();
          })
          .catch(error => this.handleError(error));
      });
    },
    send(images_ids) {
      const numbers = this.form.number.split(".");
      const base_number = numbers[0];
      const task_number = numbers[1];
      const id = this.$route.params.id
        ? parseInt(this.$route.params.id)
        : undefined;

      return axios().then(ax =>
        ax
          .request({
            url: `${config.apiPrefix}/tasks`,
            method: "POST",
            data: {
              id: id,
              base_number: base_number,
              task_number: task_number,
              body: {
                answer: this.form.answer,
                latex: this.form.latex,
                image_ids: images_ids
              }
            },
            headers: {
              Authorization: this.$store.getters.get_jwt
            }
          })
          .then(response => response)
          .catch(error => this.handleError(error))
      );
    },
    handleError(error) {
      this.isFlowFailed = true;

      const data = error.response.data;

      this.flowFailed = {
        http_code: error.response.status,
        internal_code: data.code,
        message: http_helper.get_error_message(data.code)
      };

      this.isLoading = false;

      throw error;
    }
  }
};
</script>

<style lang="scss" scoped>
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
  }

  @media (min-width: 756px) {
    .ph-task-upsert-latex {
      display: flex;
      flex-direction: row;
    }
  }

  .ph-task-additional-data {
    display: flex;
    width: 100%;
  }

  .ph-task-answer,
  .ph-task-images {
    width: 100%;
  }

  .ph-task-answer {
    h4 {
      margin-left: 1em;
    }
  }

  .ph-task-body-header {
    margin-left: 1em;
  }
}
</style>
