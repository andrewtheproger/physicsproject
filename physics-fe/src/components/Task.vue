<template>
  <div class="ph-task" v-on:keyup.escape="cl">
    <h3>3800.{{ task.base_number }}.{{ task.task_number }}</h3>
    <div classs="ph-text">
      <vue-mathjax :formula="task.body.latex"></vue-mathjax>
    </div>
    <ul class="ph-task-images">
      <li v-for="image in task.body.images" :key="image.id">
        <img v-gallery:task-images :src="image.url" />
      </li>
    </ul>

    <div v-if="task.hints.length">
      <h4>Идея решения</h4>

      <ul class="ph-task-hints">
        <li v-for="hint in task.hints" :key="hint.id">
          <div
            class="ph-latex"
            v-for="formula in hint.body.latex.split('\n')"
            :key="formula"
          >
            <vue-mathjax :formula="formula"></vue-mathjax>
          </div>

          <ul class="ph-task-hints-images">
            <li>
              <md-content v-for="id in hint.body.image_ids" :key="id">
                <img :src="id" alt="Task image" />
              </md-content>
            </li>
          </ul>
        </li>
      </ul>
    </div>
    <div class="ph-task-no-hints-available" v-else>
      Подсказок к решению пока нет.
    </div>
  </div>
</template>

<script>
import VueMathjax from "./VueMathJax/vueMathJax";

export default {
  name: "Task",
  components: {
      VueMathjax
  },
  props: ['task']
};
</script> 

<style scoped lang="scss">
@import "../config/variables.scss";

.ph-task-no-hints-available {
  font-size: 80%;
}

.ph-task-hints,
.ph-task {
  padding-left: 0;
  list-style: none;

  h3 {
    margin-top: 3em;
    text-decoration: bold;
  }

  .ph-latex {
    margin-left: 2em;
  }

  .ph-task-hints-images,
  .ph-task-images {
    list-style: none;
    padding-left: 0;

    .md-content {
      width: 200px;
      height: 160px;
      display: inline-flex;
      justify-content: center;
      align-items: center;

      margin: 0.5em;
    }

    img {
      max-height: 200px;
      filter: invert(7%);

      &:hover {
        cursor: pointer;
        filter: invert(0%);
      }
    }
  }
}
</style>
