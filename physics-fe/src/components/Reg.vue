<template>
  <div class="ph-main">
    <md-card>
      <md-card-header>
        <div class="md-title">Регистрация</div>
      </md-card-header>

      <md-card-content>
        <div class="ph-reg">
          <form v-on:submit.prevent="submit">
            <md-field :class="getValidationClass('email')">
              <label>Почта для восстановления доступа</label>

              <md-input type="email" v-model.trim="form.email" name="form-email" id="form-email"/>
              <span class="md-error" v-if="!$v.form.email.required">Почта необходима для восстановления доступа к аккаунту в случае утраты пароля</span>
              <span class="md-error" v-if="!$v.form.email.email">Не похоже на почту</span>
            </md-field>

            <md-field :class="getValidationClass('password')">
              <label>Пароль</label>

              <md-input type="password" v-model.trim="form.password" name="form-password" id="form-password"/>
              <span class="md-error" v-if="!$v.form.password.required">Пароль не должен быть пустым</span>
              <span class="md-error" v-if="!$v.form.password.minLength">Длина пароля - минимум {{$v.form.password.$params.minLength.min}} символов</span>
            </md-field>

            <md-field :class="getValidationClass('repeatPassword')">
              <label>Пароль</label>

              <md-input type="password" v-model.trim="form.repeatPassword" name="form-repeatPassword" id="form-repeatPassword"/>
              <span class="md-error" v-if="!$v.form.repeatPassword.sameAsPassword">Пароль не должен быть пустым</span>
            </md-field>

            <div class="ph-registration-submit-controls">
              <md-button
                      type="submit"
                      class="md-raised md-primary"
                      :disabled="this.isLoading">
                Далее
              </md-button>
            </div>
          </form>

          <md-progress-bar md-mode="indeterminate" v-if="this.isLoading"></md-progress-bar>

          <div class="ph-failure" v-if="flowFailed">
            {{ this.flowFailed.http_code ? 'Произошла ошибка на стороне сервера' : 'Вы ошиблись' }}: {{ this.flowFailed.message }}
          </div>
        </div>
      </md-card-content>
    </md-card>
  </div>
</template>

<script>
import { required, email, minLength, sameAs } from 'vuelidate/lib/validators'
import { validationMixin } from 'vuelidate'
import config from "../config/api.js";
import axios from "axios";
{
  axios;
}
export default {
  name: "Reg",
  mixins: [validationMixin],
  data() {
    return {
      form: {
        email: 'test@yandex.ru',
        password: '123456789123456789',
        repeatPassword: '123456789123456789'
      },
      isLoading: false,
      isFlowFailed: null,
      flowFailed: null
    };
  },
  validations: {
    form: {
      email: {
        required,
        email
      },
      password: {
        required,
        minLength: minLength(16)
      },
      repeatPassword: {
        sameAsPassword: sameAs('password')
      }
    }
  },

  methods: {
    getValidationClass (fieldName) {
      const field = this.$v.form[fieldName];

      if (field) {
        return {
          'md-invalid': field.$invalid && field.$dirty
        }
      }
    },
    submit() {
      this.isLoading = true;
      this.$v.$touch();

      if (this.$v.$invalid) {
        this.isLoading = false;
        return;
      }

      axios.post(`${config.apiPrefix}/users/register`, {
        email: this.form.email,
        password: this.form.password
      })
      .then((response) => {
        this.isLoading = false;
        this.isFlowFailed = false;

        this.$store.commit('set_jwt', response.data.jwt);

        return response;
      })
      .catch((error) => {
        this.isFlowFailed = true;

        const data = error.response.data;

        this.flowFailed = {
          http_code: error.response.code,
          internal_code: data.code,
          message: this.get_error_message(data.code),
        };

        this.isLoading = false;
      });
    }
  }
};
</script>
<style lang="scss" scoped>
@import "../config/variables.scss";

.ph-registration-submit-controls {
  display: flex;
  flex-direction: row-reverse;
}

.ph-failure {
  color: red;
}

div.md-field.md-theme-default
{
  &.md-invalid .md-error {
    -webkit-text-fill-color: red;
    color: red;
  }
}

.ph-main {
  display: flex;
  align-content: center;
  justify-content: center;
}

.md-card {
  width: 70%;
  margin: 4px;
}

.md-icon.md-theme-default.md-icon-font {
  filter: invert(1);
}

</style>
