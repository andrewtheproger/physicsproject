<template>
  <div class="ph-latex">
    <md-field class="ph-input">
      <md-textarea
        cols="30"
        rows="15"
        @change="onLatexChange"
        v-model.trim="latex"
      >
      </md-textarea>
      <md-button
        class="md-dense md-icon-button ph-latex-copy-button"
        @click="this.copyLatex"
      >
        <md-icon :class="this.getCopyStatusClass">file_copy</md-icon>
      </md-button>
    </md-field>

    <vue-mathjax class="ph-mathjax" :formula="this.latex"></vue-mathjax>
  </div>
</template>

<script>
import VueMathjax from "./VueMathJax/vueMathJax";
const latexLocalStorageKey = "ph-3800-latex-input";
export default {
  name: "Latex",
  components: {
    VueMathjax
  },
  data() {
    return {
      latex:
        localStorage.getItem(latexLocalStorageKey) ||
        "Привет, это текст на $ \\LaTeX $, да. ",
      copyStatus: null
    };
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
      localStorage.setItem(latexLocalStorageKey, this.latex || "");
    }
  }
};
</script>

<style scoped lang="scss">
@import "../config/variables.scss";
.ph-latex {
  display: flex;
  padding: 1em;

  .ph-latex-copy-button {
    position: absolute;
    bottom: 0;
    right: 0;

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

    background-color: var(--background-primary-color);
    color: var(--foreground-primary-color);
  }
}
</style>
