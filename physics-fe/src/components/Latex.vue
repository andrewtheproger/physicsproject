<template>
  <div class="ph-latex">
    <div class="ph-latex-editor">
      <editor
        v-model="body.latex"
        @init="editorInit"
        lang="latex"
        ref="aceEditor"
        font-size="40px"
        width="100%"
        height="100%"
      />

      <!--      todo how to place these controls inside ace editor block? Now it squeezes when page scrolls -->
      <div class="ph-latex-editor-controls">
        <span v-if="this.aceZoom.current !== 100"
          >{{ this.aceZoom.current }} %</span
        >

        <md-button class="md-dense md-icon-button" @click="this.copyLatex">
          <md-icon :class="this.getCopyStatusClass">file_copy</md-icon>
        </md-button>

        <md-button class="md-dense md-icon-button" @click="this.onAceZoomIn">
          <md-icon>zoom_in</md-icon>
        </md-button>

        <md-button class="md-dense md-icon-button" @click="this.onAceZoomOut">
          <md-icon>zoom_out</md-icon>
        </md-button>
      </div>
    </div>

    <div class="ph-mathjax" :style="this.getMathjaxStyle()">
      <md-field class="ph-ace-theme-editor">
        <label for="ace-editor-theme">Тема редактора</label>
        <md-select
          v-model="colorSchema"
          name="ace-editor-theme"
          id="ace-editor-theme"
          @md-selected="setColorSchema"
        >
          <md-optgroup label="Светлые">
            <md-option value="ace/theme/chrome">Chrome</md-option>
            <md-option value="ace/theme/clouds">Clouds</md-option>
            <md-option value="ace/theme/crimson_editor"
              >Crimson_editor</md-option
            >
            <md-option value="ace/theme/dawn">Dawn</md-option>
            <md-option value="ace/theme/dreamweaver">Dreamweaver</md-option>
            <md-option value="ace/theme/eclipse">Eclipse</md-option>
            <md-option value="ace/theme/github">Github</md-option>
            <md-option value="ace/theme/iplastic">Iplastic</md-option>
            <md-option value="ace/theme/katzenmilch">Katzenmilch</md-option>
            <md-option value="ace/theme/kuroir">Kuroir</md-option>
            <md-option value="ace/theme/solarized_light"
              >Solarized_light</md-option
            >
            <md-option value="ace/theme/sqlserver">Sqlserver</md-option>
            <md-option value="ace/theme/textmate">Textmate</md-option>
            <md-option value="ace/theme/tomorrow">Tomorrow</md-option>
            <md-option value="ace/theme/xcode">Xcode</md-option>
          </md-optgroup>
          <md-optgroup label="Тёмные">
            <md-option value="ace/theme/ambiance">Ambiance</md-option>
            <md-option value="ace/theme/chaos">Chaos</md-option>
            <md-option value="ace/theme/clouds_midnight"
              >Clouds_midnight</md-option
            >
            <md-option value="ace/theme/cobalt">Cobalt</md-option>
            <md-option value="ace/theme/dracula">Dracula</md-option>
            <md-option value="ace/theme/gob">Gob</md-option>
            <md-option value="ace/theme/gruvbox">Gruvbox</md-option>
            <md-option value="ace/theme/idle_fingers">Idle_fingers</md-option>
            <md-option value="ace/theme/kr_theme">Kr_theme</md-option>
            <md-option value="ace/theme/merbivore">Merbivore</md-option>
            <md-option value="ace/theme/merbivore_soft"
              >Merbivore_soft</md-option
            >
            <md-option value="ace/theme/mono_industrial"
              >Mono_industrial</md-option
            >
            <md-option value="ace/theme/monokai">Monokai</md-option>
            <md-option value="ace/theme/pastel_on_dark"
              >Pastel_on_dark</md-option
            >
            <md-option value="ace/theme/solarized_dark"
              >Solarized_dark</md-option
            >
            <md-option value="ace/theme/terminal">Terminal</md-option>
            <md-option value="ace/theme/tomorrow_night"
              >Tomorrow_night</md-option
            >
            <md-option value="ace/theme/tomorrow_night_blue"
              >Tomorrow_night_blue</md-option
            >
            <md-option value="ace/theme/tomorrow_night_bright"
              >Tomorrow_night_bright</md-option
            >
            <md-option value="ace/theme/tomorrow_night_eighties"
              >Tomorrow_night_eighties</md-option
            >
            <md-option value="ace/theme/twilight">Twilight</md-option>
            <md-option value="ace/theme/vibrant_ink">Vibrant_ink</md-option>
          </md-optgroup>
        </md-select>
      </md-field>

      <vue-mathjax
        class="ph-mathjax-render"
        :formula="this.body.latex"
      ></vue-mathjax>

      <div class="ph-mathjax-controls">
        <md-button
          class="md-dense md-icon-button"
          @click="this.onMathjaxZoomIn"
        >
          <md-icon>zoom_in</md-icon>
        </md-button>

        <md-button
          class="md-dense md-icon-button"
          @click="this.onMathjaxZoomOut"
        >
          <md-icon>zoom_out</md-icon>
        </md-button>

        <span v-if="this.mathjaxZoom.current !== 100"
          >{{ this.mathjaxZoom.current }} %</span
        >

        <span v-if="body.created_date"
          >Восстановлен LaTeX от {{ body.restored }}</span
        >
      </div>
    </div>
  </div>
</template>

<script>
import VueMathjax from "./VueMathJax/vueMathJax";

import config from "../config/api.js";
const axios = () => import(/* webpackChunkName: "axios" */ "axios");

require("brace/ext/language_tools");
require("brace/mode/latex");
require("brace/snippets/latex");
require("brace/theme/ambiance");
require("brace/theme/chaos");
require("brace/theme/chrome");
require("brace/theme/clouds");
require("brace/theme/clouds_midnight");
require("brace/theme/cobalt");
require("brace/theme/crimson_editor");
require("brace/theme/dawn");
require("brace/theme/dracula");
require("brace/theme/dreamweaver");
require("brace/theme/eclipse");
require("brace/theme/github");
require("brace/theme/gob");
require("brace/theme/gruvbox");
require("brace/theme/idle_fingers");
require("brace/theme/iplastic");
require("brace/theme/katzenmilch");
require("brace/theme/kr_theme");
require("brace/theme/kuroir");
require("brace/theme/merbivore");
require("brace/theme/merbivore_soft");
require("brace/theme/mono_industrial");
require("brace/theme/monokai");
require("brace/theme/pastel_on_dark");
require("brace/theme/solarized_dark");
require("brace/theme/solarized_light");
require("brace/theme/sqlserver");
require("brace/theme/terminal");
require("brace/theme/textmate");
require("brace/theme/tomorrow");
require("brace/theme/tomorrow_night");
require("brace/theme/tomorrow_night_blue");
require("brace/theme/tomorrow_night_bright");
require("brace/theme/tomorrow_night_eighties");
require("brace/theme/twilight");
require("brace/theme/vibrant_ink");
require("brace/theme/xcode");

const latexLocalStorageKey = "ph-3800-latex-input";

export default {
  name: "Latex",
  components: {
    VueMathjax,
    editor: require("vue2-ace-editor")
  },
  data() {
    return {
      body: {
        latex:
          localStorage.getItem(latexLocalStorageKey) ||
          "Привет, это текст на $ \\LaTeX $, да. "
      },
      copyStatus: null,
      colorSchema: null,
      mathjaxZoom: {
        current: 100,
        min: 50,
        max: 150,
        step: 10
      },
      aceZoom: {
        current: 100,
        min: 50,
        max: 150,
        step: 10
      }
    };
  },
  created() {
    const s = localStorage.getItem(latexLocalStorageKey);

    if (s) {
      this.body = JSON.parse(s);
    } else {
      this.body.latex = "Привет, это текст на $ \\LaTeX $, да. ";
    }

    if (this.body.created_date) {
      this.body.restored = new Date(this.body.created_date).toLocaleDateString(
        "ru-RU",
        config.datetime_format
      );
    } else {
      this.body.restored = "неизвестного числа";
    }
  },
  mounted() {
    const theme =
      this.user && this.user.ace_theme
        ? this.user.ace_theme
        : "brace/theme/tomorrow_night";
    this.$refs.aceEditor.editor.setTheme(theme);
    this.colorSchema = theme;
  },
  computed: {
    getCopyStatusClass() {
      if (this.copyStatus === null) {
        return "";
      }

      return this.copyStatus ? "ph-success" : "ph-failure";
    },
    user() {
      return this.$store.getters.get_user;
    }
  },
  methods: {
    setColorSchema: function(e) {
      const url = config.apiPrefix + "/users/me";
      this.$refs.aceEditor.editor.setTheme(e);

      axios().then(ax =>
        ax
          .request({
            url: url,
            method: "POST",
            data: {
              ace_theme: e
            },
            headers: {
              Authorization: this.$store.getters.get_jwt
            }
          })
          .then(
            ({ data }) => this.$store.commit("set_user", data),
            error => console.log(error)
          )
      );
    },
    getMathjaxStyle: function() {
      return {
        fontSize: `${this.mathjaxZoom.current}%`
      };
    },
    onAceZoomIn: function() {
      if (this.aceZoom.current + this.aceZoom.step <= this.aceZoom.max) {
        this.aceZoom.current += this.aceZoom.step;
      }
      this.$refs.aceEditor.editor.setFontSize(`${this.aceZoom.current}%`);
    },
    onAceZoomOut: function() {
      if (this.aceZoom.current - this.aceZoom.step >= this.aceZoom.min) {
        this.aceZoom.current -= this.aceZoom.step;
      }
      this.$refs.aceEditor.editor.setFontSize(`${this.aceZoom.current}%`);
    },
    onMathjaxZoomIn: function() {
      if (
        this.mathjaxZoom.current + this.mathjaxZoom.step <=
        this.mathjaxZoom.max
      ) {
        this.mathjaxZoom.current += this.mathjaxZoom.step;
      }
    },
    onMathjaxZoomOut: function() {
      if (
        this.mathjaxZoom.current + this.mathjaxZoom.step >=
        this.mathjaxZoom.min
      ) {
        this.mathjaxZoom.current -= this.mathjaxZoom.step;
      }
    },
    editorInit: function(editor) {
      editor.on("change", this.onLatexChange); // it doesn't work as @change dunno why
      editor.setOption("wrap", true);
    },
    copyLatex() {
      const setCopyStatusToNull = () => (this.copyStatus = null);

      this.$copyText(this.latex).then(
        () => {
          setTimeout(setCopyStatusToNull, 1000);
          return (this.copyStatus = true);
        },
        () => {
          setTimeout(setCopyStatusToNull, 1000);
          return (this.copyStatus = false);
        }
      );
    },
    onLatexChange() {
      const json = JSON.stringify({
        latex: this.body.latex || "",
        created_date: Date.now()
      });
      localStorage.setItem(latexLocalStorageKey, json);
    }
  }
};
</script>

<style scoped lang="scss">
.ph-ace-theme-editor {
  margin: 0 1em;
}

.ph-latex {
  display: flex;
  padding: 1em;
  width: 100%;
  -webkit-text-fill-color: initial;

  .ph-latex-editor-controls {
    display: flex;
    justify-content: flex-end;

    position: absolute;
    bottom: 0;
    right: 0em;

    opacity: 0.3;

    transition: all 0.3s ease;

    .md-icon:hover {
      opacity: 0.8;
    }
  }

  .ph-mathjax-controls {
    display: flex;
    justify-content: flex-start;
    width: 100%;
  }

  .ph-mathjax {
    display: flex;
    flex-wrap: wrap;
  }

  .ph-latex-editor {
    position: relative;

    .ace_editor {
      max-height: 70vh; // ace editor bugs when the content is too high
    }
  }

  .ph-mathjax,
  .ph-latex-editor {
    min-width: 50%;
    min-height: 15em;
  }

  .ph-mathjax-render {
    margin: 1em;
    min-height: 25vh;
    overflow: auto;

    word-wrap: break-word;
    white-space: pre-wrap;

    background-color: var(--background-primary-color);
    color: var(--foreground-primary-color);
  }
}
</style>
