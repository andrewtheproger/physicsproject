<template>
  <form class="mfu-uploadBox" role="form" enctype="multipart/form-data" @submit.prevent="onSubmit">
    <div class="mfu-files-input">
      <Dragndrop />
      <LinksImport />
    </div>

    <div class="mfu-buttons-wrapper">
      <md-button
        type="button"
        class="md-raised md-accent"
        @click="removefiles"
        :disabled="files.length === 0 && links.length === 0"
      >
        {{ cancelButtonMessage }}
      </md-button>
      <md-button
        type="submit"
        class="md-raised md-primary"
        :disabled="(files.length < minfiles || files.length > maxfiles) && links.length === 0"
      >
        {{ uploadButtonMessage }}
      </md-button>
    </div>
    <br />
    <div class="mfu-successMsg" v-if="successMsg !== ''">{{ successMsg }}</div>
    <div class="mfu-errorMsg" v-if="errorMsg !== ''">
      {{ fileUploadErrorMessage }}:<br />{{ errorMsg }} <br />{{
        retryErrorMessage
      }}
    </div>
    <div class="mfu-errorMsg" v-if="files.length && files.length < minfiles">
      {{ minFilesErrorMessage }}: {{ minfiles }}. <br />{{
        retryErrorMessage
      }}
    </div>
    <div class="mfu-errorMsg" v-if="files.length && files.length > maxfiles">
      {{ maxFilesErrorMessage }}: {{ maxfiles }}. <br />{{
        retryErrorMessage
      }}
    </div>
  </form>
</template>

<script>
require("es6-promise").polyfill();
import Dragndrop from './Dragndrop';
import LinksImport from './LinksImport'
import axios from "axios";
{
  axios;
}
export default {
  props: {
    postURL: {
      type: String,
      required: true,
    },
    minfiles: {
      type: Number,
      default: 1,
    },
    maxfiles: {
      type: Number,
      default: 30,
    },
    method: {
      type: String,
      default: "post",
    },
    postMeta: {
      type: [String, Array, Object],
      default: "",
    },
    postData: {
      type: [Object],
      default: () => {},
    },
    postHeader: {
      type: [Object],
      default: () => {},
    },
    successMessagePath: {
      type: String,
      required: true,
    },
    errorMessagePath: {
      type: String,
      required: true,
    },
    headerMessage: {
      type: String,
      default: "",
    },
    dropAreaPrimaryMessage: {
      type: String,
      default: "",
    },
    dropAreaSecondaryMessage: {
      type: String,
      default: "",
    },
    fileNameMessage: {
      type: String,
      default: "Имена",
    },
    fileSizeMessage: {
      type: String,
      default: "Длина",
    },
    totalFileMessage: {
      type: String,
      default: "Всего файлов:",
    },
    totalUploadSizeMessage: {
      type: String,
      default: "Всего данных:",
    },
    addMoreFiles: {
      type: String,
      default: "Добавить ещё файл",
    },
    uploadButtonMessage: {
      type: String,
      default: "Загрузить",
    },
    cancelButtonMessage: {
      type: String,
      default: "Отменить",
    },
    fileUploadErrorMessage: {
      type: String,
      default: "Произошла ошибка",
    },
    minFilesErrorMessage: {
      type: String,
      default: "Минимальное количество файлов",
    },
    maxFilesErrorMessage: {
      type: String,
      default: "Максимальное количество файлов",
    },
    retryErrorMessage: {
      type: String,
      default: "Попробуйте снова",
    },
    httpMethodErrorMessage: {
      type: String,
      default:
        "This HTTP method is not allowed. Please use either 'put' or 'post' methods.",
    },
    showHttpMessages: {
      type: Boolean,
      default: true,
    },
  },
  /*
   * The component's data.
   */
  data() {
    return {
      dragging: false,
      files: [],
      filelist: null,
      links: [],
      successMsg: "",
      errorMsg: "",
      isLoaderVisible: false,
    };
  },
  components: {
    Dragndrop,
    LinksImport
  },
  methods: {
    removefiles() {
      this.files = [];
      this.links = [];
      this.dragging = false;
    },
    onSubmit() {
      this.isLoaderVisible = true;

      const formData = new FormData();
      for (let i = 0; i < this.$refs.file.files.length; i++) {
        formData.append(`files[${i}]`, this.$refs.file.files[i]);
      }

      for (let i = 0; i < this.links.length; i++) {
        formData.append(`links[${i}]`, this.links[i]);
      }

      // why do we need separate postMeta and postData?
      const isString = typeof this.postMeta === "string" && this.postMeta !== "";
      const isObject = typeof this.postMeta === "object" && Object.keys(this.postMeta).length > 0
      const isArray = typeof this.postData === "object" &&
                this.postData !== null &&
                Object.keys(this.postData).length > 0

      if (isString || isObject) {
        formData.append("postMeta", this.postMeta);
      }

      if (isArray) {
        for (const key in this.postData) {
          formData.append(key, this.postData[key]);
        }
      }

      if (this.method !== "put" && this.method !== "post") {
        if (this.showHttpMessages) { 
          this.errorMsg = this.httpMethodErrorMessage;
        }

        this.removefiles();

        return;
      }

      axios({
          method: this.method,
          url: this.postURL,
          data: formData,
          headers: this.postHeader,
        })
        .then((response) => {
          this.isLoaderVisible = false;
          
          if (this.showHttpMessages) {
            this.successMsg = response + "." + this.successMessagePath;
          }

          this.removefiles();
        })
        .catch((error) => {
          this.isLoaderVisible = false;
          
          if (this.showHttpMessages) {
            this.errorMsg = error + "." + this.errorMessagePath;
          }

          this.removefiles();
        });
    },
  },
};
</script>

<style lang="scss" scoped>
@import "../../config/variables.scss";

.mfu-buttons-wrapper {
  display: flex;
  flex-direction: row-reverse;

  button {
    width: 10%;
  }
}

.mfu-files-input {
  display: flex;
  align-items: bottom;
}

.mfu-uploadBox {
  background: $secondary-bg-color;
  color: $primary-fg-color;
  width: 100%;
}

</style>
