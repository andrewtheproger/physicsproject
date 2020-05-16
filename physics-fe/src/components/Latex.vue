<template>
  <div class="ph-latex">
    <md-field class="ph-input">
      <md-textarea cols="30" rows="15" v-model.trim="latex"> </md-textarea>
    </md-field>

    <vue-mathjax class="ph-mathjax" :formula="this.latex"></vue-mathjax>
  </div>
</template>

<script>
import VueMathjax from "./VueMathJax/vueMathJax";
export default {
  name: "Latex",
  components: {
    VueMathjax
  },
  data() {
    return {
      latex: "Привет, это текст на $ \\LaTeX $, да. "
    };
  },
  methods: {}
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
