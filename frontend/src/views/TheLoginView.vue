<template>
  <div id="page-log-in" class="columns">
    <div class="column is-4 is-offset-4">
      <h1 class="title">{{ $t('log-in') }}</h1>
      <div class="field">
        <label>{{ $t('email-or-username') }}</label>
        <div class="control">
          <input v-model="authValue" class="input" name="authValue" type="text">
        </div>
      </div>
      <b-message v-if="showDisabledAccountLink" title="Account disabled" type="is-warning">
        {{ $t('help_login-disabled-account') }} <router-link :to="{name: 'recoverAccount'}">{{ $t('click-here') }}</router-link>.
      </b-message>
      <b-message v-if="showScheduledDeletionAccountLink" title="Account scheduled for deletion" type="is-danger">
        <span v-html="$t('help_login-scheduled-deletion-account', {x: daysBeforeDeletion})" /> <router-link :to="{name: 'recoverAccount'}">{{ $t('click-here') }}</router-link>.
      </b-message>
      <div class="field">
        <label>{{ $t('password') }}</label>
        <div class="control">
          <input v-model="password" class="input" name="password" type="password">
        </div>
      </div>
      <div class="field">
        <div class="control">
          <b-button type="is-primary" :loading="waitingFormResponse" @click="submitForm">{{ $t('log-in') }}</b-button>
        </div>
      </div>
      <router-link :to="{name: 'resetPassword'}">{{ $t('password-forgotten-?') }}</router-link>
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
      authValue: '',
      password: '',
      waitingFormResponse: false,
      showDisabledAccountLink: false,
      showScheduledDeletionAccountLink: false,
      daysBeforeDeletion: 0
    }
  },
  created() {
    document.title = `Shareish | ${this.$t('log-in')}`;
  },
  methods: {
    async submitForm() {
      this.waitingFormResponse = true;

      const formData = {
        authValue: this.authValue,
        password: this.password
      }

      try {
        const auth = (await axios.post("/api/v1/auth/login/", formData)).data;

        axios.defaults.headers.common["Authorization"] = "Token " + auth['token'];
        this.$store.commit('setToken', auth['token']);
        localStorage.setItem("token", auth['token']);

        this.$store.commit('setUserID', auth['id']);
        localStorage.setItem("user_id", auth['id']);

        await this.$router.push('/map');
      }
      catch (error) {
        if (this.isKeyedError(error)) {
          const key = this.getErrorKey(error);
          console.log(key);
          if (key === 'DISABLED_ACCOUNT') {
            this.showDisabledAccountLink = true;
          } else if (key === 'SCHEDULED_DELETION_ACCOUNT') {
            this.showScheduledDeletionAccountLink = true;
            this.daysBeforeDeletion = Number(error.response.data.days_left);
          }
        }
        this.snackbarError(error, {'showErrorCode': false});
      }

      this.waitingFormResponse = false;
    }
  }
}
</script>
