<template>
  <div class="ph-latex">
    <div class="ph-latex-editor">
      <span v-if="body.created_date">Восстановлен LaTeX от {{body.restored}}</span>

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
      require('brace/theme/tomorrow_night');
      require('brace/snippets/latex');

      editor.on('change', this.onLatexChange); // it doesn't work as @change dunno why
      editor.setOption("wrap", true)
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
