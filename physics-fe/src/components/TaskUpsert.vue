<template>
  <div class="ph-file-input-wrapper">
      <form>
        <md-field>
          <label>Номер задачи...</label>
          <md-input type="text" v-model="number" />
        </md-field>

        <md-field>
          <label>LaTeX...</label>
          <md-textarea cols="30" rows="15" v-model="latex"> </md-textarea
        ></md-field>

        <md-field>
          <md-input type="submit" value="Отправить" />
        </md-field>

        <multiple-file-uploader
          class="ph-filelink-input"
          :postURL="url"
          successMessagePath=""
          errorMessagePath=""
        ></multiple-file-uploader>
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
      files: null,
      url: `${config.apiPrefix}/images`
    };
  },

  components: {
    MultipleFileUploader
  },

  methods: {
    onPaste(evt) {
      console.log(evt);
    }
  }
};
</script>

<style lang="scss" scoped>
@import "../config/variables.scss";

.ph-file-input-wrapper {
  display: flex;

  input {
    width: 50%;
  }
}
</style>
