<template>
  <div id="page-settings" class="max-width-is-max-container">
    <h1 class="title mb-6">{{ $t('settings') }} & {{ $t('notifications') }}</h1>
    <b-loading v-if="loading" :active="true" :is-full-page="false" />
    <div v-else class="columns is-variable" id="settings-split">
      <aside class="menu column">
        <p class="menu-label">{{ $t('general') }}</p>
        <ul class="menu-list">
          <li>
            <router-link to="/settings/profile" :class="{'is-active': currentView === 'profile'}">
              <i class="fas fa-user-circle"></i>
              {{ $t('profile') }}
            </router-link>
          </li>
          <li>
            <router-link to="/settings/account" :class="{'is-active': currentView === 'account'}">
              <i class="fas fa-cog"></i>
              {{ $t('account') }}
            </router-link>
          </li>
        </ul>
        <p class="menu-label">{{ $t('email') }} {{ $t('notifications').toLowerCase() }}</p>
        <ul class="menu-list">
          <li>
            <router-link to="/settings/notifications" :class="{'is-active': currentView === 'notifications'}">
              <i class="fas fa-bell"></i>
              {{ $t('email') }} {{ $t('notifications').toLowerCase() }}
            </router-link>
          </li>
        </ul>
      </aside>
      <the-settings-profile v-if="currentView==='profile'" :user="user" @updateUser="updateUser" />
      <the-settings-account v-else-if="currentView==='account'" :user="user" @updateUser="updateUser" />
      <the-settings-notifications v-else-if="currentView==='notifications'" :user="user" @updateUser="updateUser" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import TheSettingsProfile from "@/components/TheSettingsProfile.vue";
import TheSettingsNotifications from "@/components/TheSettingsNotifications.vue";
import TheSettingsAccount from "@/components/TheSettingsAccount.vue";
import ErrorHandler from "@/components/ErrorHandler";

export default {
  name: 'TheSettingsView',
  mixins: [ErrorHandler],
  components: {TheSettingsAccount, TheSettingsNotifications, TheSettingsProfile},
  $_veeValidate: {
    validator: 'new'
  },
  data() {
    return {
      loading: true,
      user: null,
      geoLocation: null,
      currentView: null,
      possibleViews: ['profile', 'account', 'notifications']
    }
  },
  async created() {
    this.loading = true;

    document.title = 'Shareish | Settings';

    if (this.possibleViews.includes(this.$route.params.tab)) {
      this.currentView = this.$route.params.tab;
    } else {
      this.$router.push("/settings/profile")
    }

    await this.fetchUser();

    // Has the user activated geolocation?
    if ('geolocation' in navigator) {
      // Get the position
      navigator.geolocation.getCurrentPosition(
        position => {
          this.geoLocation = position;
        },
        null,
        {
          maximumAge: 10000,
          timeout: 5000,
          enableHighAccuracy: true
        }
      );
    }

    this.loading = false;
  },
  methods: {
    async fetchUser() {
      try {
        this.user = (await axios.get("/api/v1/users/me/")).data;
      }
      catch (error) {
        this.snackbarError(error);
      }
    },
    updateUser(user) {
      this.user = user;
    }
  },
  watch: {
    $route() {
      this.currentView = this.$route.params.tab;
    }
  }
};
</script>

<style scoped>
.max-width-is-max-container {
  margin: 0 auto;
  max-width: 1344px;
}

#settings-split aside.menu {
  max-width: 250px;
}

.menu-list i {
  margin-right: 3px;
}

@media screen and (max-width: 1023px) and (min-width: 768px) {
  #settings-split aside.menu {
    max-width: calc(18% + 100px);
  }
}

@media screen and (max-width: 768px) {
  #settings-split {
    display: block;
  }

  #settings-split aside.menu {
    max-width: 100%;
  }
}
</style>