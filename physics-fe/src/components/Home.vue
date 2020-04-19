<template>
  <div class="hello">

    <form class="search-form" v-on:submit.prevent="submit">
        <md-field>
          <label>2.15...</label>
          <md-input v-model="number"></md-input>
        </md-field>
        
        <md-button type="submit" class="md-icon-button md-primary">
          <md-icon>search</md-icon>
        </md-button>
    </form>

    <ul class="ph-tasks">
      <li v-for="task in this.tasks" :key="task.id">
        <h3>3800.{{ task.number }}</h3>

        <div v-for="formula in task.body.latex.split('\n')" :key="formula">
          <vue-mathjax :formula="formula"></vue-mathjax>
        </div>

        <ul class="ph-task-images">
          <li>
            <md-content v-for="href in task.body.image_hrefs" :key="href">
              <img :src="href" alt="Task image" />
            </md-content>
          </li>
        </ul>

        <div v-if="task.hints.length">
          <h4>Идея решения</h4>

          <ul class="ph-tasks-hints">
            <li v-for="hint in task.hints" :key="hint.id">
              <div v-for="formula in hint.body.latex.split('\n')" :key="formula">
                <vue-mathjax :formula="formula"></vue-mathjax>
              </div>

              <ul class="ph-tasks-hints-images">
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
      </li>
    </ul>

  </div>
</template>

<script>
/* eslint-disable */
import config from '../config/api'
import axios from "axios";

export default {
  name: "HelloWorld",

  data() {
    return {
      number: null,
      tasks: []
    };
  },

  methods: {
    async submit() { this.getTaskByNumber(this.number) },

    async getTaskByNumber(number) {
      await axios({
        url: config.apiPrefix + "/tasks",
        method: "GET",
      }).then(
        result => {
          this.tasks = result.data
        },
        error => {
          console.log(error);
        }
      );
    },
  },
};
</script>

<style scoped lang="scss">
.search-form {
  margin: 2em;
  display: flex;

  .md-button.md-primary {
    background-color: #555;

    i {
      color: #ccf;
    }
  }

  .md-field {
    border-bottom: 1px solid #ccc;

    label {
      padding-left: 1em;
      color: #555;
    }
  }
}

.ph-tasks-hints,
.ph-tasks {
  color: white;

  list-style: none;

  h3 {
    text-decoration: underline;
  }

  .ph-tasks-hints-images,
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
  }
}
</style>
