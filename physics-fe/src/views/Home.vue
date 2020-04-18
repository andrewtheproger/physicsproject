<template>
  <div>
    <HelloWorld v-bind:user="user" />
  </div>
</template>

<script>
import HelloWorld from "@/components/HelloWorld.vue";

export default {
  name: "Home",
  data() {
    return {
      user: "admin",
      
    };
  },
  components: {
    HelloWorld,
  },
};
</script>
