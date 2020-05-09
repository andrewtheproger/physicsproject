<template>
  <div class="ph-main">
    <form @submit.prevent="logout">
      <md-button
        type="submit"
        class="md-raised md-primary"
        :disabled="this.isLoading"
      >
        Выйти
      </md-button>
    </form>

    <md-progress-bar
      md-mode="indeterminate"
      v-if="this.isLoading"
    ></md-progress-bar>
  </div>
</template>

<script>
import config from "../../config/api.js";
import axios from "axios";
{
  axios;
}
export default {
  name: "Logout",
  data() {
    return {
      isLoading: false,
    };
  },
  methods: {
    logout() {
      const url = config.apiPrefix + "/users/logout";
      this.isLoading = true;
      axios({
        url: url,
        method: "POST",
        headers: {
          Authorization: this.$store.getters.get_jwt,
        },
      }).then(
        () => {
          this.isLoading = false;
          this.$store.commit("set_jwt", null);
          window.location.reload();
        },
        (error) => {
          this.isLoading = false;
          const data = error.response.data;
          if (data.code === 5) {
            this.$store.commit("set_jwt", null);
            window.location.reload();
            return;
          }
          throw error;
        }
      );
    },
  },
};
</script>
<style lang="scss" scoped>
@import "../../config/variables.scss";
</style>
