<template>
  <div>
    <form class="ph-search-form" v-on:submit.prevent="submit">
      <md-autocomplete
        v-model="number"
        :md-options="existing_numbers"
        md-dense
        :disabled="this.sending"
      >
        <transition name="slide-fade" mode="out-in">
          <label :key="numberExample">{{ numberExample }}</label>
        </transition>
      </md-autocomplete>

      <md-button
        type="submit"
        class="md-icon-button md-primary"
        :disabled="this.sending"
      >
        <md-icon>search</md-icon>
      </md-button>
    </form>

    <md-progress-bar md-mode="indeterminate" v-if="this.sending" />

    <div class="ph-error-message" v-if="isHttpFailed">
      Произошла ошибка: {{ this.flowFailed.message }}
    </div>

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
      existing_numbers: [],
      isHttpFailed: false,
      httpFailed: null
    };
  },

  created() {
    this.numberExampleInterval = setInterval(this.setNewNumberExample, 1000);
    const url = config.apiPrefix + "/tasks/predicate_numbers";

    axios({
      url: url,
      method: 'GET'
    }).then(
      result => {
        this.existing_numbers = result.data.map(x => x.base_number + '.' + x.task_number);
      },
      error => {
        console.log(error);
      }
    )
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
      console.log(this.$store.getters.get_jwt);
      await this.getTaskByNumber(this.number);
      this.sending = false;
    },

    get_error_message(code) {
      switch (code) {
        case 1:
          return 'разработчик сделал что-то не так';
        default:
          throw 'This should not happens';
      }
    },

    async getTaskByNumber(number) {
      let url = config.apiPrefix + "/tasks";

      if (number) {
        const [base_number, task_number] = number.split('.');
        url += "?filter_by_base_number=" + base_number; // todo make it looks ok
        url += "&filter_by_task_number=" + task_number;
      }

      await axios({
        url: url,
        method: "GET",
      }).then(
        (result) => {
          this.isHttpFailed = false;
          this.tasks = result.data;
        },
        (error) => {
          this.isHttpFailed = true;

          const data = error.response.data;

          this.httpFailed = {
            http_code: error.response.code,
            internal_code: data.code,
            message: this.get_error_message(data.code),
          };
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

.ph-error-message {
  color: red;
  margin: 0 1em;
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
