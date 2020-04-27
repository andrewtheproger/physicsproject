<template>
  <div class="ph-task-upsert">
    <form class="ph-form" @submit.prevent="onSubmit">
      <div class="ph-params-wrapper">
        <md-field>
          <label>Номер задачи...</label>
          <md-input type="text" @change="onNumberChange" v-model="number" />

          <span>
            <md-icon>help_outline</md-icon>

            <md-tooltip id="number_help">Например, "2.27"</md-tooltip>
          </span>
        </md-field>
      </div>

      <md-field class="ph-task-upsert-latex">
        <label>LaTeX...</label>
        <md-textarea cols="30" rows="15" v-model="latex"> </md-textarea>

        <div>
          <vue-mathjax class="ph-mathjax" :formula="latex"></vue-mathjax>
        </div>
      </md-field>

      <multiple-file-uploader
        class="ph-filelink-input"
        :postURL="url"
        ref="multipleFileUploader"
        successMessagePath=""
        errorMessagePath=""
      ></multiple-file-uploader>

      <md-progress-bar md-mode="indeterminate" v-if="this.isLoading"></md-progress-bar>

      <div class="ph-task-upsert-submit-controls">
        <md-button
          type="submit"
          class="md-raised md-primary"
          :disabled="this.isLoading">
          Добавить
        </md-button>

        <div class="ph-success" v-if="loadStatus == 200">
          Задача добавлена, спасибо
        </div>

        <div class="ph-failure" v-if="loadStatus && loadStatus != 200">
          Задача не была добавлена из-за ошибки сервера
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
export default {
  name: "User",
  data() {
    return {
      latex: "Привет, это текст на $ \\LaTeX $, да. ",
      url: `${config.apiPrefix}/images`,
      number: null,
      isbn: null,
      isLoading: false,
      loadStatus: null
    };
  },

  components: {
    MultipleFileUploader
  },

  methods: {
    onNumberChange() {
      if (this.number.includes('.')) {
        return;
      }

      this.number = this.number.replace(',', '.').replace(' ', '.').replace('-', '.')
    },
    reset() {
      this.latex = "";
      this.number = null;
      this.isbn = null;
    },
    onSubmit() {
      this.isLoading = true;
      this.$refs.multipleFileUploader.onSubmit()
        .then(result => {
          if (result.status != 200) {
            throw "General error";
          }

          this.send(result.data.ids)
            .then(result => {
              this.loadStatus = result.status;
              this.isLoading = false;
              this.reset();
            })
            .catch(error => {
              console.log(error);
              this.loadStatus = "General error";
              this.isLoading = false;    
            })
        })
        .catch(error => {
          console.log(error);
          this.loadStatus = "General error";
          this.isLoading = false;
        })
    },
    send(images_ids) {
      const numbers = this.number.split('.')
      const base_number = numbers[0];
      const task_number = numbers[1];

      return axios.post(`${config.apiPrefix}/tasks`, {
        base_number: base_number,
        task_number: task_number,
        body: {
          latex: this.latex,
          image_ids: images_ids
        }
      })
      .then(function (response) {
        return response;
      })
      .catch(function (error) {
        console.log(error);
      });
    }
  }
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

    .ph-success {
      color: green;
    }

    .ph-failure {
      color: red;
    }
  }

  .ph-task-upsert-latex {
    display: flex;
    flex-direction: column;

    textarea {
      border-right: none;
      border-bottom: 2px dotted $secondary-bg-color;
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

      textarea {
        border-right: 2px dotted $secondary-bg-color;
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
