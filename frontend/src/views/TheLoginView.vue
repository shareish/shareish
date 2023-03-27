<template>
  <div id="page-log-in" class="columns">
    <div class="column is-4 is-offset-4">
      <h1 class="title">{{ $t('log-in') }}</h1>
      <div class="field">
        <label>{{ $t('email') }}</label>
        <div class="control">
          <input v-model="email" class="input" name="email" type="email">
        </div>
      </div>
      <div class="field">
        <label>{{ $t('password') }}</label>
        <div class="control">
          <input v-model="password" class="input" name="password" type="password">
        </div>
      </div>
      <div class="field">
        <div class="control">
          <b-button class="button is-success" :loading="waitingFormResponse" @click="submitForm">{{ $t('log-in') }}</b-button>
        </div>
      </div>
      <router-link to="/reset-password">{{ $t('password-forgotten-?') }}</router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import ErrorHandler from "@/mixins/ErrorHandler";

export default {
  name: "TheLoginView",
  mixins: [ErrorHandler],
  data() {
    return {
      email: '',
      password: '',
      waitingFormResponse: false
    }
  },
  mounted() {
    document.title = `Shareish | ${this.$t('log-in')}`;
  },
  methods: {
    async submitForm() {
      this.waitingFormResponse = true;

      const formData = {
        email: this.email,
        password: this.password
      }

      try {
        const response = await axios.post("/api/v1/token/login/", formData);
        const token = response.data.auth_token;
        axios.defaults.headers.common["Authorization"] = "Token " + token;
        this.$store.commit('setToken', token);
        localStorage.setItem("token", token);

        const user = (await axios.get("api/v1/users/me/")).data;
        this.$store.commit('setUserID', user['id']);
        localStorage.setItem("user_id", user['id']);

        await this.$router.push('/');
      }
      catch (error) {
        this.snackbarError(this.$t('notif-error-user-login'));
      }

      this.waitingFormResponse = false;
    }
  }
}
</script>
