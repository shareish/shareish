<template>
  <div id="page-reset-password" class="page-signup">
    <div class="column is-4 is-offset-4">
      <h1 class="title">{{ $t('reset-password') }}</h1>
      <div class="field">
        <label>{{ $t('email') }}</label>
        <div class="control">
          <input v-model="email" class="input" name="email" required type="email">
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
  name: 'TheResetPasswordView',
  mixins: [ErrorHandler],
  data() {
    return {
      email: '',
      waitingFormResponse: false
    }
  },
  mounted() {
    document.title = `Shareish | ${this.$t('reset-password')}`;
  },
  methods: {
    async submitForm() {
      this.waitingFormResponse = true;

      const formData = {
        email: this.email,
      }

      try {
        await axios.post("/api/v1/users/reset_password/", formData);
        this.$buefy.snackbar.open({
          duration: 5000,
          type: 'is-success',
          message: this.$t('notif-success-password-reset-sent'),
          pauseOnHover: true
        });
        await this.$router.push('/log-in');
      }
      catch (error) {
        this.snackbarError(this.$t('notif-error-password-reset-sent'));
      }

      this.waitingFormResponse = false;
    }
  }
}
</script>
