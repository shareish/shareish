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
      <b-navbar-item tag="router-link" to="/conversations">
        <i class="fas fa-comments"></i>
        {{ $t('conversations') }}
        &nbsp;<span v-if="unreadMessages > 0" class="tag is-rounded">{{ unreadMessages }}</span>
      </b-navbar-item>
    </template>
    <template #end>
      <b-navbar-dropdown :label="$t(`language-${$i18n.locale}`)">
        <b-navbar-item :active="$i18n.locale === 'en'" @click="changeLanguage('en')">English</b-navbar-item>
        <b-navbar-item :active="$i18n.locale === 'fr'" @click="changeLanguage('fr')">Français</b-navbar-item>
      </b-navbar-dropdown>
      <b-navbar-dropdown v-if="isAuthenticated" :label="$t('my-account')">
        <b-navbar-item tag="router-link" to="/profile">
          <i class="fas fa-user-circle"></i>
          {{ $t('profile') }}
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
          <router-link class="button is-primary" to="/sign-up">
            <i class="fas fa-user-plus"></i>
            <strong>{{ $t('sign-up') }}</strong>
          </router-link>
          <router-link class="button is-light" to="/log-in">
            <i class="fas fa-sign-in-alt"></i>
            {{ $t('log-in') }}
          </router-link>
        </div>
      </b-navbar-item>
    </template>
  </b-navbar>
</template>

<script>
import axios from 'axios';

const NOTIFICATIONS_REFRESH_INTERVAL = 15000;

export default {
  name: 'ShareishNavbar',
  data() {
    return {
      timeout: null
    }
  },
  computed: {
    isAuthenticated() {
      return this.$store.state.isAuthenticated;
    },
    unreadMessages() {
      return this.$store.state.notifications;
    }
  },
  watch: {
    async isAuthenticated(val) {
      // Force update conversation notification when authenticated
      await this.fetchConversationUpdates();
    }
  },
  methods: {
    async fetchConversationUpdates() {
      if (this.isAuthenticated) {
        try {
          this.$store.state.notifications = (await axios.get('/api/v1/notifications/')).data['unread_messages'];
        } catch (error) {
          console.log(error);
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
    },
    async logout() {
      try {
        await axios.post('/api/v1/token/logout/');
        axios.defaults.headers.common["Authorization"] = "";
        localStorage.removeItem("token");
        this.$store.commit('removeToken');
        this.$store.commit('removeUserID');
        await this.$router.push('/');
      } catch (error) {
        if (error.response) {
          error = error.response.data;
        } else if (error.message) {
          error = error.message;
        }
        console.log(JSON.stringify(error));
      }
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
