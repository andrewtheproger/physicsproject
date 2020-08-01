<template>
  <div class="ph-latex">
    <div class="ph-latex-editor">
      <editor
        v-model="this.body.latex"
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

export default {
  name: "Latex",
  components: {
    VueMathjax,
    editor: require("vue2-ace-editor")
  },
  props: ['localStorageKey', 'initial_latex', 'created_date'],
  data() {
    return {
      body: {
        latex: null,
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
      },
      aceSettings: []
    };
  },
  created() {
    this.body.latex = this.initial_latex || '';

    if (this.body.created_date) {
      this.body.restored = new Date(this.body.created_date).toLocaleDateString(
        "ru-RU",
        config.datetime_format
      );
    } else {
      this.body.restored = "неизвестного числа";
    }

    this.aceSettings = [
      {
        name: "brace/ext/language_tools",
        import: () => import("brace/ext/language_tools")
      },
      { name: "brace/mode/latex", import: () => import("brace/mode/latex") },
      {
        name: "brace/snippets/latex",
        import: () => import("brace/snippets/latex")
      },
      {
        name: "brace/theme/ambiance",
        import: () => import("brace/theme/ambiance")
      },
      { name: "brace/theme/chaos", import: () => import("brace/theme/chaos") },
      {
        name: "brace/theme/chrome",
        import: () => import("brace/theme/chrome")
      },
      {
        name: "brace/theme/clouds",
        import: () => import("brace/theme/clouds")
      },
      {
        name: "brace/theme/clouds_midnight",
        import: () => import("brace/theme/clouds_midnight")
      },
      {
        name: "brace/theme/cobalt",
        import: () => import("brace/theme/cobalt")
      },
      {
        name: "brace/theme/crimson_editor",
        import: () => import("brace/theme/crimson_editor")
      },
      { name: "brace/theme/dawn", import: () => import("brace/theme/dawn") },
      {
        name: "brace/theme/dracula",
        import: () => import("brace/theme/dracula")
      },
      {
        name: "brace/theme/dreamweaver",
        import: () => import("brace/theme/dreamweaver")
      },
      {
        name: "brace/theme/eclipse",
        import: () => import("brace/theme/eclipse")
      },
      {
        name: "brace/theme/github",
        import: () => import("brace/theme/github")
      },
      { name: "brace/theme/gob", import: () => import("brace/theme/gob") },
      {
        name: "brace/theme/gruvbox",
        import: () => import("brace/theme/gruvbox")
      },
      {
        name: "brace/theme/idle_fingers",
        import: () => import("brace/theme/idle_fingers")
      },
      {
        name: "brace/theme/iplastic",
        import: () => import("brace/theme/iplastic")
      },
      {
        name: "brace/theme/katzenmilch",
        import: () => import("brace/theme/katzenmilch")
      },
      {
        name: "brace/theme/kr_theme",
        import: () => import("brace/theme/kr_theme")
      },
      {
        name: "brace/theme/kuroir",
        import: () => import("brace/theme/kuroir")
      },
      {
        name: "brace/theme/merbivore",
        import: () => import("brace/theme/merbivore")
      },
      {
        name: "brace/theme/merbivore_soft",
        import: () => import("brace/theme/merbivore_soft")
      },
      {
        name: "brace/theme/mono_industrial",
        import: () => import("brace/theme/mono_industrial")
      },
      {
        name: "brace/theme/monokai",
        import: () => import("brace/theme/monokai")
      },
      {
        name: "brace/theme/pastel_on_dark",
        import: () => import("brace/theme/pastel_on_dark")
      },
      {
        name: "brace/theme/solarized_dark",
        import: () => import("brace/theme/solarized_dark")
      },
      {
        name: "brace/theme/solarized_light",
        import: () => import("brace/theme/solarized_light")
      },
      {
        name: "brace/theme/sqlserver",
        import: () => import("brace/theme/sqlserver")
      },
      {
        name: "brace/theme/terminal",
        import: () => import("brace/theme/terminal")
      },
      {
        name: "brace/theme/textmate",
        import: () => import("brace/theme/textmate")
      },
      {
        name: "brace/theme/tomorrow",
        import: () => import("brace/theme/tomorrow")
      },
      {
        name: "brace/theme/tomorrow_night",
        import: () => import("brace/theme/tomorrow_night")
      },
      {
        name: "brace/theme/tomorrow_night_blue",
        import: () => import("brace/theme/tomorrow_night_blue")
      },
      {
        name: "brace/theme/tomorrow_night_bright",
        import: () => import("brace/theme/tomorrow_night_bright")
      },
      {
        name: "brace/theme/tomorrow_night_eighties",
        import: () => import("brace/theme/tomorrow_night_eighties")
      },
      {
        name: "brace/theme/twilight",
        import: () => import("brace/theme/twilight")
      },
      {
        name: "brace/theme/vibrant_ink",
        import: () => import("brace/theme/vibrant_ink")
      },
      { name: "brace/theme/xcode", import: () => import("brace/theme/xcode") }
    ];
  },
  mounted() {
    const theme =
      (this.user && this.user.ace_theme)
        ? this.user.ace_theme
        : 'ace/theme/tomorrow_night';

      return this.aceSettings
        .filter(x => x.name === `br${theme}`)[0]
        .import()
        .then(() => {
          this.colorSchema = theme;
          this.$refs.aceEditor.editor.setTheme(`br${theme}`);
        });
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
      const availableThemes = this.aceSettings.filter(x => x.name === `br${e}`);

      if (availableThemes && availableThemes.length) {
        const theme = availableThemes[0];

        theme.import().then(() => this.$refs.aceEditor.editor.setTheme(e));
      }

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
      const requiredImports = this.aceSettings
        .filter(x => ['brace/ext/language_tools', 'brace/mode/latex', 'brace/snippets/latex', `brace/theme/tomorrow_night`].includes(x.name))
        .map(x => {
          return x.import();
        });

      Promise.all(requiredImports).then(() => {
          editor.on("change", this.onLatexChange); // it doesn't work as @change dunno why
          editor.setOptions({
            wrap: true,

            mode: 'brace/mode/latex',
            theme: 'ace/theme/tomorrow_night'
          });
        });
    },
    copyLatex() {
      const setCopyStatusToNull = () => (this.copyStatus = null);

      this.$copyText(this.body.latex).then(
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
      localStorage.setItem(this.localStorageKey, json);
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
    right: 0;

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

<!-- ace editors -->
<style lang="scss">
.md-list {
  padding: 0;
}

.md-menu-content-container {
  .md-optgroup:first-child { // light themes
    background-color: #ccc;

    .md-subheader,
    .md-list-item>button {
      color: #333;
    }
  }

  .md-optgroup:last-child { // dark themes
    background-color: #333;

    .md-subheader,
    .md-list-item>button {
      color: #ccc;
    }
  }
}
</style>
