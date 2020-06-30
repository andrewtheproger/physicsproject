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

    <Message
      v-if="this.isHttpFailed"
      :text="'Произошла ошибка: ' + this.httpFailed.message"
      severity="error"
    ></Message>

    <nav v-if="page.count && !number">
      <v-pagination
        v-model="page.currentPage"
        :page-count="page.count"
        :labels="page.paginationAnchorTexts"
        @input="changePage"
      ></v-pagination>
    </nav>

    <ul class="ph-tasks" v-if="this.tasks">
      <li v-for="task in this.tasks" :key="task.id">
        <Task :task="task" />
      </li>
    </ul>

    <Message
      v-if="this.tasks && this.tasks.length === 0"
      text="Ничего не найдено"
      severity="warning"
    ></Message>
  </div>
</template>

<script>
import vPagination from "vue-plain-pagination";
import config from "../config/api";
import axios from "axios";
import Task from "./Task";
import http_helper from "../lib/http";
import Message from "./Message/Message";
import BuildUrl from "build-url";

export default {
  name: "Home",
  components: {
    Task,
    vPagination,
    Message
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
      httpFailed: null,
      page: {
        currentPage: 1,
        itemsPerPage: 5,
        count: null,
        paginationAnchorTexts: {
          first: "Начало",
          prev: "Пред.",
          next: "След.",
          last: "Конец"
        }
      }
    };
  },

  created() {
    this.numberExampleInterval = setInterval(this.setNewNumberExample, 1000);
    const url = config.apiPrefix + "/tasks/predicate_numbers";

    axios({
      url: url,
      method: "GET"
    }).then(
      result => {
        this.existing_numbers = result.data.map(
          x => x.base_number + "." + x.task_number
        );
      },
      error => {
        console.log(error);
      }
    );
  },
  beforeDestroy() {
    clearInterval(this.numberExampleInterval);
  },
  methods: {
    async changePage(page) {
      const url = BuildUrl(config.apiPrefix, {
        path: "tasks",
        queryParams: {
          page: page,
          count: this.page.itemsPerPage
        }
      });

      await axios({
        url: url,
        method: "GET"
      }).then(
        result => {
          this.isHttpFailed = false;
          this.tasks = result.data;
          this.page.count = Math.floor(
            this.existing_numbers.length / this.page.itemsPerPage
          );
        },
        error => {
          this.isHttpFailed = true;

          const data = error.response.data;

          this.httpFailed = {
            http_code: error.response.code,
            internal_code: data.code,
            message: http_helper.get_error_message(data.code)
          };
          this.tasks = [];
        }
      );
    },

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
      let url;

      if (number) {
        const [base_number, task_number] = number.split(".");

        url = BuildUrl(config.apiPrefix, {
          path: "tasks",
          queryParams: {
            page: "0",
            count: this.page.itemsPerPage,
            filter_by_base_number: base_number,
            filter_by_task_number: task_number
          }
        });
      } else {
        url = BuildUrl(config.apiPrefix, {
          path: "tasks",
          queryParams: {
            page: "0",
            count: this.page.itemsPerPage
          }
        });
      }

      await axios({
        url: url,
        method: "GET"
      }).then(
        result => {
          this.isHttpFailed = false;
          this.tasks = result.data;
          this.page.count = Math.floor(
            this.existing_numbers.length / this.page.itemsPerPage
          );
          this.page.currentPage = 1;
        },
        error => {
          this.isHttpFailed = true;

          const data = error.response.data;

          this.httpFailed = {
            http_code: error.response.code,
            internal_code: data.code,
            message: http_helper.get_error_message(data.code)
          };
          this.tasks = [];
        }
      );
    }
  }
};
</script>

<style lang="scss">
@import "../config/variables.scss";
// for some reason the pagination could not access scoped classes
// todo
.pagination {
  display: flex;
  list-style: none;

  .pagination-item {
    min-width: 1.7em;
    text-align: center;

    &.pagination-item--active .pagination-link {
      border-bottom-color: var(--foreground-secondary-color);
    }

    .pagination-link {
      background-color: var(--background-secondary-color);
      color: var(--foreground-primary-color);
      padding: 0.5em;
      border: none;
      border-bottom: 1px solid var(--background-secondary-color);

      &.pagination-link--disable {
        background-color: var(--background-primary-color);
        color: var(--foreground-primary-color);
        cursor: not-allowed;
      }

      &:not(.pagination-link--disable):hover {
        cursor: pointer;
        background-color: alpha(var(--background-secondary-color), 0.2);
      }
    }

    // dots in between
    span.pagination-link.pagination-link--disable {
      display: inline-block;
      letter-spacing: normal;
      line-height: normal;
      background-color: var(--background-primary-color);

      border: none;
    }
  }

  .pagination-item:nth-child(1),
  .pagination-item:nth-child(2),
  .pagination-item:nth-last-child(1),
  .pagination-item:nth-last-child(2) {
    margin: 0 0.5em;
    width: inherit;
  }

  .pagination-item:nth-child(1) {
    margin-left: 0;
  }
}
</style>

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
}

.ph-error-message {
  color: var(--foreground-error-color);
  margin: 0 1em;
}

.ph-search-form {
  margin: 2em 1em 0 1em;
  display: flex;

  .md-field,
  .md-field.md-theme-default.md-focused,
  .md-field.md-theme-default.md-focused,
  .md-field.md-theme-default.md-has-value {
    label {
      padding-left: 1em;
    }
  }
}

.ph-tasks {
  list-style: none;
  color: var(--foreground-primary-color);
}
</style>
