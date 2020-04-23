<template>
  <div class="mfu-uploadBoxMain">
    <div
      class="mfu-dropArea mfu-animatedBorders"
      @ondragover="addFile"
      :class="dragging ? 'mfu-dropAreaDragging' : ''"
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
        multiple
        @change="addFile"
        ref="file"
      />
    </div>

    <div v-if="files.length">
      <p>
        <strong>{{ fileNameMessage }}</strong>

        <ol>
          <li
            class="mfu-file-name"
            v-for="(file, i) in files" 
            :key="`${file.name}-${i}`"
            :data-name="file.name"
            @click="removeFile"
            >
            {{ file.name }}
          </li>
        </ol>
      </p>
      

      <p>
        <strong>{{ fileSizeMessage }}</strong>

        <ol>
          <li
            v-for="(file, i) in files"
            :key="`size-${i}`"
            >
            {{ bytesToSize(file.size) }}
          </li>
        </ol>
      </p>
     
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
</template>

<script>
require("es6-promise").polyfill();
import axios from "axios";
{
  axios;
}
export default {
  props: {
    files: {
      type: Array
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
    }
  },
  data() {
    return {
      dragging: false,
      isLoaderVisible: false,
    };
  },
  methods: {
    bytesToSize(bytes) {
      const sizes = ["байт", "килобайт", "мегабайт", "гигабайт", "терабайт"];
      if (bytes === 0) return "n/a";
      let i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
      if (i === 0) return bytes + " " + sizes[i];
      return (bytes / Math.pow(1024, i)).toFixed(2) + " " + sizes[i];
    },
    addFile(e) {
      this.successMsg = "";
      this.errorMsg = "";
      this.dragging = false; // that doesn't work on element, idk why

      const inputFilelist = e.target.files || e.dataTransfer.files;
      const inputFiles = [...(inputFilelist)]; // this is hack to get out of FileList that's not an array
      
      this.$emit('file_added', inputFiles)
    },
    removeFile(e) {
      const value = e.target.dataset.name;

      this.$emit('file_removed', value)
    }
  }
};
</script>

<style lang="scss" scoped>
@import "../../config/variables.scss";

.mfu-uploadBoxMain,
.mfu-filelink-input {
  width: 50%;
}

.mfu-file-name {
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



.mfu-dropArea {
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

.mfu-dropAreaDragging {
  background-color: lighten($secondary-bg-color, 10%);
}

.mfu-animatedBorders {
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
</style>
