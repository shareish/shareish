<template>
  <section class="settings column">
    <div class="tile is-ancestor">
      <div class="tile is-parent">
        <div class="tile is-child box">
          <div class="field is-horizontal">
            <div class="field-body">
              <b-field key="ref_location" :message="errors.first('ref_location')" :type="{'is-danger': errors.has('ref_location')}">
                <template #label>
                  <b-tooltip key="ref_location" :label="$t('help_ref_location')" multilined position="is-right">
                    {{ $t('reflocation') }}
                    <i class="icon far fa-question-circle"></i>
                  </b-tooltip>
                </template>
                <b-button @click="fetchAddressGeoLoc" type="is-primary">
                  <i class="icon fas fa-map-marker-alt"></i>
                </b-button>
                <b-input v-model="internalUser['ref_location']" name="ref_location" type="text" class="is-expanded ml-2" />
              </b-field>
            </div>
          </div>
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
            <b-slider v-model="internalUser['dwithin_notifications']" indicator :tooltip="false" :max="99" format="raw" class="mt-5 pl-3 pr-3" />
          </b-field>
        </div>
      </div>
    </div>
    <div class="box">
      <b-field key="notif_conversations" horizontal>
        <template #label>
          <b-tooltip :label="$t('help_notif_conversations')" multilined position="is-right" class="frequency_label">
            {{ $t('conversations') }}
            <i class="icon far fa-question-circle"></i>
          </b-tooltip>
        </template>
        <template v-if="windowWidth >= 1024">
          <template v-for="{key, translationKey, color} in conversationsFrequencies">
            <b-radio-button :key="key" v-model="radioGroups['notif_conversations']" :native-value="key" :type="color">
              <span>{{ $t(translationKey) }}</span>
            </b-radio-button>
          </template>
        </template>
        <template v-else>
          <b-select v-model="radioGroups['notif_conversations']" placeholder="Select a frequency" expanded>
            <option v-for="{key, translationKey} in frequencies" :value="key" :key="key">{{ $t(translationKey) }}</option>
          </b-select>
        </template>
      </b-field>
    </div>
    <div class="box">
      <template v-for="{field, translationKey, helpTranslationKey} in notificationsFields">
        <b-field :key="field" horizontal>
          <template #label>
            <b-tooltip :label="$t(helpTranslationKey)" multilined position="is-right" class="frequency_label">
              {{ $t(translationKey) }}
              <i class="icon far fa-question-circle"></i>
            </b-tooltip>
          </template>
          <template v-if="windowWidth >= 1024">
            <template v-for="{key, translationKey, color} in frequencies">
              <b-radio-button :key="key" v-model="radioGroups[field]" :native-value="key" :type="color">
                <span>{{ $t(translationKey) }}</span>
              </b-radio-button>
            </template>
          </template>
          <template v-else>
            <b-select v-model="radioGroups[field]" placeholder="Select a name" expanded>
              <option v-for="{key, translationKey} in frequencies" :value="key" :key="key">{{ $t(translationKey) }}</option>
            </b-select>
          </template>
        </b-field>
      </template>
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
      internalUser: null,
      radioGroups: {
        'notif_conversations': String,
        'notif_events': String,
        'notif_items': String
      },
      windowWidth: window.innerWidth
    }
  },
  async created() {
    this.loading = true;

    document.title = 'Shareish | Settings: Notifications';

    window.removeEventListener('resize', this.resizing);

    this.internalUser = {...this.user};

    this.radioGroups.notif_conversations = this.internalUser.mail_notif_freq_conversations;
    this.radioGroups.notif_events = this.internalUser.mail_notif_freq_events;
    this.radioGroups.notif_items = this.internalUser.mail_notif_freq_items;

    this.fetchAddress();

    // Has the user activated geolocation?
    if ("geolocation" in navigator) {
      // Get the position
      navigator.geolocation.getCurrentPosition(positon => {
        this.geoloc = positon;
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
          this.internalUser.mail_notif_freq_conversations = this.radioGroups.notif_conversations;
          this.internalUser.mail_notif_freq_events = this.radioGroups.notif_events;
          this.internalUser.mail_notif_freq_items = this.radioGroups.notif_items;

          let tempUser = {...this.internalUser}
          delete tempUser.images;
          delete tempUser.items;

          this.internalUser = (await axios.patch('/api/v1/users/me/', tempUser)).data;

          this.$buefy.snackbar.open({
            duration: 5000,
            type: 'is-success',
            message: this.$t('notif-success-user-update'),
            pauseOnHover: true,
          });

          this.$emit('updateUser', this.internalUser);

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
    },
    resizing() {
      this.windowWidth = window.innerWidth;
    }
  },
  computed: {
    notificationsFields() {
      return [
        {
          field: 'notif_items',
          translationKey: 'items',
          helpTranslationKey: 'help_notif_items'
        },
        {
          field: 'notif_events',
          translationKey: 'events',
          helpTranslationKey: 'help_notif_events'
        }
      ];
    },
    frequencies() {
      return [
        {
          key: 'I',
          translationKey: 'frequency_instantly',
          color: 'is-primary'
        },
        {
          key: 'D',
          translationKey: 'frequency_daily',
          color: 'is-info'
        },
        {
          key: 'W',
          translationKey: 'frequency_weekly',
          color: 'is-warning'
        },
        {
          key: 'N',
          translationKey: 'frequency_never',
          color: 'is-danger'
        }
      ];
    },
    conversationsFrequencies() {
      return [
        {
          key: 'I',
          translationKey: 'frequency_instantly',
          color: 'is-primary'
        },
        {
          key: 'D',
          translationKey: 'frequency_daily',
          color: 'is-info'
        },
        {
          key: 'N',
          translationKey: 'frequency_never',
          color: 'is-danger'
        }
      ];
    }
  },
  mounted() {
    this.$nextTick(() => {
      window.addEventListener('resize', this.resizing);
    });
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizing);
  },
};
</script>

<style scoped>
.frequency_label {
  min-width: 150px;
}

@media screen and (max-width: 1215px) {
  .tile.is-ancestor, .tile.is-parent {
    display: block;
  }
}
</style>
