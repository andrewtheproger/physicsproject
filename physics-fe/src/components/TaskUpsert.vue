<template>
  <div class="ph-file-input-wrapper">
    <multiple-file-uploader
      class="ph-filelink-input"
      :postURL="url"
      successMessagePath=""
      errorMessagePath=""
    ></multiple-file-uploader>

  </div>
</template>

<script>
import MultipleFileUploader from "./MultipleFileUploader";
import config from '../config/api.js';

export default {
  name: "User",
  data() {
    return {
      files: null,
      url: `${config.apiPrefix}/images`
    };
  },

  components: {
    MultipleFileUploader,
  },

  methods: {
    onPaste(evt) {
      console.log(evt);
    },
  },
};
</script>

<style lang="scss" scoped>
.ph-file-input-wrapper {
  display: flex;

  input {
    width: 50%;
  }
}
</style>
