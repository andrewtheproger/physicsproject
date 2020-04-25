<template>
  <div class="ph-task-upsert">
    <form class="ph-form" @submit.prevent="onSubmit">
      <div class="ph-params-wrapper">
        <md-field>
          <label>Номер задачи через точку...</label>
          <md-input type="text" v-model="number" />

          <span>
            <md-icon>help_outline</md-icon>

            <md-tooltip id="number_help">Например, "2.27"</md-tooltip>
          </span>
        </md-field>

        <md-field>
          <label for="movie">Isbn 3800...</label>
          <md-select v-model="isbn" name="movie" id="movie">
            <md-option value="fight-club">Fight Club</md-option>
            <md-option value="godfather">Godfather</md-option>
            <md-option value="godfather-ii">Godfather II</md-option>
            <md-option value="godfather-iii">Godfather III</md-option>
            <md-option value="godfellas">Godfellas</md-option>
            <md-option value="pulp-fiction">Pulp Fiction</md-option>
            <md-option value="scarface">Scarface</md-option>
          </md-select>

          <span>
            <md-icon>help_outline</md-icon>

            <md-tooltip id="isbn_help">ISBN - это уникальный номер книги из 11 или 13 символов. <br /> Найти его можно на первых или на последних страницах книги.</md-tooltip>
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
        @files_uploaded="files_uploaded"
        successMessagePath=""
        errorMessagePath=""
      ></multiple-file-uploader>

      <div class="ph-task-upsert-submit-controls">
        <md-button
          type="submit"
          class="md-raised md-primary">
          Добавить
        </md-button>
      </div>
    </form>
  </div>
</template>

<script>
import MultipleFileUploader from "./MultipleFileUploader/MultipleFileUploader";
import config from "../config/api.js";

export default {
  name: "User",
  data() {
    return {
      latex: "Привет, это текст на $ \\LaTeX $, да. ",
      url: `${config.apiPrefix}/images`,
      number: null,
      isbn: null,
      images_ids: []
    };
  },

  components: {
    MultipleFileUploader
  },

  methods: {
    onSubmit() {},
    files_uploaded($event) {
      this.images_ids = $event.data.ids;
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
