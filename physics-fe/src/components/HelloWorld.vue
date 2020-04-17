<template>
  <div class="hello">
    <h1>Вы авторизованы как {{ user==="user" ? "Пользователь" : "Админ"}}</h1>
    <form method="get">
      <div class="buttondiv">
        <input type="text" placeholder="Искать задачу по номеру..." />
        <br />
        <input type="submit" value="Искать" @click="getTask" />
      </div>
    </form>
    <div>
      <div>{{getShowing.text}}</div>
      <div v-for = "item in getShowing.hints" :key = "item.id" ><p v-if= "item.id - 1 !== hintsOpen">{{item.text}}</p></div>
      <div v-if = "solve"> {{getShowing.solution}}</div> 
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import { mapActions , mapGetters} from "vuex";
export default {
  name: "HelloWorld",
  props: {
    user: String
  },
  computed: mapGetters(["getShowing"]),
  data() {
    return { hintsOpen: 0, solve: false };
  },
  methods: {
    ...mapActions(["getTask"]),
  
  }
};
</script>

<style scoped lang="scss">
.buttondiv {
  margin-left: auto;
  margin-right: auto;
  text-align: center;
  input {
    width: 100%;
    height: 20px;
    &[type="submit"] {
      width: 10%;
    }
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
