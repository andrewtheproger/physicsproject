<template>
  <div class="uploadBox">
    <form role="form" enctype="multipart/form-data" @submit.prevent="onSubmit">

      <div class="ph-files-input">

        <div class="uploadBoxMain">
          <div class="form-group">
            <div
              class="dropArea animatedBorders"
              @ondragover="onChange"
              :class="dragging ? 'dropAreaDragging' : ''"
              @dragenter="dragging = true"
              @dragend="dragging = false"
              @dragleave="dragging = false"
            >
              <md-icon>
                file_copy
              </md-icon>
              <span>Перетащите файлы или...</span>
              <input
                type="file"
                id="items"
                name="items[]"
                required
                multiple
                @change="onChange"
                ref="file"
              />
            </div>
          </div>

          <div v-if="itemsAdded">
            <p>
              <strong>{{ fileNameMessage }}</strong>
            </p>
            <ol>
              <li v-for="(name, i) in itemsNames" :key="`name-${i}`">{{ name }}</li>
            </ol>
            <p>
              <strong>{{ fileSizeMessage }}</strong>
            </p>
            <ol>
              <li v-for="(size, i) in itemsSizes" :key="`size-${i}`">{{ size }}</li>
            </ol>
            <p>
              <strong>{{ totalFileMessage }}</strong> {{ itemsAdded }}
            </p>
            <p>
              <strong>{{ totalUploadSizeMessage }}</strong> {{ itemsTotalSize }}
            </p>

            <button @click.prevent="$refs.file.click()">{{ addMoreFiles }}</button>
            
            <div class="loader" v-if="isLoaderVisible">
              <div class="loaderImg"></div>
            </div>
          </div>
        </div>
        
        <md-field>
          <label>...вставьте ссылку</label>
          <md-input @paste.prevent="onPaste" class="ph-filelink-input" type="text"></md-input>
        </md-field>
      </div>

      <div class="buttons-wrapper">
        <md-button
          type="button"
          class="md-raised md-accent"
          @click="removeItems"
          :disabled="itemsAdded.length === 0"
        >
          {{ cancelButtonMessage }}
        </md-button>
        <md-button
          type="button"
          class="md-raised md-primary"
          :disabled="itemsAdded < minItems || itemsAdded > maxItems"
        >
          {{ uploadButtonMessage }}
        </md-button>
      </div>
      <br />
      <div class="successMsg" v-if="successMsg !== ''">{{ successMsg }}</div>
      <div class="errorMsg" v-if="errorMsg !== ''">
        {{ fileUploadErrorMessage }}:<br />{{ errorMsg }} <br />{{
          retryErrorMessage
        }}
      </div>
      <div class="errorMsg" v-if="itemsAdded && itemsAdded < minItems">
        {{ minFilesErrorMessage }}: {{ minItems }}. <br />{{
          retryErrorMessage
        }}
      </div>
      <div class="errorMsg" v-if="itemsAdded && itemsAdded > maxItems">
        {{ maxFilesErrorMessage }}: {{ maxItems }}. <br />{{
          retryErrorMessage
        }}
      </div>
    </form>
  </div>
</template>

<script>
require("es6-promise").polyfill();
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
    minItems: {
      type: Number,
      default: 1,
    },
    maxItems: {
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
      items: [],
      itemsAdded: "",
      itemsNames: [],
      itemsSizes: [],
      itemsTotalSize: "",
      formData: "",
      successMsg: "",
      errorMsg: "",
      isLoaderVisible: false,
    };
  },
  methods: {
    // http://scratch99.com/web-development/javascript/convert-bytes-to-mb-kb/
    bytesToSize(bytes) {
      const sizes = ["байт", "килобайт", "мегабайт", "гигабайт", "терабайт"];
      if (bytes === 0) return "n/a";
      let i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
      if (i === 0) return bytes + " " + sizes[i];
      return (bytes / Math.pow(1024, i)).toFixed(2) + " " + sizes[i];
    },
    onChange(e) {
      this.successMsg = "";
      this.errorMsg = "";
      this.dragging = false; // that doesn't work on element, idk why
      this.formData = new FormData();

      const inputFiles = [...(e.target.files || e.dataTransfer.files)] // this is hack to get out of FileList that's not an array
      let files = [...inputFiles, ...this.items];
      
      this.itemsAdded = files.length;
      
      for (const x in files) {
        if (!isNaN(x)) {
          this.itemsNames = files.map(x => x.name)
          this.itemsSizes = files.map(x => this.bytesToSize(x.size));
          this.itemsTotalSize = this.bytesToSize(files.reduce((acc, cur) => acc + cur.size, 0));
          this.items = files;
          this.formData.append("items[]", this.items);
        }
      }
    },
    removeItems() {
      this.items = "";
      this.itemsAdded = "";
      this.itemsNames = [];
      this.itemsSizes = [];
      this.itemsTotalSize = "";
      this.dragging = false;
    },
    onSubmit() {
      this.isLoaderVisible = true;
      if (
        (typeof this.postMeta === "string" && this.postMeta !== "") ||
        (typeof this.postMeta === "object" &&
          Object.keys(this.postMeta).length > 0)
      ) {
        this.formData.append("postMeta", this.postMeta);
      }

      if (
        typeof this.postData === "object" &&
        this.postData !== null &&
        Object.keys(this.postData).length > 0
      ) {
        for (var key in this.postData) {
          this.formData.append(key, this.postData[key]);
        }
      }
      if (this.method === "put" || this.method === "post") {
        axios({
          method: this.method,
          url: this.postURL,
          data: this.formData,
          headers: this.postHeader,
        })
          .then((response) => {
            this.isLoaderVisible = false;
            // Show success message
            if (this.showHttpMessages)
              this.successMsg = response + "." + this.successMessagePath;
            this.removeItems();
          })
          .catch((error) => {
            this.isLoaderVisible = false;
            if (this.showHttpMessages)
              this.errorMsg = error + "." + this.errorMessagePath;
            this.removeItems();
          });
      } else {
        if (this.showHttpMessages) this.errorMsg = this.httpMethodErrorMessage;
        this.removeItems();
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import "../config/variables.scss";

.md-field,
.md-field.md-theme-default.md-focused,
.md-field.md-theme-default.md-has-value {
  .md-input,
  label {
    color: inherit;
    -webkit-text-fill-color: inherit;
  }

  width: 50%;
  max-height: 3em;
}

.md-field.md-theme-default label,
.md-icon.md-theme-default.md-icon-font {
  color: inherit;
}

.md-field.md-theme-default label {
  padding-left: 1em;
}

.buttons-wrapper {
  display: flex;
  flex-direction: row-reverse;

  button {
    width: 10%;
  }
}

.ph-files-input {
  display: flex;
  align-items: bottom;

  .uploadBoxMain,
  .ph-filelink-input {
    width: 50%;
  }
}

.uploadBox {
  background: $secondary-bg-color;
  color: $primary-fg-color;
  width: 100%;

  .dropArea {
    text-align: center;
    padding: 1em;
    background-color: $secondary-bg-color;
    
    &::before,
    &::after {
        cursor: pointer;
    }

    &:hover {
      background-color: lighten($secondary-bg-color, 10%);
    }

    input {
      position: absolute;
      cursor: pointer;
      top: 0;
      bottom: 0;
      left: 0;
      width: 100%;
      opacity: 0;
    }
  }
  
  .dropAreaDragging {
    background-color: lighten($secondary-bg-color, 10%);
  }

  .animatedBorders {
    position: relative;

    box-sizing: border-box;
    box-shadow: inset 0 0 0 2px lighten($primary-bg-color, 40%);

    transition: color 0.25s;

    &::before,
    &::after {
      box-sizing: inherit;
      content: '';
      position: absolute;
      width: 100%;
      height: 100%;
      pointer-events: none;

      border: 2px solid transparent;
      width: 0;
      height: 0;
    }

    &::before {
      top: 0;
      left: 0;
    }

    &::after {
      bottom: 0;
      right: 0;
    }
    
    &:hover {
      color: $secondary-fg-color;
    }

    &:hover::before,
    &:hover::after {
      width: 100%;
      height: 100%;
    }

    &:hover::before {
      border-top-color: $secondary-fg-color;
      border-right-color: $secondary-fg-color;
      transition:
        width 0.25s ease-out,
        height 0.25s ease-out 0.25s;
    }

    &:hover::after {
      border-bottom-color: $secondary-fg-color;
      border-left-color: $secondary-fg-color;
      
      transition:
        border-color 0s ease-out 0.5s,
        width 0.25s ease-out 0.5s,
        height 0.25s ease-out 0.75s;
    }
  }
}


  
</style>
