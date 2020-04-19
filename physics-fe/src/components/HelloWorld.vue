<template>
  <div class="hello">

    <form class="search-form" v-on:submit.prevent="getTask">
        <md-field>
          <label>2.15...</label>
          <md-input v-model="num"></md-input>
        </md-field>
        
        <md-button class="md-icon-button md-primary">
          <md-icon>search</md-icon>
        </md-button>
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
