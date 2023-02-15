<template>
  <section class="settings column">
    <div class="tile is-ancestor">
      <div class="tile is-parent">
        <div class="tile is-child box">
          <b-field key="ref_location" :message="errors.first('ref_location')" :type="{'is-danger': errors.has('ref_location')}">
            <template #label>
              <b-tooltip key="ref_location" :label="$t('help_ref_location')" multilined position="is-right">
                {{ $t('reflocation') }}
                <i class="icon far fa-question-circle"></i>
              </b-tooltip>
            </template>
            <b-input v-model="user['ref_location']" name="ref_location" type="text" />
          </b-field>
        </div>
      </div>
      <div class="tile is-parent">
        <div class="tile is-child box">
          <b-field key="dwithin_notifications" :message="errors.first('dwithin_notifications')" :type="{'is-danger': errors.has('dwithin_notifications')}">
            <template #label>
              <b-tooltip key="dwithin_notifications" :label="$t('help_dwithin')" multilined position="is-right">
                {{ $t('dwithin_notif') }}
                <i class="icon far fa-question-circle"></i>
              </b-tooltip>
            </template>
            <b-input v-model="user['dwithin_notifications']" v-validate="'numeric|max_value:1000|min_value:0'" name="dwithin_notifications" type="number" />
          </b-field>
        </div>
      </div>
    </div>
    <b-button :label="$t('save')" type="is-primary" @click="save" />
  </section>
</template>


<script>
import axios from 'axios';

export default {
  name: 'SettingsNotifications',
  $_veeValidate: {
    validator: 'new'
  },
  props: {
    user: Object
  },
  data() {
    return {
      loading: true,
      geoloc: null,
      internalUser: null
    }
  },
  async created() {
    document.title = 'Shareish | Settings: Notifications';

    this.loading = true;

    this.internalUser = this.user;

    this.fetchAddress();

    // Has the user activated geolocation?
    if ("geolocation" in navigator) {
      // Get the position
      navigator.geolocation.getCurrentPosition(pos => {
        this.geoloc = pos;
      }, err => {
        console.log(err);
      }, {
        maximumAge: 10000,
        timeout: 5000,
        enableHighAccuracy: true
      });
    }

    this.loading = false;
  },
  methods: {
    async fetchAddressGeoLoc() {
      // We need to transform this.geoloc to SRID=4326;POINT (50.695118 5.0868788)
      if (this.geoloc !== null) {
        let geoLocPoint = 'SRID=4326;POINT (' + this.geoloc.coords.latitude + ' ' + this.geoloc.coords.longitude + ')';
        console.log(this.internalUser.ref_location);
        try {
          this.internalUser.ref_location = (await axios.post(
              `/api/v1/address/`,
              geoLocPoint
          )).data;
        } catch (error) {
          console.log(JSON.stringify(error));
        }
      }
    },
    async fetchAddress() {
      if (this.internalUser !== null && this.internalUser.ref_location !== null) {
        try {
          this.internalUser.ref_location = (await axios.post(
              `/api/v1/address/`,
              this.internalUser.ref_location
          )).data;
        } catch (error) {
          console.log(JSON.stringify(error));
        }
      }
    },
    async save() {
      let result = await this.$validator.validateAll();
      if (result) {
        try {
          let user = (await axios.patch('/api/v1/users/me/', this.internalUser)).data;

          this.$buefy.snackbar.open({
            duration: 5000,
            type: 'is-success',
            message: this.$t('notif-success-user-update'),
            pauseOnHover: true,
          });

          this.$emit('updateUser', user);

          this.internalUser = user;
          this.fetchAddress();
        } catch (error) {
          console.log(error);
          this.$buefy.snackbar.open({
            duration: 5000,
            type: 'is-danger',
            message: this.$t('notif-error-user-update'),
            pauseOnHover: true,
          })
        }
      }
    }
  }
};
</script>

<style scoped>
@media screen and (max-width: 1215px) {
  .tile.is-ancestor, .tile.is-parent {
    display: block;
  }
}
</style>