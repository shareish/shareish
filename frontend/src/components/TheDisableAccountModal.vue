<template>
  <b-loading v-if="loading" :active="true" :is-full-page="false" />
  <div v-else class="modal-card">
    <header class="modal-card-head">
      <p class="modal-card-title">{{ $tc('disable-your-account') }}</p>
      <button class="delete" type="button" @click="$emit('close')" />
    </header>
    <section class="modal-card-body">
      <p class="mb-5">You are about to disable your account.</p>
      <p class="label mb-1">Here is what will happen on confirmation:</p>
      <ul class="mb-5">
        <li>Your items will be set as unlisted or private (see differences below) and therefore not visible on Shareish anymore;</li>
        <li>Users on Shareish won't be able to message you anymore;</li>
        <li>Your profile won't be visible anymore;</li>
        <li>You won't be able to log-in until you enable your account back;</li>
        <li>You won't receive any new notification from Shareish.</li>
      </ul>
      <p class="label mb-2">In addition, you can choose the visibility of your items while you are away:</p>
      <b-field class="mb-2">
          <b-radio-button v-model="visibility"
              native-value="unlisted"
              type="is-info">
              <i class="fas fa-eye-slash mr-2"></i>
              <span>Unlisted</span>
          </b-radio-button>
          <b-radio-button v-model="visibility"
              native-value="private"
              type="is-info">
              <i class="fas fa-lock mr-2"></i>
              <span>Private</span>
          </b-radio-button>
      </b-field>
      <p class="mb-5"><small>{{ visibilityExplanation }}</small></p>
      <p class="label mb-2">If you still want to disable your account, please enter your password:</p>
      <b-input type="password" v-model="password" password-reveal />
    </section>
    <footer class="modal-card-foot">
      <b-button :label="$t('cancel')" @click="$emit('close')" />
      <b-button :label="$t('confirm')" type="is-danger" :loading="waitingFormResponse" @click="disable" />
    </footer>
  </div>
</template>

<script>
import ErrorHandler from "@/mixins/ErrorHandler";
import axios from "axios";
import {logout} from "@/functions";

export default {
  name: 'TheDisableAccountModal',
  mixins: [ErrorHandler],
  data() {
    return {
      visibility: "unlisted",
      password: "",
      waitingFormResponse: false,
      loading: false
    }
  },
  computed: {
    userId() {
      return Number(this.$store.state.user.id);
    },
    visibilityExplanation() {
      return this.$t(this.visibility + '-item-explanation');
    }
  },
  methods: {
    async disable() {
      this.waitingFormResponse =  true;

      try {
        const data = {
          visibility: this.visibility,
          password: this.password
        }
        await axios.post(`/api/v1/users/${this.userId}/disable`, data);

        this.$emit('close');

        this.$buefy.snackbar.open({
          duration: 5000,
          type: 'is-success',
          message: this.$t('notif-success-account-disabling'),
          pauseOnHover: true,
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
