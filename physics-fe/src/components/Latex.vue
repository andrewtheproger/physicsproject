<template>
  <div class="ph-latex">
    <div class="ph-latex-editor">
      <div>
        <span v-if="body.created_date">Восстановлен LaTeX от {{body.restored}}</span>

      </div>

      <editor v-model="body.latex"
              @init="editorInit"
              lang="latex"
              ref='myEditor'
              theme="tomorrow_night"
              font-size="40px"
              width="100%"
              height="100%"/>

      <div class="ph-latex-editor-controls">
        <span v-if="this.aceZoom.current !== 100">{{this.aceZoom.current}} %</span>

        <md-button
          class="md-dense md-icon-button"
          @click="this.copyLatex"
        >
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
      <md-field>
        <label for="ace-editor-theme">Тема редактора</label>
        <md-select
          v-model="colorSchema"
          name="ace-editor-theme"
          id="ace-editor-theme"
          @md-selected="setColorSchema"
        >
          <md-optgroup label="Светлые">
            <md-option value="chrome">Chrome</md-option>
            <md-option value="clouds">Clouds</md-option>
            <md-option value="crimson_editor">Crimson_editor</md-option>
            <md-option value="dawn">Dawn</md-option>
            <md-option value="dreamweaver">Dreamweaver</md-option>
            <md-option value="eclipse">Eclipse</md-option>
            <md-option value="github">Github</md-option>
            <md-option value="iplastic">Iplastic</md-option>
            <md-option value="katzenmilch">Katzenmilch</md-option>
            <md-option value="kuroir">Kuroir</md-option>
            <md-option value="solarized_light">Solarized_light</md-option>
            <md-option value="sqlserver">Sqlserver</md-option>
            <md-option value="textmate">Textmate</md-option>
            <md-option value="tomorrow">Tomorrow</md-option>
            <md-option value="xcode">Xcode</md-option>
          </md-optgroup>
          <md-optgroup label="Тёмные">
            <md-option value="ambiance">Ambiance</md-option>
            <md-option value="chaos">Chaos</md-option>
            <md-option value="clouds_midnight">Clouds_midnight</md-option>
            <md-option value="cobalt">Cobalt</md-option>
            <md-option value="dracula">Dracula</md-option>
            <md-option value="gob">Gob</md-option>
            <md-option value="gruvbox">Gruvbox</md-option>
            <md-option value="idle_fingers">Idle_fingers</md-option>
            <md-option value="kr_theme">Kr_theme</md-option>
            <md-option value="merbivore">Merbivore</md-option>
            <md-option value="merbivore_soft">Merbivore_soft</md-option>
            <md-option value="mono_industrial">Mono_industrial</md-option>
            <md-option value="monokai">Monokai</md-option>
            <md-option value="pastel_on_dark">Pastel_on_dark</md-option>
            <md-option value="solarized_dark">Solarized_dark</md-option>
            <md-option value="terminal">Terminal</md-option>
            <md-option value="tomorrow_night">Tomorrow_night</md-option>
            <md-option value="tomorrow_night_blue">Tomorrow_night_blue</md-option>
            <md-option value="tomorrow_night_bright">Tomorrow_night_bright</md-option>
            <md-option value="tomorrow_night_eighties">Tomorrow_night_eighties</md-option>
            <md-option value="twilight">Twilight</md-option>
            <md-option value="vibrant_ink">Vibrant_ink</md-option>
          </md-optgroup>
        </md-select>
      </md-field>

      <vue-mathjax
        class="ph-mathjax-render"
        :formula="this.body.latex"
      ></vue-mathjax>

      <div class="ph-mathjax-controls">
        <md-button class="md-dense md-icon-button" @click="this.onMathjaxZoomIn">
          <md-icon>zoom_in</md-icon>
        </md-button>

        <md-button class="md-dense md-icon-button" @click="this.onMathjaxZoomOut">
          <md-icon>zoom_out</md-icon>
        </md-button>

        <span v-if="this.mathjaxZoom.current !== 100">{{this.mathjaxZoom.current}} %</span>
      </div>
    </div>
  </div>
</template>

<script>
import VueMathjax from "./VueMathJax/vueMathJax";
import config from "../config/api";
const latexLocalStorageKey = "ph-3800-latex-input";
export default {
  name: "Latex",
  components: {
    VueMathjax,
    editor: require('vue2-ace-editor'),
  },
  data() {
    return {
      body: {
        latex:
          localStorage.getItem(latexLocalStorageKey) ||
          "Привет, это текст на $ \\LaTeX $, да. ",
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
      )
    } else {
      this.body.restored = 'неизвестного числа'
    }
  },
  computed: {
    getCopyStatusClass() {
      if (this.copyStatus === null) {
        return "";
      }

      return this.copyStatus ? "ph-success" : "ph-failure";
    }
  },
  methods: {
    setColorSchema: function(e) {
      this.$refs.myEditor.editor.setTheme(`ace/theme/${e}`);
    },
    getMathjaxStyle: function() {
      return {
        fontSize: `${this.mathjaxZoom.current}%`
      }
    },
    onAceZoomIn: function() {
      if (this.aceZoom.current + this.aceZoom.step <= this.aceZoom.max) {
        this.aceZoom.current += this.aceZoom.step;
      }
      this.$refs.myEditor.editor.setFontSize(`${this.aceZoom.current}%`)
    },
    onAceZoomOut: function() {
      if (this.aceZoom.current - this.aceZoom.step >= this.aceZoom.min) {
        this.aceZoom.current -= this.aceZoom.step;
      }
      this.$refs.myEditor.editor.setFontSize(`${this.aceZoom.current}%`)
    },
    onMathjaxZoomIn: function() {
      if (this.mathjaxZoom.current + this.mathjaxZoom.step <= this.mathjaxZoom.max) {
        this.mathjaxZoom.current += this.mathjaxZoom.step;
      }
    },
    onMathjaxZoomOut: function() {
      if (this.mathjaxZoom.current + this.mathjaxZoom.step >= this.mathjaxZoom.min) {
        this.mathjaxZoom.current -= this.mathjaxZoom.step;
      }
    },
    editorInit: function (editor) {
      require('brace/ext/language_tools');
      require('brace/mode/latex');
      require('brace/snippets/latex');
      require('brace/theme/ambiance');
      require('brace/theme/chaos');
      require('brace/theme/chrome');
      require('brace/theme/clouds');
      require('brace/theme/clouds_midnight');
      require('brace/theme/cobalt');
      require('brace/theme/crimson_editor');
      require('brace/theme/dawn');
      require('brace/theme/dracula');
      require('brace/theme/dreamweaver');
      require('brace/theme/eclipse');
      require('brace/theme/github');
      require('brace/theme/gob');
      require('brace/theme/gruvbox');
      require('brace/theme/idle_fingers');
      require('brace/theme/iplastic');
      require('brace/theme/katzenmilch');
      require('brace/theme/kr_theme');
      require('brace/theme/kuroir');
      require('brace/theme/merbivore');
      require('brace/theme/merbivore_soft');
      require('brace/theme/mono_industrial');
      require('brace/theme/monokai');
      require('brace/theme/pastel_on_dark');
      require('brace/theme/solarized_dark');
      require('brace/theme/solarized_light');
      require('brace/theme/sqlserver');
      require('brace/theme/terminal');
      require('brace/theme/textmate');
      require('brace/theme/tomorrow');
      require('brace/theme/tomorrow_night');
      require('brace/theme/tomorrow_night_blue');
      require('brace/theme/tomorrow_night_bright');
      require('brace/theme/tomorrow_night_eighties');
      require('brace/theme/twilight');
      require('brace/theme/vibrant_ink');
      require('brace/theme/xcode');

      editor.on('change', this.onLatexChange); // it doesn't work as @change dunno why
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
@import "../config/variables.scss";
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
