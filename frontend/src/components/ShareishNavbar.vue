<template>
  <b-navbar type="is-primary" shadow class="navbar">
    <template #brand>
      <b-navbar-item tag="router-link" :to="{ path: '/' }">
        <strong>Shareish</strong>
      </b-navbar-item>
    </template>
    <template #start v-if="isAuthenticated">
      <b-navbar-item tag="router-link" to="/map">
        <i class="far fa-map"></i>
        {{$t('map')}}
      </b-navbar-item>

      <b-navbar-item tag="router-link" to="/items">
        <i class="fas fa-binoculars"></i>
        {{$t('browse-items')}}
      </b-navbar-item>

      <b-navbar-item tag="router-link" to="/add-item">
        <i class="fas fa-plus"></i>
        {{$t('add-item')}}
      </b-navbar-item>

      <b-navbar-item tag="router-link" to="/conversations">
        <i class="fas fa-comments"></i>
        {{$t('conversations')}}
        &nbsp;<span class="tag is-rounded" v-if="unreadMessages > 0">{{unreadMessages}}</span>
      </b-navbar-item>
    </template>

    <template #end>
      <b-navbar-dropdown :label="$t(`language-${$i18n.locale}`)">
        <b-navbar-item @click="changeLanguage('en')" :active="$i18n.locale === 'en'">
          English
        </b-navbar-item>
        <b-navbar-item @click="changeLanguage('fr')" :active="$i18n.locale === 'fr'">
          Français
        </b-navbar-item>
      </b-navbar-dropdown>
      <b-navbar-item tag="router-link" v-if="isAuthenticated" to="/profile">
        <i class="fas fa-user-circle"></i>
        {{$t('my-account')}}
      </b-navbar-item>
      <b-navbar-item tag="div" v-else>
        <div class="buttons">
          <router-link to="/sign-up" class="button is-primary">
            <i class="fas fa-user-plus"></i>
            <strong>{{ $t('sign-up') }}</strong>
          </router-link>
          <router-link to="/log-in" class="button is-light">
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
  methods: {
    async fetchConversationUpdates() {
      if (this.isAuthenticated) {
        try {
          this.$store.state.notifications = (await axios.get('/api/v1/notifications/')).data['unread_messages'];
        }
        catch (error) {
          console.log(error);
        }
      }
      clearTimeout(this.timeout);
      this.timeout = setTimeout(this.fetchConversationUpdates, NOTIFICATIONS_REFRESH_INTERVAL);
    },
    changeLanguage(lang){
      localStorage.setItem('language', lang);
      this.$i18n.locale = lang;
    },
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