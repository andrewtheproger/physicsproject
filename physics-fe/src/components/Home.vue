<template>
  <div>
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
        <Task :task="task" />
      </li>
    </ul>
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

.ph-tasks {
  list-style: none;
}
</style>
