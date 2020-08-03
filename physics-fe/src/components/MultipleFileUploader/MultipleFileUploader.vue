<template>
  <div class="mfu-uploadBox" role="form" enctype="multipart/form-data">
    <div class="mfu-files-input">
      <Dragndrop
        :files="this.files"
        @file_added="file_added"
        @file_removed="file_removed"
      />

<!--      <LinksImport-->
<!--        :links="this.links"-->
<!--        @link_added="link_added"-->
<!--        @link_removed="link_removed"-->
<!--      />-->
    </div>
  </div>
</template>

<script>
require("es6-promise").polyfill();
import Dragndrop from "./Dragndrop";
// import LinksImport from "./LinksImport";
const axios = () => import(/* webpackChunkName: "axios" */ "axios");

export default {
  props: {
    postURL: {
      type: String,
      required: true
    },
    minfiles: {
      type: Number,
      default: 1
    },
    maxfiles: {
      type: Number,
      default: 30
    },
    method: {
      type: String,
      default: "post"
    },
    postMeta: {
      type: [String, Array, Object],
      default: ""
    },
    postData: {
      type: [Object],
      default: () => {}
    },
    postHeader: {
      type: [Object],
      default: () => {}
    },
    successMessagePath: {
      type: String,
      required: true
    },
    errorMessagePath: {
      type: String,
      required: true
    },
    headerMessage: {
      type: String,
      default: ""
    },
    dropAreaPrimaryMessage: {
      type: String,
      default: ""
    },
    dropAreaSecondaryMessage: {
      type: String,
      default: ""
    },
    fileNameMessage: {
      type: String,
      default: "Имена"
    },
    fileSizeMessage: {
      type: String,
      default: "Длина"
    },
    totalFileMessage: {
      type: String,
      default: "Всего файлов:"
    },
    totalUploadSizeMessage: {
      type: String,
      default: "Всего данных:"
    },
    addMoreFiles: {
      type: String,
      default: "Добавить ещё файл"
    },
    uploadButtonMessage: {
      type: String,
      default: "Загрузить"
    },
    cancelButtonMessage: {
      type: String,
      default: "Отменить"
    },
    fileUploadErrorMessage: {
      type: String,
      default: "Произошла ошибка"
    },
    minFilesErrorMessage: {
      type: String,
      default: "Минимальное количество файлов"
    },
    maxFilesErrorMessage: {
      type: String,
      default: "Максимальное количество файлов"
    },
    retryErrorMessage: {
      type: String,
      default: "Попробуйте снова"
    },
    httpMethodErrorMessage: {
      type: String,
      default:
        "This HTTP method is not allowed. Please use either 'put' or 'post' methods."
    },
    showHttpMessages: {
      type: Boolean,
      default: true
    },
    links: {
      type: Array,
      default: () => []
    }
  },
  /*
   * The component's data.
   */
  data() {
    return {
      dragging: false,
      files: [], // files to show
      filelist: [], // files to send
      successMsg: "",
      errorMsg: ""
    };
  },
  components: {
    Dragndrop,
    // LinksImport
  },
  methods: {
    removefiles() {
      this.files = [];
      this.filelist = [];
      this.links = [];
      this.dragging = false;
    },
    link_added($event) {
      this.links = [...this.links, $event];
    },
    link_removed($event) {
      this.links = this.links.filter(x => x !== $event);
    },
    file_added($event) {
      this.filelist = $event;

      const inputFiles = [...$event]; // this is hack to get out of FileList that's not an array
      this.files = [...inputFiles, ...this.files].filter(x => x);
    },
    file_removed($event) {
      this.files = this.files.filter(x => x.name !== $event);
    },
    onSubmit() {
      if (this.filelist.length === 0) {
        return Promise.resolve({status: 200, data: {ids: []}});
      }

      const formData = new FormData();
      for (let i = 0; i < this.filelist.length; i++) {
        formData.append(`files[${i}]`, this.filelist[i]);
      }

      for (let i = 0; i < this.links.length; i++) {
        formData.append(`links[${i}]`, this.links[i]);
      }

      // why do we need separate postMeta and postData?
      const isString =
        typeof this.postMeta === "string" && this.postMeta !== "";
      const isObject =
        typeof this.postMeta === "object" &&
        Object.keys(this.postMeta).length > 0;
      const isArray =
        typeof this.postData === "object" &&
        this.postData !== null &&
        Object.keys(this.postData).length > 0;

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

      return axios().then(
        ax =>
          ax.request({
            method: this.method,
            url: this.postURL,
            data: formData,
            headers: this.postHeader
          }))
        .then(response => {
          if (this.showHttpMessages) {
            this.successMsg = response + "." + this.successMessagePath;
          }

          this.removefiles();

          return response;
        })
        .catch(error => {
          if (this.showHttpMessages) {
            this.errorMsg = error + "." + this.errorMessagePath;
          }

          this.removefiles();
        });
    }
  }
};
</script>

<style lang="scss" scoped>
.mfu-buttons-wrapper {
  display: flex;
  flex-direction: row-reverse;
}

.mfu-files-input {
  display: flex;
}

.mfu-uploadBox {
  border: 1px solid var(--background-secondary-color);
  width: 100%;
}
</style>
