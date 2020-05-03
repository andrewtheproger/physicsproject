<template>
  <div></div>
</template>
<script>
export default {
  props: ["user"],
  mounted() {
    if (this.user.status !== "authorized") {
      this.$route.router.go(`/login`);
    }
  }
};
</script>
<style lang="scss"></style>
