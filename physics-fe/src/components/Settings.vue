<template>
  <div>
    <md-switch @change="toggle()">Поменять тему</md-switch>
  </div>
</template>
<script>
export default {
  methods: {
    toggle() {
      this.$emit("changeTheme");
    },
  },
  data() {
    return {
      theme: Boolean,
    };
  },
  props: ["theme"],
};
</script>
<style lang="scss" scoped></style>
