<template>
  <div class="hello">
    <h1 style="color: white;">
      Вы авторизованы как {{ user === "user" ? "Пользователь" : "Админ" }}
    </h1>
    <form v-on:submit.prevent="getTask">
      <div class="buttondiv">
        <input
          type="text"
          placeholder="Искать задачу по номеру..."
          v-model="num"
        />
        <br />
        <input type="submit" />
      </div>
    </form>
    <div class="container" v-if="getShowing !== undefined">
      <div v-for="item in getShowing.body.image_hrefs" :key="item">
        <img v-bind:src="item" class="graph" />
      </div>
      <p v-if="solution">{{ getShowing.body.latex }}</p>
    </div>
    <div v-if="getShowing !== undefined">
      <div v-for="item in getShowing.hints" :key="item.id">
        <p v-if="item.id <= hints && item.status !== `pending`">
          {{ item.latex }}
        </p>
        <div v-for="n in item.image_hrefs" :key="n">
          <img v-bind:src="n" class="graph" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import { mapGetters, mapActions } from "vuex";
export default {
  name: "HelloWorld",
  props: {
    user: String,
  },
  computed: mapGetters(["getShowing"]),

  data() {
    return {
      url: "http://127.0.0.1:5000/api/",
      num: "",
      hints: 0,
      solution: false,
    };
  },
  methods: {
    ...mapActions(["getTaskByNum"]),
    getTask() {
      this.getTaskByNum(this.num);
      console.log(this.getShowing);
    },
  },
};
</script>

<style scoped lang="scss">
.graph {
  width: 100%;
  height: 100%;
}
.buttondiv {
  margin-left: auto;
  margin-right: auto;
  text-align: center;
  input {
    &[type = text] {
      width: 100%;
    }
    
    color: white;
    border: 1px solid lightgray;
    background-color: #252525;
  }
}
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;

  li {
    display: inline-block;
    margin: 0 10px;
  }
}
a {
  color: #7e9ef5;
}
</style>
