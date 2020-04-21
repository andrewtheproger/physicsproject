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
                id="files"
                name="files[]"
                required
                multiple
                @change="onChange"
                ref="file"
              />
            </div>
          </div>

          <div v-if="files.length">
            <p>
              <strong>{{ fileNameMessage }}</strong>
            </p>
            <ol>
              <li
                class="file-name"
                v-for="(file, i) in files" 
                :key="`${file.name}-${i}`"
                :data-name="file.name"
                @click="removeFile"
                >
                {{ file.name }}
              </li>
            </ol>
            <p>
              <strong>{{ fileSizeMessage }}</strong>
            </p>
            <ol>
              <li
                v-for="(file, i) in files"
                :key="`size-${i}`"
                >
                {{ bytesToSize(file.size) }}
              </li>
            </ol>
            <p>
              <strong>{{ totalFileMessage }}</strong> {{ files.length }}
            </p>
            <p>
              <strong>{{ totalUploadSizeMessage }}</strong> {{ bytesToSize(files.reduce((acc, cur) => acc + cur.size, 0)) }}
            </p>
            
            <md-button
              type="button"
              class="md-raised"
              @click.prevent="$refs.file.click()"
            >
              {{ addMoreFiles }}
            </md-button>

            <div class="loader" v-if="isLoaderVisible">
              <div class="loaderImg"></div>
            </div>
          </div>
        </div>
        
        <div class="container">
          <md-field>
            <label>...вставьте ссылку</label>
            <md-input @paste.prevent="onPaste" class="ph-filelink-input" type="text"></md-input>
          </md-field>

          <ul class="previews">
                  <transition-group name="slide-fade" mode="out-in">

              <li 
                class="preview"
                v-for="(link, i) in links" 
                :key="`link-${i}`"
                :data-link="link"
                @click="removeLink"
                >
                    <img :src="link" alt="img"  />
              </li>
                  </transition-group>
          </ul>
        </div>
      </div>

      <div class="buttons-wrapper">
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
      <div class="successMsg" v-if="successMsg !== ''">{{ successMsg }}</div>
      <div class="errorMsg" v-if="errorMsg !== ''">
        {{ fileUploadErrorMessage }}:<br />{{ errorMsg }} <br />{{
          retryErrorMessage
        }}
      </div>
      <div class="errorMsg" v-if="files.length && files.length < minfiles">
        {{ minFilesErrorMessage }}: {{ minfiles }}. <br />{{
          retryErrorMessage
        }}
      </div>
      <div class="errorMsg" v-if="files.length && files.length > maxfiles">
        {{ maxFilesErrorMessage }}: {{ maxfiles }}. <br />{{
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
  methods: {
    onPaste(e) {
      const value = e.clipboardData.getData('Text').trim()

      if (this.links.includes(value)) {
        return;
      }

      this.links = [...this.links, value]
    },
    removeLink(e) {
      const value = e.target.dataset.link;

      this.links = this.links.filter(x => x !== value)
    },
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

      const inputFilelist = e.target.files || e.dataTransfer.files;
      const inputFiles = [...(inputFilelist)]; // this is hack to get out of FileList that's not an array
      let files = [...inputFiles, ...this.files].filter(x => x);
      
      this.files = files;
    },
    removeFile(e) {
      const value = e.target.dataset.name;

      this.files = this.files.filter(x => x.name !== value);
    },
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
@import "../config/variables.scss";

.file-name {
  position: relative;

  &:after {
    display: none;
    content: 'X';
    font-size: 2em;
    color: #d00;
    cursor: pointer;

    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    
    background-color: rgba(0,0,0,0.2);
  }

  &:hover {
    &:after {
      display: flex;
      justify-content: center;
      align-items: center;
    }
  }
}

.container {
  display: flex;
  flex-direction: column;
  width: 50%;

  .previews span{
    list-style: none;
    display: flex;
    flex-wrap: wrap;
    align-items: center;

    .slide-fade-enter-active {
      transition: all .3s ease;
    }

    .slide-fade-leave-active {
      transition: all .3s ease;
    }

    .slide-fade-enter {
      transform: translateY(-100px);
      opacity: 0;
    }

    .slide-fade-leave-to {
      transform: translateY(100px);
      opacity: 0; 
    }

    .preview {
      margin: 3px;
      width: 30%;
      position: relative;
      transition: all 1 easy;

      &:after {
        display: none;
        content: 'X';
        font-size: 3em;
        color: #d00;
        cursor: pointer;

        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        
        background-color: rgba(0,0,0,0.2);
      }

      &:hover {
        &:after {
          display: flex;
          justify-content: center;
          align-items: center;
        }
      }
    }
  }
}

.md-field,
.md-field.md-theme-default.md-focused,
.md-field.md-theme-default.md-has-value {
  .md-input,
  label {
    color: inherit;
    -webkit-text-fill-color: inherit;
  }


  &:hover:after {
    background-color: $secondary-fg-color;
    transition: all .3s;
  }

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
