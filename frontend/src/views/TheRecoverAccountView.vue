<template>
  <div id="page-enable-account" class="columns">
    <div class="column is-4 is-offset-4">
      <h1 class="title">{{ $t('recover-account') }}</h1>
      <template v-if="!urlToken">
        <p class="mb-1">{{ $t('help_recover-account') }}</p>
        <ul class="mb-5">
          <li>Your items will be visible again on Shareish.</li>
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
      <template v-else-if="token">
        <p class="mb-3" v-html="$t('help_confirm-recover', {email: token.user.email, username: token.user.username})" />
        <b-button type="is-primary" :loading="waitingFormResponse" @click="confirmRecover">{{ $t('confirm-recover') }}</b-button>
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
      token: ''
    }
  },
  computed: {
    urlToken() {
      return ('token' in this.$route.params) ? this.$route.params.token : null;
    }
  },
  created() {
    document.title = `Shareish | ${this.$t('account-recovering')}`;

    if (this.urlToken)
      this.verifyToken(this.urlToken);
  },
  methods: {
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
          pauseOnHover: true
        });

        await this.$router.push("/log-in");
      }
      catch (error) {
        this.snackbarError(error);
      }

      this.waitingFormResponse = false;
    },
    async verifyToken(token) {
      let tokenIsValid = false;
      if (isNotEmptyString(token)) {
        try {
          this.token = (await axios.get(`/api/v1/tokens/${token}/check?action=recover_account`)).data;
          tokenIsValid = true;
        }
        catch (error) {
          this.snackbarError(error, {showErrorCode: false});
        }
      }
      if (!tokenIsValid)
        await this.$router.push("/recover-account");
    },
    async confirmRecover() {
      this.waitingFormResponse = true;

      try {
        await axios.get(`/api/v1/recover-account/confirm/${this.token.token}`);

        this.$buefy.snackbar.open({
          duration: 9000,
          type: 'is-success',
          message: this.$t('notif-success-account-recovering', {email: this.token.user.email, username: this.token.user.username}),
          pauseOnHover: true
        });

        await this.$router.push("/log-in");
      }
      catch (error) {
        this.snackbarError(error, {showErrorCode: false});
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
