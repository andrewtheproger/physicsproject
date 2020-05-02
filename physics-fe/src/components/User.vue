<template>
  <div class="ph-user">
    <md-tabs v-if="this.$store.getters.get_user.is_token_expired" @md-changed="onTabChange">
      <md-tab id="tab-login" md-label="Вход"></md-tab>
      <md-tab id="tab-registration" md-label="Регистрация"></md-tab>
    </md-tabs>

    <Login v-if="this.$store.getters.get_user.is_token_expired && this.tabs.isLogin"></Login>
    <Reg v-if="this.$store.getters.get_user.is_token_expired && this.tabs.isRegistration"></Reg>

    <Userpage v-if="!this.$store.getters.get_user.is_token_expired"></Userpage>
  </div>
</template>

<script>
import Reg from './Reg'
import Login from './Login'
import Userpage from './Userpage'
import http_helper from '../lib/http'

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
  mounted() {
    http_helper.getMeAsUser(this.$store.getters.get_jwt).then(response => this.$store.commit("set_user", response.data));
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
