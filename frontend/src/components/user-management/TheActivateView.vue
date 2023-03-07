<template>
  <div id="page-activate" class="columns">
    <div class="column is-4 is-offset-4">
      <h1 class="title">{{ $t('activate-your-account') }}</h1>
      <div class="field">
        <label>{{ $t('email') }}</label>
        <div class="control">
          <input v-model="email" class="input" name="email" required type="email">
        </div>
      </div>
      <div class="field">
        <div class="control">
          <b-button class="button is-success" :loading="waitingFormResponse" @click="resendActivation">{{ $t('resend-activation') }}</b-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"
import ErrorHandler from "@/components/ErrorHandler";

export default {
  name: 'TheActivateView',
  mixins: [ErrorHandler],
  data() {
    return {
      email: "",
      errors: [],
      waitingFormResponse: false
    }
  },
  mounted() {
    document.title = `Shareish | ${this.$t('activate-your-account')}`;
    const uid = this.$route.params.uid;
    const token = this.$route.params.token;
    if (uid && token)
      this.submitActivation(uid, token);
  },
  methods: {
    async submitActivation(uid, token) {
      this.errors = [];

      const formData = {
        uid: uid,
        token: token
      };

      try {
        await axios.post("/api/v1/users/activation/", formData);
        this.$buefy.snackbar.open({
          duration: 5000,
          type: 'is-success',
          message: this.$t('notif-success-email-activation'),
          pauseOnHover: true
        });
        await this.$router.push("/");
      }
      catch (error) {
        let errorMessage;
        if (error.response) {
          for (const property in error.response.data) {
            if (Array.isArray(error.response.data[property])) {
              for (const idx in error.response.data[property]) {
                const message = error.response.data[property][idx];
                this.errors.push(`${property}: ${message}`);
              }
            } else {
              this.errors.push(`${property}: ${error.response.data[property]}`);
            }
          }
          console.log(JSON.stringify(error.response.data));
          errorMessage = this.errors.join("<br />");
        } else if (error.message) {
          console.log(JSON.stringify(error.message));
          errorMessage = error.message;
        } else {
          console.log(JSON.stringify(error));
          errorMessage = this.$t('notif-error-email-activation');
        }

        this.snackbarError(errorMessage);
      }
    },
    async resendActivation() {
      this.waitingFormResponse = true;

      const formData = {
        email: this.email
      };

      try {
        await axios.post("/api/v1/users/resend_activation/", formData);
        this.$buefy.snackbar.open({
          duration: 5000,
          type: 'is-success',
          message: this.$t('notif-success-resend-activation'),
          pauseOnHover: true
        });
      }
      catch (error) {
        this.snackbarError(this.$t('notif-error-resend-activation'));
      }

      this.waitingFormResponse = false;
    }
  }
};
</script>