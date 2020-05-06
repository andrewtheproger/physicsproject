<template>
  <div class="ph-latex">
    <md-textarea
        cols="30"
        rows="15"
        v-model.trim="latex"
        class="ph-input"
    >
    </md-textarea>

    <vue-mathjax
        class="ph-mathjax"
        :formula="this.latex"
    ></vue-mathjax>
  </div>
</template>

<script>
export default {
    name: "Latex",
    data() {
      return {
          latex: "Привет, это текст на $ \\LaTeX $, да. ",
      }
    },
    methods: {

    }
}
</script>

<style scoped lang="scss">
@import "../config/variables.scss";
.ph-latex {
  display: flex;
  padding: 1em;

  .ph-input,
  .ph-mathjax {
    width: 50%;
    margin: 1em;

    background-color: var(--background-primary-color);
    color: var(--foreground-primary-color);
  }
}
</style>
