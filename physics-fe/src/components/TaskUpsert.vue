<template>
  <div class="ph-task-upsert">
      <form @submit.prevent="onSubmit">
        <md-field>
          <label>Номер задачи...</label>
          <md-input type="text" v-model="number" />
        </md-field>

        <md-field>
          <label for="movie">Isbn...</label>
          <md-select v-model="isbn" name="movie" id="movie">
            <md-option value="fight-club">Fight Club</md-option>
            <md-option value="godfather">Godfather</md-option>
            <md-option value="godfather-ii">Godfather II</md-option>
            <md-option value="godfather-iii">Godfather III</md-option>
            <md-option value="godfellas">Godfellas</md-option>
            <md-option value="pulp-fiction">Pulp Fiction</md-option>
            <md-option value="scarface">Scarface</md-option>
          </md-select>
        </md-field>

        <md-field class="ph-task-upsert-latex">
          <label>LaTeX...</label>
          <md-textarea cols="30" rows="15" v-model="latex"> </md-textarea>

          <div>
            <vue-mathjax :formula="latex"></vue-mathjax>
          </div>
        </md-field>

        <multiple-file-uploader
          class="ph-filelink-input"
          :postURL="url"
          successMessagePath=""
          errorMessagePath=""
        ></multiple-file-uploader>

        <md-field>
          <md-input type="submit" value="Отправить" />
        </md-field>
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
      isbn: null
    };
  },

  components: {
    MultipleFileUploader
  },

  methods: {
    onSubmit() {
      
    }
  }
};
</script>

<style lang="scss" scoped>
@import "../config/variables.scss";

.ph-task-upsert {
  padding: 2em;

  .ph-task-upsert-latex {
    display: flex;

    textarea {
      border-right: 2px dotted $secondary-bg-color;
    }

    textarea, div {
      width: 50%;
    }
  }
}
</style>
