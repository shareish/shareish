<template>
  <div id="page-reset-password-confirm" class="columns">
    <div class="column is-4 is-offset-4">
      <h1 class="title">{{ $t('reset-password') }}</h1>
      <div class="field">
        <label>{{ $t('password') }}</label>
        <div class="control">
          <input v-model="password" :placeholder="$t('enter-new-password')" class="input" name="password" type="password">
        </div>
      </div>
      <div class="field">
        <div class="control">
          <b-button type="is-primary" :loading="waitingFormResponse" @click="submitForm">{{ $t('reset-password') }}</b-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import ErrorHandler from "@/mixins/ErrorHandler";

export default {
  name: 'TheResetPasswordConfirmView',
  mixins: [ErrorHandler],
  data() {
    return {
      uid: '',
      token: '',
      password: '',
      waitingFormResponse: false
    }
  },
  mounted() {
    document.title = `Shareish | ${this.$t('reset-password')}`;
    this.uid = this.$route.params.uid;
    this.token = this.$route.params.token;
  },
  methods: {
    async submitForm() {
      this.waitingFormResponse = true;

      const formData = {
        uid: this.uid,
        token: this.token,
        new_password: this.password
      };

      try {
        await axios.post("/api/v1/users/reset_password_confirm/", formData);
        this.$buefy.snackbar.open({
          duration: 5000,
          type: 'is-success',
          message: this.$t('notif-success-password-reset'),
          pauseOnHover: true
        });
        await this.$router.push('/login');
      }
      catch (error) {
        this.snackbarError(this.$t('notif-error-reset-password'));
      }

      this.waitingFormResponse = false;
    }
  }
}
</script>
