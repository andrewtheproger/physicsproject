<template>
  <div class="ph-about">
    <div>
      Проект посвящён книге "3800 задач по физике". Цели две:

      <ul>
        <li>Позволить быстро искать задачу по номеру,</li>
        <li>Сопроводить каждую задачу комментариями и подсказками.</li>
      </ul>
    </div>

    <h2>Текущее состояние проекта</h2>
    <div>
      <span>
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

        <span v-if="!this.last_commit_url">Загружаю...</span>

        <span v-if="this.last_commit_url">
          Последний коммит:
          <a :href="this.last_commit_url" target="_blank"
            >{{ this.last_commit_datetime_string }} {{ this.ago }}
          </a>
        </span>
      </span>

      <ul class="ph-targets">
        <li>
          <md-icon class="ph-target-done">done</md-icon>
          Создать интерфейс добавления задач,
        </li>
        <li>
          <md-icon class="ph-target-in-progress">clear</md-icon>
          Создать интерфейс добавления подсказок к задачам,
        </li>
        <li>
          <md-icon class="ph-target-in-progress">clear</md-icon>
          Перенести все задачи из 3800 к нам,
        </li>
        <li>
          <md-icon class="ph-target-in-progress">clear</md-icon>
          Сопроводить каждую задачу подсказкой или комментарием.
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

      Полезные ссылки:

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
      </ul>
    </div>

    <h4>График разработки</h4>
    <div>
      <ul>
        <li>
          До 02.04.2020

          <ul>
            <li>Добавим настройки цветовой схемы</li>
            <li>Поправим ui на мобилках</li>
          </ul>
        </li>

        <li>
          До 09.02.2020

          <ul>
            <li>Добавим статистику проекта</li>
            <li>Создадим интерфейс добавления подсказок к задачам</li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import config from "../config/api";
export default {
  name: "About",
  data() {
    return {
      ago: null,
      last_commit_url: null,
      last_commit_datetime_string: null
    };
  },
  methods: {
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
    const uri =
      "https://api.github.com/repos/andrewtheproger/physicsproject/branches/master";

    axios.get(uri).then(
      result => this.get_last_change_block(result),
      error => console.log(error)
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

    .md-icon.md-theme-default.md-icon-font.ph-target-done {
      color: var(--foreground-success-color);
    }

    .md-icon.md-theme-default.md-icon-font.ph-target-in-progress {
      color: var(--foreground-error-color);
    }
  }
}
</style>
