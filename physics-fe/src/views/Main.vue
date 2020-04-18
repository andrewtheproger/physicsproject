<template>
  <div class = "main">
    
  </div>
</template>
<script>
import { mapGetters, mapActions } from "vuex";
export default {
  name: "HelloWorld",
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
<style lang="scss">

</style>
