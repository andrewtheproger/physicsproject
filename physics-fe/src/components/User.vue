<template>
  <div class="ph-user">
    <md-tabs v-if="!this.$store.getters.get_jwt" @md-changed="onTabChange">
      <md-tab id="tab-login" md-label="Вход"></md-tab>
      <md-tab id="tab-registration" md-label="Регистрация"></md-tab>
    </md-tabs>

    <Login v-if="!this.$store.getters.get_jwt && this.tabs.isLogin"></Login>
    <Reg v-if="!this.$store.getters.get_jwt && this.tabs.isRegistration"></Reg>

    <Userpage v-if="this.$store.getters.get_jwt"></Userpage>
  </div>
</template>

<script>
import Reg from './Reg'
import Login from './Login'
import Userpage from './Userpage'

export default {
  name: "User",
  components: {
    Reg,
    Login,
    Userpage
  },
  data() {
    return {
      tabs: {
        isRegistration: null,
      }
    }
  },
  methods: {
    onTabChange(id) {
      switch (id) {
        case 'tab-registration':
          this.tabs.isRegistration = true;
          this.tabs.isLogin = false;
          break;
        case 'tab-login':
          this.tabs.isRegistration = false;
          this.tabs.isLogin = true;
          break;
        default:
          this.tabs.isRegistration = null;
          this.tabs.isLogin = null;
      }
    }
  }
};
</script>

<style lang="scss" scoped>
@import "../config/variables.scss";

</style>
