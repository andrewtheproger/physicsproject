<template>
  <div class="ph-latex">
    <md-field class="ph-input">
      <md-textarea cols="30" rows="15"
                   @change="onLatexChange"
                   v-model.trim="latex"> </md-textarea>
    </md-field>

    <vue-mathjax class="ph-mathjax" :formula="this.latex"></vue-mathjax>
  </div>
</template>

<script>
import VueMathjax from "./VueMathJax/vueMathJax";
const latexLocalStorageKey = 'ph-3800-latex-input';
export default {
  name: "Latex",
  components: {
    VueMathjax
  },
  data() {
    return {
      latex: localStorage.getItem(latexLocalStorageKey) || "Привет, это текст на $ \\LaTeX $, да. "
    };
  },
  methods: {
    onLatexChange() {
      localStorage.setItem(latexLocalStorageKey, this.latex || '')
    }
  }
};
</script>

<style scoped lang="scss">
@import "../config/variables.scss";
.ph-latex {
  display: flex;
  padding: 1em;

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
