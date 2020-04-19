<template>
  <div>
    <form class="ph-search-form" v-on:submit.prevent="submit">
        <md-field>
          <label>{{numberExample}}</label>
          <md-input v-model="number" :disabled="this.sending"></md-input>
        </md-field>
        
        <md-button type="submit" class="md-icon-button md-primary" :disabled="this.sending">
          <md-icon>search</md-icon>
        </md-button>
    </form>

    <md-progress-bar md-mode="indeterminate" v-if="this.sending" />

    <ul class="ph-tasks" v-if="this.tasks">
      <li v-for="task in this.tasks" :key="task.id">
        <Task :task="task" />
      </li>
    </ul>

    <div class="ph-nothing-found" v-if="this.tasks && this.tasks.length === 0">
      Ничего не найдено.
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import config from '../config/api'
import axios from "axios";
import Task from "./Task"

export default {
  name: "Home",
  components: {
    Task
  },

  data() {
    return {
      number: null,
      tasks: null,
      numberExample: '2.15...',
      numberExampleInterval: null,
      sending: false
    };
  },

  created() {
    this.numberExampleInterval = setInterval(this.setNewNumberExample, 1000);
  },
  beforeDestroy() {
    clearInterval(this.numberExampleInterval);
  },

  methods: {
    getRandomInt(min, max) { return Math.floor(Math.random() * (max - min) + min) },

    setNewNumberExample() {
      const lhs = this.getRandomInt(1, 12)
      const rhs = this.getRandomInt(1, 200)
      this.numberExample = lhs + "." + rhs + "..."
    },

    async submit() { 
      this.sending = true
      await this.getTaskByNumber(this.number)
      this.sending = false
    },

    async getTaskByNumber(number) {
      let url = config.apiPrefix + "/tasks"

      if (number) {
        url += "?filter_by_number=" + number
      }

      await axios({
        url: url,
        method: "GET",
      }).then(
        result => {
          this.tasks = result.data
        },
        error => {
          console.log(error);
          this.tasks = []
        }
      );
    },
  },
};
</script>

<style scoped lang="scss">
.ph-nothing-found {
  margin: 1em;
  color: white;
}

.ph-search-form {
  margin: 2em 1em 0 1em;
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

    input.md-input {
      -webkit-text-fill-color: white;
    }
  }
}

.ph-tasks {
  list-style: none;
}
</style>
