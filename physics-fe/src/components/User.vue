<template>
  <div class="ph-user">
    <md-tabs v-if="this.user.is_token_expired" @md-changed="onTabChange">
      <md-tab id="tab-login" md-label="Вход"></md-tab>
      <md-tab id="tab-registration" md-label="Регистрация"></md-tab>
    </md-tabs>

    <Login v-if="this.user.is_token_expired && this.tabs.isLogin"></Login>
    <Registration
      v-if="this.user.is_token_expired && this.tabs.isRegistration"
    ></Registration>

    <Userpage v-if="this.user.is_token_expired === false"></Userpage>
  </div>
</template>

<script>
const Registration = () =>
  import(
    /* webpackChunkName: "components_User_Registration" */ "./User/Registration"
  );
const Login = () =>
  import(/* webpackChunkName: "components_User_Login" */ "./User/Login");
const Userpage = () =>
  import(/* webpackChunkName: "components_User_Userpage" */ "./User/Userpage");

export default {
  name: "User",
  components: {
    Registration,
    Login,
    Userpage
  },
  data() {
    return {
      tabs: {
        isRegistration: null
      }
    };
  },
  computed: {
    user() {
      return this.$store.getters.get_user;
    }
  },
  methods: {
    onTabChange(id) {
      switch (id) {
        case "tab-registration":
          this.tabs.isRegistration = true;
          this.tabs.isLogin = false;
          break;
        case "tab-login":
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

<style lang="scss" scoped></style>
