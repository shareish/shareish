<template>
  <b-loading v-if="loading" :active="true" :is-full-page="false" />
  <div v-else class="modal-card">
    <header class="modal-card-head">
      <p class="modal-card-title">{{ $tc('delete-your-account') }}</p>
      <button class="delete" type="button" @click="$emit('close')" />
    </header>
    <section class="modal-card-body">
      <p class="mb-5 has-text-centered is-size-5"><strong class="has-text-danger">{{ $t('about-to-x-your-account', {x: lcall($t('delete'))}) }}</strong></p>
      <p class="label mb-1">Here is what will happen on confirmation:</p>
      <ul class="mb-5">
        <li>Your items will be completely deleted from Shareish;</li>
        <li>Users on Shareish won't be able to message you anymore;</li>
        <li>Your profile will be deleted;</li>
        <li>This account will never be accessible anymore once deleted;</li>
        <li>You won't receive any new notification from Shareish.</li>
      </ul>
      <p class="mb-5">
        <strong>{{ $t('as-security-email-confirmation-delete') }}</strong>
        {{ $t('if-delete-choice-confirmed-no-recover') }}
      </p>
      <p class="mb-5 has-text-centered is-size-5"><strong class="has-text-danger">{{ $t('danger-warning-delete-account') }}</strong></p>
      <p class="mb-2">{{ $t('if-still-want-to-x-your-account-password', {x: lcall($t('delete'))}) }}</p>
      <b-input type="password" v-model="password" password-reveal />
    </section>
    <footer class="modal-card-foot">
      <b-button :label="$t('cancel')" @click="$emit('close')" />
      <b-button :label="$t('send-confirmation-email')" type="is-danger" :loading="waitingFormResponse" @click="sendDeleteConfirmation" />
    </footer>
  </div>
</template>

<script>
import ErrorHandler from "@/mixins/ErrorHandler";
import axios from "axios";
import {lcall, logout} from "@/functions";

export default {
  name: 'TheDisableAccountModal',
  mixins: [ErrorHandler],
  data() {
    return {
      password: "",
      waitingFormResponse: false,
      loading: false
    }
  },
  computed: {
    userId() {
      return Number(this.$store.state.user.id);
    }
  },
  methods: {
    lcall,
    async sendDeleteConfirmation() {
      this.waitingFormResponse =  true;

      try {
        const data = {
          password: this.password
        }
        await axios.post(`/api/v1/users/${this.userId}/send-delete-confirmation`, data);

        this.$emit('close');

        this.$buefy.snackbar.open({
          duration: 5000,
          type: 'is-success',
          message: this.$t('notif-success-account-deletion-process-link-sent'),
          pauseOnHover: true,
        });
      }
      catch (error) {
        this.snackbarError(error);
      }

      this.waitingFormResponse =  false;
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
