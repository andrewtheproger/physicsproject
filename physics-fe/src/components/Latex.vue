<template>
  <div class="ph-latex">
    <div class="ph-latex-editor">
      <span v-if="body.created_date">Восстановлен LaTeX от {{body.restored}}</span>

      <editor v-model="body.latex"
              @init="editorInit"
              lang="latex"
              theme="tomorrow_night"
              width="100%"
              height="100%"/>

      <md-button
        class="md-dense md-icon-button ph-latex-copy-button"
        @click="this.copyLatex"
      >
        <md-icon :class="this.getCopyStatusClass">file_copy</md-icon>
      </md-button>
    </div>

    <vue-mathjax class="ph-mathjax" :formula="this.body.latex"></vue-mathjax>
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
      body: {},
      copyStatus: null
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

  .ph-latex-editor {
    position: relative;
    min-width: 50%;
    min-height: 15em;
  }

  .ph-latex-copy-button {
    position: absolute;
    bottom: 0;
    right: 3em;

    opacity: 0.3;

    transition: all 0.3s ease;

    .md-icon:hover {
      opacity: 0.8;
    }
  }

  .ph-input {
    border: 1px solid var(--foreground-primary-color);

    textarea {
      max-height: inherit;
    }
  }

  .ph-input,
  .ph-mathjax {
    width: 50%;
    margin: 1em;
    max-height: 75vh;
    overflow: auto;

    background-color: var(--background-primary-color);
    color: var(--foreground-primary-color);
  }
}
</style>
