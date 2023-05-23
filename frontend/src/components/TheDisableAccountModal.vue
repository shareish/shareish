<template>
  <b-loading v-if="loading" :active="true" :is-full-page="false" />
  <div v-else class="modal-card">
    <header class="modal-card-head">
      <p class="modal-card-title">{{ $tc('disable-your-account') }}</p>
      <button class="delete" type="button" @click="$emit('close')" />
    </header>
    <section class="modal-card-body">
      <p class="mb-5 has-text-centered is-size-5"><strong class="has-text-danger">{{ $t('about-to-x-your-account', {x: lcall($t('disable'))}) }}</strong></p>
      <p class="label mb-1">Here is what will happen on confirmation:</p>
      <ul class="mb-5">
        <li>Your items will not visible on Shareish anymore;</li>
        <li>Users on Shareish won't be able to message you anymore;</li>
        <li>Your profile won't be visible anymore;</li>
        <li>You won't be able to log-in until you enable your account back;</li>
        <li>You won't receive any new notification from Shareish.</li>
      </ul>
      <p class="mb-2">{{ $t('if-still-want-to-x-your-account-password', {x: lcall($t('disable'))}) }}</p>
      <b-input type="password" v-model="password" password-reveal />
    </section>
    <footer class="modal-card-foot">
      <b-button :label="$t('cancel')" @click="$emit('close')" />
      <b-button :label="$t('send-confirmation-email')" type="is-danger" :loading="waitingFormResponse" @click="sendDisableConfirmation" />
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
    async sendDisableConfirmation() {
      this.waitingFormResponse =  true;

      try {
        const data = {
          password: this.password
        }
        await axios.post(`/api/v1/users/${this.userId}/disable`, data);

        this.$emit('close');

        this.$buefy.snackbar.open({
          duration: 5000,
          type: 'is-success',
          message: this.$t('notif-success-account-disabling'),
          pauseOnHover: true
        });

        await logout(this);
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
