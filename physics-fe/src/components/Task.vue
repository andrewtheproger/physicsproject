<template>
  <div class="ph-task" v-on:keyup.escape="cl">
    <h3 class="ph-task-header">
      <span>3800.{{ task.base_number }}.{{ task.task_number }}</span>
      <md-button
        :to="`/edit/${task.id}`"
        class="md-icon-button md-dense md-primary"
        v-if="this.user.isAdmin"
      >
        <md-icon>edit</md-icon>
      </md-button>
    </h3>
    <div classs="ph-text">
      <vue-mathjax :formula="task.body.latex"></vue-mathjax>
    </div>
    <ul class="ph-task-images">
      <li v-for="image in task.body.images" :key="image.id">
        <img alt="task image" :src="image.url" />
      </li>
    </ul>

    <div v-if="task.hints.length">
      <h4>Идея решения</h4>

      <ul class="ph-task-hints">
        <li v-for="hint in task.hints" :key="hint.id">
          <div
            class="ph-latex"
            v-for="formula in hint.body.latex.split('\n')"
            :key="formula"
          >
            <vue-mathjax :formula="formula"></vue-mathjax>
          </div>

          <ul class="ph-task-hints-images">
            <li>
              <md-content v-for="id in hint.body.image_ids" :key="id">
                <img :src="id" alt="Task image" />
              </md-content>
            </li>
          </ul>
        </li>
      </ul>
    </div>
    <div class="ph-task-no-hints-available" v-else>
      Подсказок к решению пока нет.
    </div>

    <div v-if="task.body.answer">
      <h4>Ответ</h4>

      <vue-mathjax :formula="task.body.answer"></vue-mathjax>
    </div>
    <div class="ph-task-no-hints-available" v-else>
      Ответа на задачу не найдено
    </div>
  </div>
</template>

<script>
import VueMathjax from "./VueMathJax/vueMathJax";

export default {
  name: "Task",
  components: {
    VueMathjax
  },
  props: ["task"],
  computed: {
    user() {
      return this.$store.getters.get_user;
    }
  }
};
</script>

<style scoped lang="scss">
.ph-task-no-hints-available {
  font-size: 80%;
}

.ph-task-header {
  display: flex;
  align-items: center;
}

.ph-task-hints,
.ph-task {
  padding-left: 0;
  list-style: none;

  h3 {
    margin-top: 3em;
    text-decoration: double;
  }

  .ph-latex {
    margin-left: 2em;
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
      max-height: 200px;
      filter: invert(7%);

      &:hover {
        cursor: pointer;
        filter: invert(0%);
      }
    }
  }
}
</style>
