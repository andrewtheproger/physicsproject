<template>
  <div class="ph-userpage">
    <md-card>
      <md-card-header>
        <div class="md-title">Вы</div>
      </md-card-header>

      <md-card-content>
        <div class="md-layout md-gutter">
          <div class="md-layout-item md-small-size-100">
            <md-field>
              <label>Почта</label>
              <md-input
                name="form-email"
                id="form-email"
                autocomplete="given-name"
                v-model="this.$store.getters.get_user.email"
                :disabled="true"
              />
            </md-field>

            <md-checkbox
              v-if="this.$store.getters.get_user.isAdmin"
              v-model="this.$store.getters.get_user.isAdmin"
              disabled
              >Админ</md-checkbox
            >
          </div>
        </div>
      </md-card-content>

      <md-card-actions>
        <Logout></Logout>
      </md-card-actions>
    </md-card>

    <div class="ph-failure" v-if="flowFailed">
      {{
        this.flowFailed.http_code
          ? "Произошла ошибка на стороне сервера"
          : "Вы ошиблись"
      }}: {{ this.flowFailed.message }}
    </div>

    <md-progress-bar
      md-mode="indeterminate"
      v-if="this.isLoading"
    ></md-progress-bar>
  </div>
</template>

<script>
import axios from "axios";
{
  axios;
}
import Logout from "./Logout";

export default {
  name: "Userpage",
  components: {
    Logout
  },
  data() {
    return {
      isLoading: false,
      isFlowFailed: null,
      flowFailed: null
    };
  },
  methods: {}
};
</script>

<style lang="scss" scoped>
@import "../config/variables.scss";

.md-checkbox {
  display: flex;
}

.ph-userpage {
  display: flex;
  align-items: center;
  justify-content: center;
}

.md-card {
  width: 70%;
}
</style>
