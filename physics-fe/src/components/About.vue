<template>
  <div class="ph-about">
    <div>
      Проект посвящён книге "3800 задач по физике". Цели две:

      <ul>
        <li>Позволить быстро искать задачу по номеру,</li>
        <li>Сопроводить каждую задачу ответом, комментариями и подсказками.</li>
      </ul>

      Содержимое сайта перелицензировано под
      <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">
        <img
          alt="Лицензия Creative Commons"
          style="border-width:0"
          src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png"
        />
      </a>
    </div>

    <h2>
      Текущее состояние проекта

      <a
        class="ph-github-icon"
        href="https://github.com/andrewtheproger/physicsproject"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 1000 1000"
          width="2em"
          height="2em"
        >
          <path
            d="M512 0C229.25 0 0 229.25 0 512c0 226.25 146.69 418.13 350.16 485.81 25.59 4.69 34.94-11.12 34.94-24.62 0-12.19-.47-52.56-.72-95.31C242 908.81 211.91 817.5 211.91 817.5c-23.31-59.12-56.84-74.87-56.84-74.87-46.53-31.75 3.53-31.12 3.53-31.12 51.41 3.56 78.47 52.75 78.47 52.75 45.69 78.25 119.88 55.63 149 42.5 4.65-33 17.9-55.62 32.5-68.37-113.66-12.95-233.23-56.89-233.23-253.08 0-55.94 19.97-101.56 52.66-137.41-5.22-13-22.84-65.09 5.06-135.56 0 0 42.94-13.75 140.81 52.5 40.81-11.41 84.59-17.03 128.13-17.22 43.5.19 87.31 5.88 128.19 17.28 97.69-66.31 140.69-52.5 140.69-52.5 28 70.53 10.38 122.56 5.13 135.5 32.81 35.84 52.63 81.47 52.63 137.41 0 196.69-119.75 240-233.81 252.69 18.44 15.88 34.75 47 34.75 94.75 0 68.44-.69 123.63-.69 140.5 0 13.63 9.31 29.56 35.25 24.56C877.44 930 1024 738.13 1024 512 1024 229.25 794.75 0 512 0z"
          ></path>
        </svg>
      </a>
    </h2>
    <div class="ph-statistics">
      <div class="ph-statistic-block">
        <span>
          <span v-if="!this.last_commit_url">Загружаю...</span>

          <span v-if="this.last_commit_url">
            Последний коммит:
            <a :href="this.last_commit_url" target="_blank"
              >{{ this.last_commit_datetime_string }} {{ this.ago }}
            </a>
          </span>
        </span>

        <ul>
          <li>Всего пользователей: {{ this.statistics.users.length }}</li>
          <li>Всего задач: {{ this.formatTotalStatistics() }}</li>
          <li>
            Заполненность разделов:
            <ul>
              <li>{{ this.getParagraphStatistics(1) }}</li>
              <li>{{ this.getParagraphStatistics(2) }}</li>
              <li>{{ this.getParagraphStatistics(3) }}</li>
              <li>{{ this.getParagraphStatistics(4) }}</li>
              <li>{{ this.getParagraphStatistics(5) }}</li>
              <li>{{ this.getParagraphStatistics(6) }}</li>
              <li>{{ this.getParagraphStatistics(7) }}</li>
              <li>{{ this.getParagraphStatistics(8) }}</li>
              <li>{{ this.getParagraphStatistics(9) }}</li>
              <li>{{ this.getParagraphStatistics(10) }}</li>
              <li>{{ this.getParagraphStatistics(11) }}</li>
              <li>{{ this.getParagraphStatistics(12) }}</li>
              <li>{{ this.getParagraphStatistics(13) }}</li>
              <li>{{ this.getParagraphStatistics(14) }}</li>
              <li>{{ this.getParagraphStatistics(15) }}</li>
              <li>{{ this.getParagraphStatistics(16) }}</li>
              <li>{{ this.getParagraphStatistics(17) }}</li>
              <li>{{ this.getParagraphStatistics(18) }}</li>
              <li>{{ this.getParagraphStatistics(19) }}</li>
              <li>{{ this.getParagraphStatistics(20) }}</li>
              <li>{{ this.getParagraphStatistics(21) }}</li>
            </ul>
          </li>
        </ul>
      </div>

      <div class="ph-statistic-block ph-graphics">
        <div class="ph-graphic">
          <span class="ph-graphics-title">
            Количество зарегистрированных пользователей
          </span>

          <trend
            :data="getUsersStatistics()"
            :gradient="['#99cc99', '#339933']"
            auto-draw
            smooth
          >
          </trend>
        </div>

        <div class="ph-graphic">
          <span class="ph-graphics-title">
            Количество созданных задач
          </span>

          <trend
            :data="getTasksStatistics()"
            :gradient="['#99cc99', '#339933']"
            auto-draw
            smooth
          >
          </trend>
        </div>
        <div>
          <span>Активность пользователей:</span>
          <ul>
            <li v-for="result in this.grouped()" :key="result.creatorName">
              {{ result.creatorName }} - {{ result.count }}
            </li>
          </ul>
        </div>
      </div>

      <ul class="ph-statistic-block ph-targets">
        <li>
          <Message
            text="Создать интерфейс добавления задач"
            severity="success"
          ></Message>
        </li>
        <li>
          <Message
            text="Создать интерфейс добавления подсказок к задачам"
            severity="error"
          ></Message>
        </li>
        <li>
          <Message
            text="Перенести все задачи из 3800 к нам (~ 800/3800)"
            severity="warning"
          ></Message>
        </li>
        <li>
          <Message
            text="Сопроводить каждую задачу ответом и подсказкой"
            severity="error"
          ></Message>
        </li>
      </ul>
    </div>

    <h2>Как помочь проекту</h2>

    <div>
      Лучше всего - добавить задачу из 3800:

      <ul>
        <li>
          <a href="/#/" target="_blank">Найдите</a>, какой задачи у нас нет,
        </li>
        <li>
          Перейдите на
          <a href="/#/add" target="_blank">страницу добавления задачи</a> и
          добавьте её.
        </li>
      </ul>

      Мы записываем условие в формате
      <a href="https://ru.wikipedia.org/wiki/LaTeX" target="_blank">LaTeX</a> -
      этот формат позволяет удобно хранить и передавать формулы. LaTeX очень
      прост в освоении, основы таковы:

      <ul>
        <li>Русский текст пишется просто так,</li>
        <li>Формулы пишутся между символами доллара,</li>
        <li>Маленькие цифры снизу пишутся через _</li>
        <li>Степени пишутся через ^</li>
        <li>Сложные выражения обрамляются фигурными скобками</li>
        <li>
          Синтаксис LaTeX описан на
          <a
            href="https://ru.wikipedia.org/wiki/Википедия:Формулы"
            target="_blank"
            >этой странице</a
          >
        </li>
      </ul>

      Если вы можете в разработку - добро пожаловать на гитхаб.
    </div>

    <h2>Как не надо помогать проекту</h2>
    <div>
      <ul>
        <li>Не надо перечислять деньги</li>
        <li>Не надо предлагать разместить рекламу</li>
      </ul>
    </div>

    <h2>Полезные ссылки</h2>

    <ul>
      <li>
        <a href="https://www.mathway.com/ru/graph" target="_blank">
          Построение простых графиков
        </a>
      </li>
      <li>
        <a href="https://wolframalpha.com" target="_blank">
          Построение сложных графиков
        </a>
      </li>
      <li>
        <a
          href="https://github.com/andrewtheproger/physicsproject/blob/master/PATCHNOTES.md"
          target="_blank"
        >
          История разработки
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
import Message from "./Message/Message";
import Trend from "vuetrend";
import paragraps from "../config/3800";
import config from "../config/api.js";

const axios = () => import(/* webpackChunkName: "axios" */ "axios");

export default {
  name: "About",
  components: {
    Message,
    Trend
  },
  data() {
    return {
      ago: null,
      last_commit_url: null,
      last_commit_datetime_string: null,
      statistics: {
        users: [],
        tasks: []
      }
    };
  },
  methods: {
    formatTotalStatistics() {
      const currentTaskCount = this.statistics.tasks.length;
      const totalTaskCount = Object.values(paragraps).reduce(
        (acc, val) => acc + val.total || 0,
        0
      );
      return `${currentTaskCount} / ${totalTaskCount} (${Math.round(
        (currentTaskCount / totalTaskCount) * 100
      )}%)`;
    },
    grouped() {
      if (!this.statistics.tasks) {
        return [];
      }

      const a = this.statistics.tasks.reduce((acc, cur) => {
        acc[cur.creator.name] = [...(acc[cur.creator.name] || []), cur];
        return acc;
      }, {});

      const array = Object.entries(a);
      return array
        .map(x => ({
          creatorName: x[0],
          count: x[1].length
        }))
        .sort((lhs, rhs) => (lhs.count < rhs.count ? 1 : -1));
    },
    getParagraphStatistics(number) {
      const count = this.statistics.tasks.filter(x => x.base_number === number)
        .length;

      return `${number}. ${paragraps[number].title} - ${count} / ${
        paragraps[number].total
      } (${Math.round((count / paragraps[number].total) * 100)}%)`;
    },
    getTasksStatistics() {
      if (!this.statistics.tasks) {
        return [];
      }

      const registrations = this.statistics.tasks.map(x =>
        Math.round(x.created_date / (1000 * 60 * 60 * 24))
      ); // milliseconds * seconds * minutes * hours
      const startsAt = registrations[0];
      const endsAt = registrations[registrations.length - 1];
      let count = 1;
      const result = [];

      for (let i = startsAt; i < endsAt; i++) {
        count += registrations.filter(x => x === i).length;
        result.push(count);
      }

      return result;
    },
    getUsersStatistics() {
      if (!this.statistics.users) {
        return [];
      }

      const registrations = this.statistics.users.map(x =>
        Math.round(x.created_date / (1000 * 60 * 60 * 24))
      ); // milliseconds * seconds * minutes * hours
      const startsAt = registrations[0];
      const endsAt = registrations[registrations.length - 1];
      let count = 1;
      const result = [];

      for (let i = startsAt; i < endsAt; i++) {
        count += registrations.filter(x => x === i).length;
        result.push(count);
      }

      return result;
    },
    get_last_change_block(result) {
      const git_info = result.data;

      const now = Date.now();

      const last_commit_datetime = new Date(
        Date.parse(git_info.commit.commit.author.date)
      );
      const diff = Math.round(
        (now - last_commit_datetime.getTime()) / (24 * 3600 * 1000)
      );

      const last_commit_url = git_info.commit.html_url;

      const last_commit_datetime_string = last_commit_datetime.toLocaleDateString(
        "ru-RU",
        config.datetime_format
      );

      const ago = diff === 0 ? "(сегодня)" : `(дней назад: ${diff})`;

      this.ago = ago;
      this.last_commit_url = last_commit_url;
      this.last_commit_datetime_string = last_commit_datetime_string;
    }
  },
  mounted() {
    const githubUri =
      "https://api.github.com/repos/andrewtheproger/physicsproject/branches/master";

    axios().then(ax =>
      ax.get(githubUri).then(
        result => this.get_last_change_block(result),
        error => console.log(error)
      )
    );

    const statisticsUri = config.apiPrefix + "/statistics";
    axios().then(ax =>
      ax.get(statisticsUri).then(
        result => {
          this.statistics = result.data;
        },
        error => console.log(error)
      )
    );
  }
};
</script>

<style lang="scss" scoped>
.ph-about {
  padding: 1em;
  color: var(--foreground-primary-color);

  .ph-github-icon {
    filter: invert(100%);
    padding-right: 1em;
  }

  .ph-targets {
    list-style: none;

    li {
      margin: 0.5em 0;
    }
  }
}

.ph-statistics {
  display: flex;

  .ph-statistic-block {
    width: 30%;
  }
}

.ph-graphics {
}

.ph-graphics-title {
  padding: 0 1em;
}

.ph-graphics-title {
  border-image-slice: 1;
  border-bottom-width: 1px;
  border-bottom-style: solid;
  border-image-source: linear-gradient(
    to right,
    var(--foreground-primary-color),
    transparent
  );
}

.ph-graphic {
  border-left: 1px solid var(--foreground-primary-color);

  border-image-slice: 1;
  border-bottom-width: 1px;
  border-bottom-style: solid;
  border-top-width: 1px;
  border-top-style: solid;
  border-image-source: linear-gradient(
    to right,
    var(--foreground-primary-color),
    transparent
  );

  svg {
    height: initial;
  }
}
</style>
