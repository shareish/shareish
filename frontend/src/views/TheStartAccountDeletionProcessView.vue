<template>
  <div v-if="token" id="page-enable-account" class="columns">
    <div class="column is-4 is-offset-4">
      <h1 class="title">{{ $t('start-account-deletion-process') }}</h1>

      <p class="mb-3" v-html="$t('help_start-account-deletion-process', {email: token.user.email, username: token.user.username})" />
      <b-button type="is-danger" :loading="waitingFormResponse" @click="confirmDeletion">{{ $t('confirm-deletion') }}</b-button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ErrorHandler from "@/mixins/ErrorHandler";
import {isNotEmptyString, logout} from "@/functions";

export default {
  name: "TheStartAccountDeletionProcessView",
  mixins: [ErrorHandler],
  data() {
    return {
      accountValue: '',
      waitingFormResponse: false,
      token: null
    }
  },
  computed: {
    urlToken() {
      return this.$route.params.token;
    }
  },
  async created() {
    document.title = `Shareish | ${this.$t('start-account-deletion-process')}`;

    if (this.urlToken)
      await this.verifyToken(this.urlToken);
  },
  methods: {
    async verifyToken(token) {
      let tokenIsValid = false;
      if (isNotEmptyString(token)) {
        try {
          this.token = (await axios.get(`/api/v1/tokens/${token}/check?action=delete_account`)).data;
          tokenIsValid = true;
        }
        catch (error) {
          this.snackbarError(error, {showErrorCode: false});
        }
      }
      if (!tokenIsValid)
        await this.$router.push("/");
    },
    async confirmDeletion() {
      this.waitingFormResponse = true;

      try {
        await axios.get(`/api/v1/delete-account/confirm/${this.token.token}`);

        this.$buefy.snackbar.open({
          duration: 9000,
          type: 'is-success',
          message: this.$t('notif-success-start-account-deletion-process', {email: this.token.user.email, username: this.token.user.username}),
          pauseOnHover: true
        });

        await logout(this);
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
