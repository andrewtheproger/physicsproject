<template>
  <div>
    <div class="ph-search-controls">
      <form class="ph-search-by-base-form" v-on:submit.prevent="submitByBase">
        <md-field>
          <label for="ph-base-number">Раздел</label>
          <md-select id="ph-base-number" v-model="selectedBase" @md-selected="submitByBase">
            <md-option value="">[ не выбран ]</md-option>
            <md-option value="1">1. Кинематика</md-option>
            <md-option value="2">2. Динамика</md-option>
            <md-option value="3">3. Работа</md-option>
            <md-option value="4">4. Статика</md-option>
            <md-option value="5">5. Гравитация</md-option>
            <md-option value="6">6. Механическое колебания и волны</md-option>
            <md-option value="7">7. Динамика ТТ</md-option>
            <md-option value="8">8. Гидростатика</md-option>
            <md-option value="9">9. МКТ</md-option>
            <md-option value="10">10. Термодинакмика</md-option>
            <md-option value="11">11. Электростатика</md-option>
            <md-option value="12">12. Постоянный ток</md-option>
            <md-option value="13">13. Магнетизм</md-option>
            <md-option value="14">14. Электрические колебания и волны</md-option>
            <md-option value="15">15. Геометрическая оптика</md-option>
            <md-option value="16">16. Фотометрия</md-option>
            <md-option value="17">17. Волновая оптика</md-option>
            <md-option value="18">18. Теория относительности</md-option>
            <md-option value="19">19. Квант</md-option>
            <md-option value="20">20. Атомная физика</md-option>
            <md-option value="21">21. Ядерная физика</md-option>
          </md-select>
        </md-field>
      </form>

      <form class="ph-search-form" v-on:submit.prevent="submitByNumber">
        <md-autocomplete
          v-model="number"
          :md-options="existing_numbers"
          @md-selected="submitByNumber"
          md-dense
          :disabled="sending"
        >
          <transition name="slide-fade" mode="out-in">
            <label :key="numberExample">{{ numberExample }}</label>
          </transition>
        </md-autocomplete>

        <md-button
          type="submit"
          class="md-icon-button md-primary"
          :disabled="sending"
        >
          <md-icon>search</md-icon>
        </md-button>
      </form>

      <md-progress-bar md-mode="indeterminate" v-if="sending" />
    </div>

    <Message
      v-if="isHttpFailed"
      :text="'Произошла ошибка: ' + httpFailed.message"
      severity="error"
    ></Message>

    <nav v-if="page.count && !number">
      <v-pagination
        v-model="page.currentPage"
        :page-count="page.count"
        @input="changePage"
      ></v-pagination>
    </nav>

    <ul class="ph-tasks" v-if="tasks">
      <li v-for="task in tasks" :key="task.id">
        <Task :task="task" />
      </li>
    </ul>

    <Message
      v-if="tasks && tasks.length === 0"
      text="Ничего не найдено"
      severity="warning"
    ></Message>
  </div>
</template>

<script>
import config from "../config/api.js";
import http_helper from "../lib/http";
import BuildUrl from "build-url";

const vPagination = () =>
  import(/* webpackChunkName: "vue-plain-pagination" */ "vue-plain-pagination");
const Task = () => import(/* webpackChunkName: "components_Task" */ "./Task");
const Message = () =>
  import(
    /* webpackChunkName: "components_Message_Message" */ "./Message/Message"
  );
const axios = () => import(/* webpackChunkName: "axios" */ "axios");

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
      selectedBase: null,
      page: {
        currentPage: 1,
        itemsPerPage: 5,
        count: null,
      }
    };
  },

  created() {
    this.numberExampleInterval = setInterval(this.setNewNumberExample, 1000);
    const url = config.apiPrefix + "/tasks/predicate_numbers";

    axios().then(ax =>
      ax
        .request({
          url: url,
          method: "GET"
        })
        .then(
          result => {
            this.existing_numbers = result.data.map(
              x => x.base_number + "." + x.task_number
            );
          },
          error => {
            throw error;
          }
        )
    );
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

    async submitByBase() {
      // russian up call from @md-selected on md-select that is triggered by setting this.selectedBase to null in submitByNumber method
      if (this.selectedBase === "") {
        return;
      }

      this.sending = true;
      await this.getTaskByBase(this.selectedBase).then(() => {
        this.sending = false;
        this.number = "";
        this.page.currentPage = 1;
      });
    },

    async submitByNumber() {
      this.sending = true;
      this.getTaskByNumber(this.number).then(() => {
        this.sending = false;
        this.page.currentPage = 1;
        this.selectedBase = "";
      });
    },

    async changePage(page) {
      let url;

      if (this.selectedBase) {
        url = BuildUrl(config.apiPrefix, {
          path: "tasks",
          queryParams: {
            page: page - 1,
            count: this.page.itemsPerPage.toString(),
            filter_by_base_number: this.selectedBase
          }
        });
      } else {
        url = BuildUrl(config.apiPrefix, {
          path: "tasks",
          queryParams: {
            page: page - 1,
            count: this.page.itemsPerPage.toString()
          }
        });
      }

      await this.getTasksByUrl(url);
    },

    async getTaskByBase(base) {
      const url = BuildUrl(config.apiPrefix, {
        path: "tasks",
        queryParams: {
          page: "0",
          count: this.page.itemsPerPage,
          filter_by_base_number: base
        }
      });

      await this.getTasksByUrl(url);
    },

    async getTasksByUrl(url) {
      axios().then(ax =>
        ax
          .request({
            url: url,
            method: "GET"
          })
          .then(
            result => {
              this.isHttpFailed = false;
              this.tasks = result.data.items;
              this.page.count = Math.floor(
                result.data.total / this.page.itemsPerPage
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
          )
      );
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

      await this.getTasksByUrl(url);
    }
  }
};
</script>

<style lang="scss">
@import "../config/mixins";
// for some reason the pagination could not access scoped classes
// todo
.pagination {
  display: flex;
  list-style: none;

  @media (max-width: 756px) {
    padding: 0;
    justify-content: center;
  }

  li:first-child,
  li:last-child {
    display: none;
  }

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

.ph-search-controls {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: baseline;
  margin: 2em 1em 0 1em;
}

.ph-search-by-base-form,
.ph-search-form {
  padding: 1em;
  width: 45%;
}

.ph-search-form {
  display: flex;
  align-items: baseline;

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
