<template>
  <div id="page-enable-account" class="columns">
    <div class="column is-4 is-offset-4">
      <h1 class="title">{{ $t('recover-account') }}</h1>
      <template v-if="!token">
        <p class="mb-1">{{ $t('help_recover-account') }}</p>
        <ul class="mb-5">
          <li>All your items will stay unlisted or private. You will need to make them public if you want them to be seen again.</li>
          <li>Users on Shareish will be able to message you;</li>
          <li>Your profile will be visible;</li>
          <li>We will start sending you email notifications again.</li>
        </ul>
        <p class="mb-5"><strong>{{ $t('continue-recover-account') }}</strong></p>
        <div class="field">
          <label>{{ $t('email-or-username') }}</label>
          <div class="control">
            <input v-model="accountValue" class="input" name="accountValue" type="text">
          </div>
        </div>
        <div class="field">
          <div class="control">
            <b-button type="is-primary" :loading="waitingFormResponse" @click="submitForm">{{ $t('recover') }}</b-button>
          </div>
        </div>
      </template>
      <template v-else>
        <p class="mb-3" v-html="$t('help_confirm-recover', {email: accountEmailToRecover})" />
        <b-button type="is-primary" :loading="waitingFormResponse" @click="validateRecover">{{ $t('confirm-recover') }}</b-button>
      </template>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ErrorHandler from "@/mixins/ErrorHandler";
import {isNotEmptyString} from "@/functions";

export default {
  name: "TheRecoverAccountView",
  mixins: [ErrorHandler],
  data() {
    return {
      accountValue: '',
      waitingFormResponse: false,
      accountEmailToRecover: ''
    }
  },
  computed: {
    token() {
      return ('token' in this.$route.params) ? this.$route.params.token : null;
    }
  },
  created() {
    document.title = `Shareish | ${this.$t('log-in')}`;

    if (this.token)
      this.verifyToken(this.token);
  },
  methods: {
    async verifyToken(token) {
      let tokenIsValid = false;
      if (isNotEmptyString(token) && token.length === 40) {
        try {
          this.accountEmailToRecover = (await axios.post(`/api/v1/recover-account/check/${token}`)).data;
          tokenIsValid = true;
        }
        catch (error) {
          this.snackbarError(error);
        }
      }
      if (!tokenIsValid) {
        this.snackbarError("Invalid token.");
        await this.$router.push("/recover-account");
      }
    },
    async submitForm() {
      this.waitingFormResponse = true;

      const formData = {
        accountValue: this.accountValue
      };

      try {
        const email = (await axios.post("/api/v1/recover-account/", formData)).data;

        this.$buefy.snackbar.open({
          duration: 9000,
          type: 'is-success',
          message: this.$t('notif-success-email-recover-account', {email}),
          pauseOnHover: true,
        });

        await this.$router.push("/log-in");
      }
      catch (error) {
        this.snackbarError(error);
      }

      this.waitingFormResponse = false;
    },
    async validateRecover() {
      this.waitingFormResponse = true;

      try {
        const user = (await axios.post(`/api/v1/recover-account/confirm/${this.token}`)).data;

        this.$buefy.snackbar.open({
          duration: 9000,
          type: 'is-success',
          message: this.$t('notif-success-account-recovering', {email: user.email, username: user.username}),
          pauseOnHover: true,
        });

        await this.$router.push("/log-in");
      }
      catch (error) {
        this.snackbarError(error);
      }

      this.waitingFormResponse = false;
    }
  }
}
</script>

<style lang="scss" scoped>
ul {
  list-style: circle !important;

  li {
    margin-left: 30px;
  }
}
</style>
