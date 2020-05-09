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
            @click="removeFile">
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
      dragging: false
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
      this.dragging = false;

      const inputFilelist = e.target.files || e.dataTransfer.files;

      this.$emit('file_added', inputFilelist)
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

.mfu-uploadBoxMain {
  width: 50%;
}
.mfu-uploadBoxMain {
  width: 100%;
  height: 100%;
}
.mfu-file-name {
  position: relative;

  &:after {
    display: none;
    content: 'X';
    font-size: 2em;
    color: var(--foreground-error-color);
    cursor: pointer;

    position: absolute;
    top: 0;
    right: -1em;
    bottom: 0;
    left: 0;

    background-color: alpha(var(--background-primary-color), 0.2);
  }

  &:hover {
    &:after {
      display: flex;
      flex-direction: row-reverse;
    }
  }
}

.mfu-dropArea {
  text-align: center;
  padding: 1em;
  background-color: var(--background-secondary-color);
  color: var(--foreground-primary-color);

  &::before,
  &::after {
    cursor: pointer;
  }

  &:hover {
    background-color: alpha(var(--background-secondary-color), 0.7);
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
  background-color: alpha(var(--background-secondary-color), 0.7)
}

.mfu-animatedBorders {
  position: relative;

  box-sizing: border-box;
  box-shadow: inset 0 0 0 2px alpha(var(--background-primary-color), 0.7);

  transition: color 0.25s;

  &::before,
  &::after {
    box-sizing: inherit;
    content: '';
    position: absolute;
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
    color: var(--foreground-primary-color);
  }

  &:hover::before,
  &:hover::after {
    width: 100%;
    height: 100%;
  }

  &:hover::before {
    border-top-color: var(--background-secondary-color);
    border-right-color: var(--background-secondary-color);
    transition:
      width 0.25s ease-out,
      height 0.25s ease-out 0.25s;
  }

  &:hover::after {
    border-bottom-color: var(--background-secondary-color);
    border-left-color: var(--background-secondary-color);

    transition:
      border-color 0s ease-out 0.5s,
      width 0.25s ease-out 0.5s,
      height 0.25s ease-out 0.75s;
  }
} 
</style>
