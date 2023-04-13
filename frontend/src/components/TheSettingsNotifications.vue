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
                <b-button type="is-primary" @click="fetchAddressGeoLoc">
                  <i class="icon fas fa-map-marker-alt"></i>
                </b-button>
                <b-input v-model="address" class="is-expanded ml-2" name="ref_location" type="text" />
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
    <b-button :label="$t('save')" :loading="waitingFormResponse" type="is-primary" @click="save" />
  </section>
</template>


<script>
import axios from "axios";
import ErrorHandler from "@/mixins/ErrorHandler";
import WindowSize from "@/mixins/WindowSize";
import {GeolocationCoords} from "@/functions";

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
  data() {
    return {
      loading: true,
      geoLocation: null,
      internalUser: null,
      refLocation: null,
      address: null,
      radioGroups: {
        'notif_conversations': String,
        'notif_events': String,
        'notif_items': String
      },
      waitingFormResponse: false
    }
  },
  async created() {
    this.loading = true;

    document.title = 'Shareish | Settings: Notifications';

    this.internalUser = {...this.user};
    if (this.internalUser.ref_location !== null) {
      this.refLocation = new GeolocationCoords(this.internalUser.ref_location);
      this.address = await this.fetchAddress(this.refLocation);
    }

    this.radioGroups.notif_conversations = this.internalUser.mail_notif_freq_conversations;
    this.radioGroups.notif_events = this.internalUser.mail_notif_freq_events;
    this.radioGroups.notif_items = this.internalUser.mail_notif_freq_items;

    // Has the user activated geolocation?
    if ('geolocation' in navigator) {
      // Get the position
      navigator.geolocation.getCurrentPosition(
        position => {
          this.geoLocation = new GeolocationCoords(position);
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
    async fetchAddressGeoLoc() {
      if (this.geoLocation !== null)
        this.address = await this.fetchAddress(this.geoLocation);
      else
        this.snackbarError(this.$t('enable-geolocation-to-use-feature'));
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
      return null
    },
    async save() {
      this.waitingFormResponse = true;

      let result = await this.$validator.validateAll();
      if (result) {
        try {
          this.internalUser.mail_notif_freq_conversations = this.radioGroups.notif_conversations;
          this.internalUser.mail_notif_freq_events = this.radioGroups.notif_events;
          this.internalUser.mail_notif_freq_items = this.radioGroups.notif_items;

          let tempUser = {...this.internalUser}
          tempUser.ref_location = this.address;
          delete tempUser.images;
          delete tempUser.items;

          this.internalUser = (await axios.patch("/api/v1/webusers/me/", tempUser)).data;
          this.$emit('updateUser', this.internalUser);

          if (this.internalUser.ref_location !== null) {
            if (this.refLocation === null) {
              this.refLocation = new GeolocationCoords(this.internalUser.ref_location);
            } else {
              this.refLocation.update(this.internalUser.ref_location);
            }
            this.address = await this.fetchAddress(this.refLocation);
          } else {
            this.refLocation = null;
            this.address = null;
          }

          this.$buefy.snackbar.open({
            duration: 5000,
            type: 'is-success',
            message: this.$t('notif-success-user-update'),
            pauseOnHover: true,
          });
        } catch (error) {
          this.fullErrorHandling(error);
        }
      }

      this.waitingFormResponse = false;
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
