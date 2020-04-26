<template>
  <div>
    <form class="ph-search-form" v-on:submit.prevent="submit">
      <md-field>
        <transition name="slide-fade" mode="out-in">
          <label :key="numberExample">{{ numberExample }}</label>
        </transition>

        <md-input v-model="number" :disabled="this.sending"></md-input>
      </md-field>

      <md-button
        type="submit"
        class="md-icon-button md-primary"
        :disabled="this.sending"
      >
        <md-icon>search</md-icon>
      </md-button>
    </form>

    <md-progress-bar md-mode="indeterminate" v-if="this.sending" />

    <ul class="ph-tasks" v-if="this.tasks">
      <li v-for="task in this.tasks" :key="task.id">
        <div v-if="!task.text">
          {{
            (task.text =
              "2.52 На материальную точку, масса которой равна $ m= 600 г$, действуют две силы $ F_1=2$ Н и $ F_2=3$ Н. Найти угол $ \\alpha $ между этими силами, если под их действием материальная точка движется с ускорением $ a = 8 м/с^2 $? При каких условиях её движение под действием этих сил будет прямоугольным?")
          }}
        </div>
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
import config from "../config/api";
import axios from "axios";
import Task from "./Task";

export default {
  name: "Home",
  components: {
    Task,
  },

  data() {
    return {
      number: null,
      tasks: null,
      numberExample: "2.15...",
      numberExampleInterval: null,
      sending: false,
    };
  },

  created() {
    this.numberExampleInterval = setInterval(this.setNewNumberExample, 1000);
  },
  beforeDestroy() {
    clearInterval(this.numberExampleInterval);
  },

  methods: {
    getRandomInt(min, max) {
      return Math.floor(Math.random() * (max - min) + min);
    },

    setNewNumberExample() {
      const lhs = this.getRandomInt(1, 12);
      const rhs = this.getRandomInt(1, 200);
      this.numberExample = lhs + "." + rhs + "...";
    },

    async submit() {
      this.sending = true;
      await this.getTaskByNumber(this.number);
      this.sending = false;
    },

    async getTaskByNumber(number) {
      let url = config.apiPrefix + "/tasks";

      if (number) {
        url += "?filter_by_number=" + number;
      }

      await axios({
        url: url,
        method: "GET",
      }).then(
        (result) => {
          this.tasks = result.data;
        },
        (error) => {
          console.log(error);
          this.tasks = [];
        }
      );
    },
  },
};
</script>

<style scoped lang="scss">
@import "../config/variables.scss";

.slide-fade-enter-active {
  transition: all 0.3s ease;
}

.slide-fade-leave-active {
  transition: all 0.3s ease;
}

.slide-fade-enter {
  transform: translateY(10px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

.ph-nothing-found {
  margin: 1em;
  color: $primary-fg-color;
}

.ph-search-form {
  margin: 2em 1em 0 1em;
  display: flex;

  .md-button.md-primary {
    background-color: $secondary-bg-color;

    i {
      color: $secondary-fg-color;
    }
  }

  .md-field,
  .md-field.md-theme-default.md-focused,
  .md-field.md-theme-default.md-focused,
  .md-field.md-theme-default.md-has-value {
    border-bottom: 1px solid $primary-fg-color;

    input.md-input {
      color: inherit;
      -webkit-text-fill-color: $primary-fg-color;
    }

    label {
      padding-left: 1em;
      color: $secondary-bg-color;
    }
  }
}

.ph-tasks {
  list-style: none;
}
</style>
