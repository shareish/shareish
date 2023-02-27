<template>
  <div class="page-account container">
    <h1 class="title mb-6">{{ $t('settings') }} & {{ $t('notifications') }}</h1>
    <b-loading v-if="loading" :active="loading" :is-full-page="false" />
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
<!--          <li>-->
<!--            <router-link to="/settings/privacy" :class="{'is-active': currentView === 'privacy'}">-->
<!--              <i class="fas fa-lock"></i>-->
<!--              {{ $t('privacy') }}-->
<!--            </router-link>-->
<!--          </li>-->
<!--          <li>-->
<!--            <router-link to="/settings/account" :class="{'is-active': currentView === 'account'}">-->
<!--              <i class="fas fa-cog"></i>-->
<!--              {{ $t('account') }}-->
<!--            </router-link>-->
<!--          </li>-->
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
      <settings-profile v-if="currentView==='profile'" :user="user" @updateUser="updateUser" />
      <settings-notifications v-else-if="currentView==='notifications'" :user="user" @updateUser="updateUser" />
      <div v-else class="test">Test</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import SettingsProfile from "@/components/settings/SettingsProfile.vue";
import SettingsNotifications from "@/components/settings/SettingsNotifications.vue";

export default {
  name: 'Settings',
  components: {SettingsNotifications, SettingsProfile},
  $_veeValidate: {
    validator: 'new'
  },
  data() {
    return {
      loading: true,
      user: null,
      geoloc: null,
      currentView: null,
      possibleViews: ['profile', 'privacy', 'account', 'notifications']
    }
  },
  async created() {
    this.loading = true;

    document.title = 'Shareish | Settings';

    if (this.possibleViews.includes(this.$route.params.page)) {
      this.currentView = this.$route.params.page;
    } else {
      this.$router.push("/settings/profile")
    }

    await this.fetchUser();

    // Has the user activated geolocation?
    if ("geolocation" in navigator) {
      // Get the position
      navigator.geolocation.getCurrentPosition(pos => {
        this.geoloc = pos;
      }, error => {
        console.log(error);
      }, {
        maximumAge: 10000,
        timeout: 5000,
        enableHighAccuracy: true
      });
    }

    this.loading = false;
  },
  methods: {
    async fetchUser() {
      try {
        const uri = `/api/v1/users/me/`
        this.user = (await axios.get(uri)).data;
      } catch (error) {
        console.log(error);
      }
    },
    async fetchAddressGeoLoc() {
      if (this.geoloc !== null) {
        let geoLocPoint = 'SRID=4326;POINT (' + this.geoloc.coords.latitude + ' ' + this.geoloc.coords.longitude + ')';
        try {
          this.user.ref_location = (await axios.post(`/api/v1/address/`, geoLocPoint)).data;
        } catch (error) {
          console.log(JSON.stringify(error));
        }
      }
    },
    async fetchAddress() {
      if (this.user !== null && this.user.ref_location !== null) {
        try {
          this.user.ref_location = (await axios.post(`/api/v1/address/`, this.user.ref_location)).data;
        } catch (error) {
          console.log(JSON.stringify(error));
        }
      }
    },
    updateUser(user) {
      this.user = user;
    }
  },
  watch: {
    $route() {
      this.currentView = this.$route.params.page;
    }
  }
};
</script>

<style scoped>
#settings-split aside.menu {
  max-width: 250px;
}

@media screen and (max-width: 1023px) and (min-width: 767px) {
  #settings-split aside.menu {
    max-width: calc(18% + 100px);
  }
}

@media screen and (max-width: 767px) {
  #settings-split {
    display: block;
  }

  #settings-split aside.menu {
    max-width: 100%;
  }
}

.menu-list i {
  margin-right: 3px;
}
</style>
