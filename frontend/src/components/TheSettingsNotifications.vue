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
                <b-tooltip :label="$t('use-geolocation')" type="is-info" position="is-bottom">
                  <b-button type="is-info" @click="useGeoLocAddress">
                    <i class="fas fa-street-view"></i>
                  </b-button>
                </b-tooltip>
                <address-auto-complete v-model="address" :location="this.geoLocation" class="is-expanded ml-2"/>
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
            <b-slider
                v-model="internalUser['dwithin_notifications']"
                :max="99"
                :tooltip="false"
                class="mt-5 pl-3 pr-3"
                format="raw"
                indicator
            />
          </b-field>
        </div>
      </div>
    </div>
    <div class="box">
      <b-field v-for="{field, translationKey, helpTranslationKey} in notificationsFields" :key="field" horizontal>
        <template #label>
          <b-tooltip :label="$t(helpTranslationKey)" class="frequency_label" multilined position="is-right">
            {{ $t(translationKey) }}
            <i class="icon far fa-question-circle"></i>
          </b-tooltip>
        </template>
        <template v-if="windowWidth >= 1024">
          <b-radio-button
              v-for="{key, translationKey, color} in frequencies"
              :key="key"
              v-model="radioGroups[field]"
              :native-value="key" :type="color"
          >
            <span>{{ $t(translationKey) }}</span>
          </b-radio-button>
        </template>
        <template v-else>
          <b-select v-model="radioGroups[field]" expanded placeholder="Select a name">
            <option v-for="{key, translationKey} in frequencies" :key="key" :value="key">
              {{ $t(translationKey) }}
            </option>
          </b-select>
        </template>
      </b-field>
    </div>
    <div class="box">
      <b-field key="notif_osm" horizontal>
        <template #label>
          <b-tooltip :label="$t('help_notif_osm')" class="frequency_label" multilined position="is-right">
            {{ $t('public_resource_osm') }}
            <i class="icon far fa-question-circle"></i>
          </b-tooltip>
        </template>
        <template v-if="windowWidth >= 1024">
          <b-radio-button
              v-for="{key, translationKey, color} in OSMFrequencies"
              :key="key"
              v-model="radioGroups['notif_osm']"
              :native-value="key"
              :type="color"
          >
            <span>{{ $t(translationKey) }}</span>
          </b-radio-button>
        </template>
        <template v-else>
          <b-select v-model="radioGroups['notif_osm']" expanded placeholder="Select a frequency">
            <option v-for="{key, translationKey} in frequencies" :key="key" :value="key">
              {{ $t(translationKey) }}
            </option>
          </b-select>
        </template>
      </b-field>
    </div>
    <div class="box">
      <b-field key="notif_conversations" horizontal>
        <template #label>
          <b-tooltip :label="$t('help_notif_conversations')" class="frequency_label" multilined position="is-right">
            {{ $t('conversations') }}
            <i class="icon far fa-question-circle"></i>
          </b-tooltip>
        </template>
        <template v-if="windowWidth >= 1024">
          <b-radio-button
              v-for="{key, translationKey, color} in conversationsFrequencies"
              :key="key"
              v-model="radioGroups['notif_conversations']"
              :native-value="key"
              :type="color"
          >
            <span>{{ $t(translationKey) }}</span>
          </b-radio-button>
        </template>
        <template v-else>
          <b-select v-model="radioGroups['notif_conversations']" expanded placeholder="Select a frequency">
            <option v-for="{key, translationKey} in frequencies" :key="key" :value="key">
              {{ $t(translationKey) }}
            </option>
          </b-select>
        </template>
      </b-field>
    </div>
    <div class="box">
      <b-field key="notif_generalinfo" horizontal>
        <template #label>
          <b-tooltip :label="$t('help_notif_generalinfo')" class="frequency_label" multilined position="is-right">
            {{ $t('notif_generalinfo') }}
            <i class="icon far fa-question-circle"></i>
          </b-tooltip>
        </template>
        <template v-if="windowWidth >= 1024">
          <b-radio-button
              v-for="{key, translationKey, color} in GeneralInfoFrequencies"
              :key="key"
              v-model="radioGroups['notif_generalinfo']"
              :native-value="key"
              :type="color"
          >
            <span>{{ $t(translationKey) }}</span>
          </b-radio-button>
        </template>
        <template v-else>
          <b-select v-model="radioGroups['notif_generalinfo']" expanded placeholder="Select a frequency">
            <option v-for="{key, translationKey} in frequencies" :key="key" :value="key">
              {{ $t(translationKey) }}
            </option>
          </b-select>
        </template>
      </b-field>
    </div>
    <b-button :label="$t('save')" :loading="waitingFormResponse" type="is-primary" @click="save" />
  </section>
</template>


<script>
import axios from "axios";
import ErrorHandler from "@/mixins/ErrorHandler";
import WindowSize from "@/mixins/WindowSize";
import {GeolocationCoords, isNotEmptyString} from "@/functions";
import AddressAutoComplete  from "@/components/AddressAutoComplete.vue";
export default {
  name: 'TheSettingsNotifications',
  mixins: [ErrorHandler, WindowSize],
  $_veeValidate: {
    validator: 'new'
  },
  props: {
    user: {
      type: Object,
      required: true
    }
  },
  components:{
    AddressAutoComplete ,
  },
  data() {
    return {
      loading: true,
      geoLocation: null,
      geoLocationAddress: "",
      checkAddress: false,
      suggestedAddresses: [],
      internalUser: null,
      address: "",
      radioGroups: {
        'notif_conversations': String,
        'notif_events': String,
        'notif_items': String,
        'notif_osm': String,
        'notif_generalinfo': String,
      },
      waitingFormResponse: false,
      timeouts: {}
    }
  },
  async created() {
    this.loading = true;

    document.title = 'Shareish | Settings: Notifications';

    this.internalUser = {
      'dwithin_notifications': this.user.dwithin_notifications,
      'mail_notif_freq_conversations': this.user.mail_notif_freq_conversations,
      'mail_notif_freq_events': this.user.mail_notif_freq_events,
      'mail_notif_freq_items': this.user.mail_notif_freq_items,
      'mail_notif_freq_osm': this.user.mail_notif_freq_osm,
      'mail_notif_generalinfo': this.user.mail_notif_generalinfo,	
    };

    if (this.user.ref_location !== null) {
      this.internalUser.ref_location = new GeolocationCoords(this.user.ref_location);
      this.checkAddress = false;
      this.address = await this.fetchAddress(this.internalUser.ref_location);
    } else {
      this.internalUser.ref_location = null;
    }

    this.radioGroups.notif_conversations = this.internalUser.mail_notif_freq_conversations;
    this.radioGroups.notif_events = this.internalUser.mail_notif_freq_events;
    this.radioGroups.notif_items = this.internalUser.mail_notif_freq_items;
    this.radioGroups.notif_osm = this.internalUser.mail_notif_freq_osm;
    this.radioGroups.notif_generalinfo = this.internalUser.mail_notif_generalinfo;  

      
    // Has the user activated geolocation?
    if ('geolocation' in navigator) {
      // Get the position
      navigator.geolocation.getCurrentPosition(
        async position => {
          this.geoLocation = new GeolocationCoords(position);
          this.geoLocationAddress = await this.fetchAddress(this.geoLocation);
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
  watch: {
    address() {
      if (this.checkAddress) {
        clearTimeout(this.timeouts['address']);
        this.timeouts['address'] = setTimeout(async () => {
          if (isNotEmptyString(this.address)) {
            const geolocation = await this.fetchGeolocation(this.address);
            if (geolocation !== null)
              this.suggestedAddresses = [await this.fetchAddress(geolocation)];
          }
        }, 750);
      } else {
        this.checkAddress = true;
      }
    }
  },
  methods: {
    async useGeoLocAddress() {
      if (this.geoLocation instanceof GeolocationCoords) {
        this.checkAddress = false;
        this.address = this.geoLocationAddress;
      } else {
        this.snackbarError(this.$t('enable-geolocation-to-use-feature'));
      }
    },
    async fetchAddress(location) {
      if (location instanceof GeolocationCoords) {
        try {
          return (await axios.post("/api/v1/address/reverse", location)).data;
        }
        catch (error) {
          this.fullErrorHandling(error);
        }
      }
      return null;
    },
    async fetchGeolocation(address) {
      if (isNotEmptyString(address)) {
        try {
          const formData = new FormData();
          formData.append('address', address);
          const location = (await axios.post("/api/v1/address", formData)).data;
          if (location !== null)
            return new GeolocationCoords(location);
        }
        catch (error) {
          this.fullErrorHandling(error);
        }
      }
      return null;
    },
    async save() {
      this.waitingFormResponse = true;

      clearTimeout(this.timeouts['save']);
      this.timeouts['save'] = setTimeout(async () => {
        let result = await this.$validator.validateAll();
        if (result) {
          try {
            if (isNotEmptyString(this.address)) {
              const newRefLocation = await this.fetchGeolocation(this.address);
              if (newRefLocation instanceof GeolocationCoords) {
                console.log("oki !")
                this.internalUser.ref_location = newRefLocation;
                this.address = await this.fetchAddress(this.internalUser.ref_location);
              } else {
                this.internalUser.ref_location = null;
              }
            } else {
              this.internalUser.ref_location = null;
            }

            this.internalUser.mail_notif_freq_conversations = this.radioGroups.notif_conversations;
            this.internalUser.mail_notif_freq_events = this.radioGroups.notif_events;
            this.internalUser.mail_notif_freq_items = this.radioGroups.notif_items;
            this.internalUser.mail_notif_freq_osm = this.radioGroups.notif_osm;
            this.internalUser.mail_notif_generalinfo = this.radioGroups.notif_generalinfo;

            if (this.internalUser.ref_location instanceof GeolocationCoords)
              this.internalUser.ref_location = this.internalUser.ref_location.toString();

            await axios.patch("/api/v1/webusers/me/", this.internalUser);

            this.$emit('updateUser', this.internalUser);

            this.$buefy.snackbar.open({
              duration: 5000,
              type: 'is-success',
              message: this.$t('notif-success-user-update'),
              pauseOnHover: true
            });
          }
          catch (error) {
            this.fullErrorHandling(error);
          }
        }

        this.waitingFormResponse = false;
      }, 400);
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
        },
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
    },
    OSMFrequencies() {
      return [
        {
          key: 'D',
          translationKey: 'frequency_daily',
          color: 'is-primary'
        },
	{
          key: 'W',
          translationKey: 'frequency_weekly',
          color: 'is-info'
        },
	{
          key: 'M',
          translationKey: 'frequency_monthly',
          color: 'is-warning'
        },
        {
          key: 'N',
          translationKey: 'frequency_never',
          color: 'is-danger'
        }
      ];
    },
    GeneralInfoFrequencies() {
      return [
        {
          key: true,
          translationKey: 'frequency_always',
          color: 'is-primary'
        },
        {
          key: false,
          translationKey: 'frequency_never',
          color: 'is-danger'
        }
      ];
    }
      
  }
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
