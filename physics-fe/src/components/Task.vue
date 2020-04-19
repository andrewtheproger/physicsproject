<template>
  <div class="ph-task" v-on:keyup.escape="cl">
    <h3>3800.{{ task.number }}</h3>

    <div v-for="formula in task.body.latex.split('\n')" :key="formula">
      <vue-mathjax :formula="formula"></vue-mathjax>
    </div>

    <ul class="ph-task-images">
      <li>
        <img v-gallery:task-images v-for="href in task.body.image_hrefs" :key="href" :src="href" />
      </li>
    </ul>

    <div v-if="task.hints.length">
      <h4>Идея решения</h4>

      <ul class="ph-task-hints">
        <li v-for="hint in task.hints" :key="hint.id">
          <div v-for="formula in hint.body.latex.split('\n')" :key="formula">
            <vue-mathjax :formula="formula"></vue-mathjax>
          </div>

          <ul class="ph-task-hints-images">
            <li>
              <md-content v-for="href in hint.body.image_hrefs" :key="href">
                <img :src="href" alt="Task image" />
              </md-content>
            </li>
          </ul>
        </li>
      </ul>
    </div>
    <div v-else>
      Подсказок к решению пока нет.
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import config from '../config/api'
import axios from "axios";
import Task from './Task'

export default {
  name: "Task",
  props: ['task'],
  methods: {
    cl() {
      console.log('a')
      $imgVuer.close()
    }
  }
};
</script>

<style scoped lang="scss">
.ph-task-hints,
.ph-task {
  color: white;

  list-style: none;

  h3 {
    text-decoration: underline;
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
      height: 200px;
      filter: invert(7%);

      &:hover {
        cursor: pointer;
        filter: invert(0%);
      }
    }
  }
}
</style>
