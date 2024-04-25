<template>
  <b-navbar class="navbar" shadow type="is-primary">
    <template #brand>
      <b-navbar-item :to="{path: '/'}" tag="router-link">
        <strong>Shareish</strong>
      </b-navbar-item>
    </template>
    <template v-if="isAuthenticated" #start>
      <b-navbar-item tag="router-link" to="/map">
        <i class="far fa-map"></i>
        {{ $t('map') }}
      </b-navbar-item>
      <b-navbar-item tag="router-link" to="/items">
        <i class="fas fa-binoculars"></i>
        {{ $t('browse-items') }}
      </b-navbar-item>
      <b-navbar-item tag="router-link" to="/add-item">
        <i class="fas fa-plus"></i>
        {{ $t('add-item') }}
      </b-navbar-item>
      <b-navbar-item tag="router-link" :to="{name:'mapPopup', params:{popup:true}}">
        <i class="fas fa-plus"></i>
        {{ $t('add-publicresource') }}
      </b-navbar-item>
      <b-navbar-item tag="router-link" to="/conversations">
        <i class="fas fa-comments"></i>
        {{ $t('conversations') }}
        <span v-if="unreadMessagesCount > 0" class="tag is-rounded ml-2">{{ unreadMessagesCount }}</span>
      </b-navbar-item>
    </template>
    <template #end>
      <b-navbar-dropdown :label="$t(`language-${$i18n.locale}`)">
        <b-navbar-item :active="$i18n.locale === 'en'" @click="changeLanguage('en')">English</b-navbar-item>
        <b-navbar-item :active="$i18n.locale === 'fr'" @click="changeLanguage('fr')">Français</b-navbar-item>
      </b-navbar-dropdown>
      <b-navbar-dropdown v-if="isAuthenticated" :label="$t('my-account')">
        <b-navbar-item tag="router-link" to="/account">
          <i class="fas fa-user-circle"></i>
          {{ $t('account') }}
        </b-navbar-item>
        <b-navbar-item tag="router-link" to="/settings">
          <i class="fas fa-cog"></i>
          {{ $t('settings') }}
        </b-navbar-item>
        <b-navbar-item @click="logout()">
          <i class="fas fa-sign-out-alt"></i>
          {{ $t('log-out') }}
        </b-navbar-item>
      </b-navbar-dropdown>
      <b-navbar-item v-else tag="div">
        <div class="buttons">
          <router-link :to="{name: 'signup'}" class="button is-primary">
            <i class="fas fa-user-plus"></i>
            <strong>{{ $t('sign-up') }}</strong>
          </router-link>
          <router-link :to="{name: 'login'}" class="button is-light">
            <i class="fas fa-sign-in-alt"></i>
            {{ $t('log-in') }}
          </router-link>
        </div>
      </b-navbar-item>
    </template>
  </b-navbar>
</template>

<script>
import axios from "axios";
import ErrorHandler from "@/mixins/ErrorHandler";
import {logout} from "@/functions";

const NOTIFICATIONS_REFRESH_INTERVAL = 15000;

export default {
  name: 'TheNavbar',
  mixins: [ErrorHandler],
  data() {
    return {
      timeout: null,
      unableToGetNotifications: false
    }
  },
  computed: {
    isAuthenticated() {
      return this.$store.state.isAuthenticated;
    },
    unreadMessagesCount() {
      return Number(this.$store.state.notifications);
    }
  },
  watch: {
    async isAuthenticated() {
      // Force update conversation notification when authenticated
      await this.fetchConversationUpdates();
    }
  },
  methods: {
    async logout() {
      await logout(this);
    },
    async fetchConversationUpdates() {
      if (this.isAuthenticated) {
        try {
          this.$store.state.notifications = (await axios.get("/api/v1/notifications/")).data;
          if (this.unableToGetNotifications) {
            this.$buefy.snackbar.open({
              duration: 5000,
              type: 'is-success',
              message: this.$t('notifications-reloaded-successfully'),
              pauseOnHover: true,
              queue: false
            });
            this.unableToGetNotifications = false;
          }
        }
        catch (error) {
          if (!this.unableToGetNotifications) {
            this.unableToGetNotifications = true;
            this.snackbarError(error);
          }
        }
      } else {
        this.$store.state.notifications = 0;
      }
      clearTimeout(this.timeout);
      this.timeout = setTimeout(this.fetchConversationUpdates, NOTIFICATIONS_REFRESH_INTERVAL);
    },
    changeLanguage(lang) {
      localStorage.setItem('language', lang);
      this.$i18n.locale = lang;
    }
  },
  mounted() {
    this.fetchConversationUpdates();
  },
  destroyed() {
    clearTimeout(this.timeout);
  }
};
</script>

<style scoped>
.navbar .fas, .far {
  padding-right: 0.5rem;
}
</style>
