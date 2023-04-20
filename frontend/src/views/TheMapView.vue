<template>
  <div id="page-map">
    <div id="map-surrounding">
      <l-map
          :bounds.sync="bounds"
          :center.sync="leafletCenter"
          :zoom.sync="zoom"
          id="leaflet-map"
          @update:bounds="boundsUpdated"
      >
        <l-tile-layer :attribution="attribution" :options="tileLayerOptions" :url="url"></l-tile-layer>
        <l-control position="topright">
          <div class="is-flex is-flex-direction-column">
            <b-tooltip :label="$t('use-geolocation')" position="is-left" type="is-info" class="w-100 mt-1">
              <b-button type="is-info" @click="setCenterAtGeoLocation" expanded>
                <i class="fas fa-street-view"></i>
              </b-button>
            </b-tooltip>
            <b-tooltip :label="$t('use-reflocation')" position="is-left" type="is-info" class="w-100 mt-1">
              <b-button type="is-info" @click="setCenterAtRefLocation" expanded>
                <i class="fas fa-home"></i>
              </b-button>
            </b-tooltip>
            <b-tooltip :label="$t('open-map-settings')" position="is-left" type="is-primary" class="w-100 mt-1">
              <b-button type="is-primary" @click="openFlap('settings')" expanded>
                <i class="fas fa-cog"></i>
              </b-button>
            </b-tooltip>
            <b-tooltip :label="$t('filter-items')" position="is-left" type="is-primary" class="w-100 mt-1">
              <b-button type="is-primary" @click="openFlap('filters')" expanded>
                <i class="fas fa-filter"></i>
              </b-button>
            </b-tooltip>
          </div>
        </l-control>
        <l-control position="bottomleft">
          <div class="control-loading">
            <i v-show="mapLoading" class="fas fa-spinner fa-2x fa-pulse"></i>
          </div>
          <div v-show="zoom < minZoomToShowElements" class="control-zoom-info leaflet-control-attribution">
            {{ $t('too-small-zoom') }}
          </div>
        </l-control>

        <l-marker v-if="geoLocation" :icon="geoLocationIcon" :lat-lng="geoLocation.leafletLatLng" />
        <l-marker v-if="refLocation" :icon="geoLocationIcon" :lat-lng="refLocation.leafletLatLng" />

        <l-layer-group v-if="zoom >= minZoomToShowElements">
          <v-marker-cluster :options="markerClusterGroupOptions">
            <l-marker
                v-for="item in items"
                :key="item.id"
                :ref="'marker-item-' + item.id"
                :icon="item.icon"
                :lat-lng="item.location.leafletLatLng"
            >
              <l-popup :options="{className:'item-popup', maxWidth: '500'}">
                <item-map-popup :item="item" />
              </l-popup>
            </l-marker>
          </v-marker-cluster>
        </l-layer-group>
        <l-feature-group v-if="zoom >= minZoomToShowElements">
          <l-layer-group>
            <v-marker-cluster :options="extraLayersMarkerClusterGroupOptions">
              <template v-for="extraCategory in user.map_ecats">
                <l-marker
                    v-for="marker in extraCategories[extraCategory.category].markers"
                    :key="marker.id"
                    :icon="extraCategoriesIcons[extraCategories[extraCategory.category].id]"
                    :lat-lng="marker.location.leafletLatLng"
                    :visible="extraCategory.selected"
                >
                  <l-popup>
                    <div v-if="marker.name"><strong>{{ marker.name }}</strong></div>
                    <div class="is-grey">{{ $tc('map_ecat_' + extraCategory.category, 1) }}</div>
                    <div v-if="marker.description">{{ marker.description }}</div>
                    <div class="is-grey is-size-7 has-text-right is-italic">
                      <a :href="getMarkerURL(extraCategory.category, marker.id)" target="_blank">
                        <span><i class="fas fa-external-link-alt"></i></span>
                        <span>{{ $t(extraCategory.category === 'FLF' ? 'from-ff' : 'from-osm') }}</span>
                      </a>
                    </div>
                  </l-popup>
                </l-marker>
              </template>
            </v-marker-cluster>
          </l-layer-group>
        </l-feature-group>
      </l-map>
      <div id="flap">
        <div class="inner">
          <div v-if="flapSelected === 'settings'" class="settings">
            <header class="is-flex">
              <h2 class="title">{{ $t('settings') }}</h2>
              <b-button
                  type="is-dark"
                  outlined
                  class="close"
                  @click="closeFlap"
              >
                <i class="fas fa-times"></i>
              </b-button>
            </header>
            <div class="content">
              <h3 class="title is-size-4 mb-1">OpenStreetMap & Falling Fruit</h3>
              <p class="subtitle is-size-6 mt-0 mb-5">{{ $t('define-elements-to-see-on-map') }}</p>
              <div class="columns is-mobile buttons m-0 mb-4">
                <div class="column p-0 pr-2">
                  <b-button expanded type="is-primary" @click="selectAll">{{ $t('select-all') }}</b-button>
                </div>
                <div class="column p-0 pl-2">
                  <b-button expanded type="is-danger" @click="deselectAll">{{ $t('deselect-all') }}</b-button>
                </div>
              </div>
              <div id="ecats-checkboxes" class="columns is-mobile is-flex-wrap-wrap m-0">
                <div v-for="(extraCategory, index) in user.map_ecats" :key="index" class="column is-half p-0 pb-2" :class="{'pr-2': index % 2 === 0, 'pl-2': index % 2 !== 0}">
                  <b-field>
                    <b-checkbox v-model="ecatsCheckboxes" :native-value="extraCategory.category" type="is-primary">
                      <img :src="extraCategoriesIcons[extraCategories[extraCategory.category].id].options.iconUrl" style="width: 24px; vertical-align: middle;" class="mr-1">
                      {{ $tc('map_ecat_' + extraCategory.category, 0) }}
                    </b-checkbox>
                  </b-field>
                </div>
              </div>
              <div class="buttons mt-3 is-flex is-justify-content-center">
                <b-button
                    :label="$t('save')"
                    type="is-primary"
                    :loading="waitingFormResponse"
                    @click="saveExtraCategories"
                />
              </div>
            </div>
          </div>
          <div v-else-if="flapSelected === 'filters'" class="filters">
            <header class="is-flex">
              <h2 class="title">{{ $tc('filter', 0) }}</h2>
              <b-button
                  type="is-dark"
                  outlined
                  class="close"
                  @click="closeFlap"
              >
                <i class="fas fa-times"></i>
              </b-button>
            </header>
            <div class="content">
              <div id="filters">
                <div class="search">
                  <b-field :label="$t('search')">
                    <b-input v-model="searchString" :placeholder="$t('name') + ', ' + lcall($t('description')) + ' ' + lcall($t('or')) + ' ' + lcall($t('author'))" />
                  </b-field>
                </div>
                <div class="other-filters mt-4">
                  <toggle-box :title="$tc('type', 0)" outlined :title-size="6" class="mt-3">
                    <template v-if="windowWidth >= 768 && windowWidth < 1024">
                      <div class="columns is-mobile">
                        <div class="column pr-2">
                          <b-field class="mb-1">
                            <b-checkbox-button v-model="searchTypes" native-value="DN" type="is-success">
                              <span>{{ $t('donation') }}</span>
                            </b-checkbox-button>
                          </b-field>
                        </div>
                        <div class="column pr-2 pl-2">
                          <b-field class="mb-1">
                            <b-checkbox-button v-model="searchTypes" native-value="RQ" type="is-danger">
                              <span>{{ $t('request') }}</span>
                            </b-checkbox-button>
                          </b-field>
                        </div>
                        <div class="column pr-2 pl-2">
                          <b-field class="mb-1">
                            <b-checkbox-button v-model="searchTypes" native-value="LN" type="is-warning">
                              <span>{{ $t('loan') }}</span>
                            </b-checkbox-button>
                          </b-field>
                        </div>
                        <div class="column pl-2">
                          <b-field class="mb-1">
                            <b-checkbox-button v-model="searchTypes" native-value="EV" type="is-purple">
                              <span>{{ $t('event') }}</span>
                            </b-checkbox-button>
                          </b-field>
                        </div>
                      </div>
                    </template>
                    <template v-else>
                      <b-field class="mb-1">
                        <b-checkbox-button v-model="searchTypes" native-value="DN" type="is-success">
                          <span>{{ $t('donation') }}</span>
                        </b-checkbox-button>
                      </b-field>
                      <b-field class="mb-1">
                        <b-checkbox-button v-model="searchTypes" native-value="RQ" type="is-danger">
                          <span>{{ $t('request') }}</span>
                        </b-checkbox-button>
                      </b-field>
                      <b-field class="mb-1">
                        <b-checkbox-button v-model="searchTypes" native-value="LN" type="is-warning">
                          <span>{{ $t('loan') }}</span>
                        </b-checkbox-button>
                      </b-field>
                      <b-field class="mb-1">
                        <b-checkbox-button v-model="searchTypes" native-value="EV" type="is-purple">
                          <span>{{ $t('event') }}</span>
                        </b-checkbox-button>
                      </b-field>
                    </template>
                  </toggle-box>
                  <toggle-box :title="$tc('category', 0)" outlined :title-size="6" class="mt-3">
                    <div v-if="searchCategories.length > 0" id="selected-categories">
                      <p class="has-text-weight-bold mb-2">{{ $t('searched-categories') }}:</p>
                      <div v-for="category in searchCategories" :key="category" class="selected-category columns is-mobile">
                        <div class="column name">{{ getCategory(category) }}</div>
                        <div class="column close" @click="removeCategory(category)"><i class="fas fa-times-circle"></i></div>
                      </div>
                    </div>
                    <template v-else>
                      <p class="mb-2"><small>{{ $t('no-categories-selected-for-search') }}</small></p>
                    </template>
                    <category-selector v-model="selectedCategory" expanded />
                  </toggle-box>
                  <toggle-box :title="$t('availability')" outlined :title-size="6" class="mt-3">
                    <b-field :label="$t('from')">
                      <b-datetimepicker
                          v-model="searchAvailabilityFrom"
                          icon="calendar"
                          :icon-right="searchAvailabilityFrom ? 'close-circle' : ''"
                          icon-right-clickable
                          @icon-right-click="searchAvailabilityFrom = null"
                          icon-pack="fas"
                          :locale="$i18n.locale"
                      />
                    </b-field>
                    <b-field :label="$t('until')">
                      <b-datetimepicker
                          v-model="searchAvailabilityUntil"
                          icon="calendar"
                          :icon-right="searchAvailabilityUntil ? 'close-circle' : ''"
                          icon-right-clickable
                          @icon-right-click="searchAvailabilityUntil = null"
                          icon-pack="fas"
                          :locale="$i18n.locale"
                      />
                    </b-field>
                  </toggle-box>
                  <toggle-box :title="$t('publication')" outlined :title-size="6" class="mt-3">
                    <b-field>
                      <b-switch v-model="onlyUnseen" type="is-primary">{{ $t('show-only-unseen') }}</b-switch>
                    </b-field>
                    <b-field>
                      <b-switch v-model="useMinCreactiondate" type="is-primary">{{ $t('filter-items-creationdate') }}</b-switch>
                    </b-field>
                    <template v-if="useMinCreactiondate">
                      <div class="columns is-mobile mb-0 mt-3">
                        <div class="column pr-1">
                            <b-slider v-model="sliderTimeUnit" class="pr-5 pl-4" :min="1" :max="sliderTimeUnitMax" :step="1" indicator :tooltip="false" />
                        </div>
                        <div class="column pl-1" style="flex: 0 0 auto;">
                          <b-select v-model="timeUnit" :placeholder="$t('unit')">
                              <option value="days">{{ $tc('day', 0) }}</option>
                              <option value="hours">{{ $tc('hour', 0) }}</option>
                              <option value="minutes">{{ $tc('minute', 0) }}</option>
                          </b-select>
                        </div>
                      </div>
                      <p v-if="timeUnit === 'days'">{{ $t('only-items-created-on') }} <b>{{ formattedDay(minCreationdate) }}</b> {{ $t('will-be-showed') }}.</p>
                      <p v-else>{{ $t('only-items-created-on') }} <b>{{ formattedDay(minCreationdate) }}</b> {{ $t('created-at') }} <b>{{ formattedHour(minCreationdate) }}</b> {{ $t('will-be-showed') }}.</p>
                    </template>
                  </toggle-box>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as L from 'leaflet'; // do not remove for markercluster
import "leaflet.markercluster";
import "leaflet-easybutton";
import axios from "axios"

import {
  greenIcon,
  yellowIcon,
  redIcon,
  greyIcon,
  eventIcon,
  publicBookcaseIcon,
  aedIcon,
  giveBoxIcon,
  drinkingWaterIcon, freeShopIcon, foodSharingIcon, foodBankIcon, soupKitchenIcon, fallingfruitIcon, blueIcon
} from "@/map-icons";

import {LMap, LTileLayer, LControl, LMarker, LPopup, LFeatureGroup, LLayerGroup} from "vue2-leaflet";
import Vue2LeafletMarkercluster from "vue2-leaflet-markercluster";
import ItemMapPopup from "@/components/ItemMapPopup.vue";
import ErrorHandler from "@/mixins/ErrorHandler";
import {GeolocationCoords, lcall, ucfirst} from "@/functions";
import {LatLng} from "leaflet/dist/leaflet-src.esm";
import WindowSize from "@/mixins/WindowSize";
import ToggleBox from "@/components/ToggleBox.vue";
import CategorySelector from "@/components/CategorySelector.vue";
import moment from "moment";
import {categories} from "@/categories";

const itemTypeIcons = {
  'DN': greenIcon,
  'LN': yellowIcon,
  'RQ': redIcon,
  'EV': eventIcon
}

export default {
  name: 'TheMapView',
  mixins: [ErrorHandler, WindowSize],
  components: {
    CategorySelector,
    ToggleBox,
    ItemMapPopup,
    LMap,
    LTileLayer,
    LControl,
    LLayerGroup,
    LPopup,
    LMarker,
    LFeatureGroup,
    'v-marker-cluster': Vue2LeafletMarkercluster
  },
  data() {
    return {
      mapLoading: true,
      zoom: 14,
      preLeafletCenter: new LatLng(50.6450944, 5.5736112),
      leafletCenter: new LatLng(50.6450944, 5.5736112),
      flapOpened: false,
      flapSelected: null,
      ecatsCheckboxes: [],
      waitingFormResponse: false,

      isMoreFiltersOpened: false,
      bounds: null,
      searchBounds: null,
      searchString: null,
      searchTypes: ['DN', 'LN', 'RQ', 'EV'],
      searchCategories: [],
      selectedCategory: null,
      searchAvailabilityFrom: null,
      searchAvailabilityUntil: null,
      geoLocation: null,
      refLocation: null,
      onlyUnseen: false,
      useMinCreactiondate: false,
      timeUnit: 'hours',
      sliderTimeUnitMemory: {
        'days': 1,
        'hours': 1,
        'minutes': 1
      },
      sliderTimeUnitMaximums: {
        'days': 31,
        'hours': 24,
        'minutes': 60
      },
      sliderTimeUnit: 1,
      minCreationdate: new Date(),
      searchMinCreationdate: null,
      initialItemsLoadDone: false,
      user: {},

      url: "https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png",
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>',
      tileLayerOptions: {
        zoom: 14,
        maxZoom: 19
      },
      markerClusterGroupOptions: {
        // disableClusteringAtZoom: 16,
        chunkedLoading: true,
        maxClusterRadius: 25,
        disableClusteringAtZoom: 15
      },
      minZoomToShowElements: 12,
      extraLayersMarkerClusterGroupOptions: {
        disableClusteringAtZoom: 15,
        chunkedLoading: true,
        maxClusterRadius: 30
      },
      extraCategories: {
        'BKC': {
          id: 'bookcases',
          markers: [],
          tagValue: 'public_bookcase'
        },
        'DEF': {
          id: 'defibrillators',
          markers: [],
          tagValue: 'defibrillator'
        },
        'DWS': {
          id: 'drinking-water-spots',
          markers: [],
          tagValue: 'drinking_water'
        },
        'FDB': {
          id: 'food-banks',
          markers: [],
          tagValue: 'food_bank'
        },
        'FDS': {
          id: 'food-sharings',
          markers: [],
          tagValue: 'food_sharing'
        },
        'FLF': {
          id: 'falling-fruits',
          markers: [],
          tagValue: 'ffruit'
        },
        'FRS': {
          id: 'free-shops',
          markers: [],
          tagValue: 'free_shop'
        },
        'GVB': {
          id: 'give-boxes',
          markers: [],
          tagValue: 'give_box'
        },
        'SPK':  {
          id: 'soup-kitchens',
          markers: [],
          tagValue: 'soup_kitchen'
        }
      },
      extraLayersTagsOverpass: {
        'public_bookcase': 'amenity',
        'defibrillator': 'emergency',
        'give_box': 'amenity',
        'food_bank': 'social_facility',
        'food_sharing': 'amenity',
        'soup_kitchen': 'social_facility',
        'drinking_water': 'amenity',
        'free_shop': 'amenity'
      },
      extraCategoriesIcons: {
        'bookcases': publicBookcaseIcon,
        'defibrillators': aedIcon,
        'give-boxes': giveBoxIcon,
        'drinking-water-spots': drinkingWaterIcon,
        'free-shops': freeShopIcon,
        'food-sharings': foodSharingIcon,
        'food-banks': foodBankIcon,
        'soup-kitchens': soupKitchenIcon,
        'falling-fruits': fallingfruitIcon
      },
      geoLocationIcon: blueIcon,
      routedItemLocation: null,
      items: [],

      routedItemError: false,
      timeouts: {}
    }
  },
  async created() {
    document.title = `Shareish | ${this.$t('map')}`;

    await this.updateGeoLocation();
    await this.fetchUser();

    for (const i in this.user.map_ecats) {
      if (this.user.map_ecats[i].selected === true)
        this.ecatsCheckboxes.push(this.user.map_ecats[i].category)
    }

    if (this.geoLocation instanceof GeolocationCoords)
      this.preLeafletCenter = this.geoLocation.leafletLatLng;
    else if (this.refLocation instanceof GeolocationCoords)
      this.preLeafletCenter = this.refLocation.leafletLatLng;

    if (this.itemId !== null)
      await this.fetchRoutedItem();

    this.leafletCenter = this.preLeafletCenter;

    this.mapLoading = false;
  },
  computed: {
    params() {
      return {
        search: this.searchString,
        types: this.searchTypes,
        categories: this.searchCategories,
        onlyNew: (this.onlyUnseen) ? this.onlyUnseen : null,
        availableFrom: this.searchAvailabilityFrom,
        availableUntil: this.searchAvailabilityUntil,
        minCreationdate: this.searchMinCreationdate
      };
    },
    itemId() {
      return (this.$route.query.id) ? Number(this.$route.query.id) : null;
    },
    userId() {
      return Number(this.$store.state.user.id);
    },
    sliderTimeUnitMax() {
      return this.sliderTimeUnitMaximums[this.timeUnit];
    }
  },
  watch: {
    useMinCreactiondate() {
      if (this.useMinCreactiondate)
        this.updateSearchMinCreationdate();
      else
        this.searchMinCreationdate = null;
    },
    timeUnit() {
      this.sliderTimeUnit = this.sliderTimeUnitMemory[this.timeUnit];
      this.updateSearchMinCreationdate();
    },
    sliderTimeUnit() {
      this.sliderTimeUnitMemory[this.timeUnit] = this.sliderTimeUnit;
      this.updateSearchMinCreationdate();
    },
    selectedCategory() {
      if (this.searchCategories.indexOf(this.selectedCategory) === -1)
        this.searchCategories.push(this.selectedCategory);
    },
    params() {
      if (this.initialItemsLoadDone)
        this.fetchMathElements();
    }
  },
  methods: {
    ucfirst,
    lcall,
    async saveExtraCategories() {
      this.waitingFormResponse =  true;

      try {
        const data = {};
        data['map_ecats'] = []
        for (const [index, extraCategory] of Object.entries(this.user.map_ecats))
          data['map_ecats'].push({
            'category': extraCategory.category,
            'selected': this.ecatsCheckboxes.includes(extraCategory.category)
          });

        await axios.patch(`/api/v1/webusers/${this.userId}/`, data);

        this.$buefy.snackbar.open({
          duration: 5000,
          type: 'is-success',
          message: this.$t('map-settings-saved'),
          pauseOnHover: true,
          queue: false
        });

        for (const i in this.user.map_ecats)
          this.user.map_ecats[i].selected = this.ecatsCheckboxes.includes(this.user.map_ecats[i].category);
      }
      catch (error) {
        this.snackbarError(error);
      }

      this.waitingFormResponse =  false;
    },
    selectAll() {
      for (const i in this.user.map_ecats) {
        if (!this.ecatsCheckboxes.includes(this.user.map_ecats[i].category))
          this.ecatsCheckboxes.push(this.user.map_ecats[i].category);
      }
    },
    deselectAll() {
      this.ecatsCheckboxes = [];
    },
    updateSearchMinCreationdate() {
      this.minCreationdate = this.getMinCreationdate();

      clearTimeout(this.timeouts['searchMinCreationdate']);
      this.timeouts['searchMinCreationdate'] = setTimeout(() => {
        this.searchMinCreationdate = this.minCreationdate;
      }, 600);
    },
    getMinCreationdate() {
      let minCreationdate = new Date();

      switch (this.timeUnit) {
        case 'days':
          minCreationdate.setDate(minCreationdate.getDate() - this.sliderTimeUnit);
          minCreationdate.setHours(0);
          minCreationdate.setMinutes(0);
          break;
        case 'hours':
          minCreationdate.setHours(minCreationdate.getHours() - this.sliderTimeUnit);
          minCreationdate.setMinutes(0);
          break;
        case 'minutes':
          minCreationdate.setMinutes(minCreationdate.getMinutes() - this.sliderTimeUnit);
          break;
      }
      minCreationdate.setSeconds(0);
      minCreationdate.setMilliseconds(0);

      return minCreationdate;
    },
    formattedDay(date) {
      return (moment(date).locale(this.$i18n.locale).format("DD/MM/YYYY"));
    },
    formattedHour(date) {
      return (moment(date).locale(this.$i18n.locale).format("HH:mm"));
    },
    getCategory(category) {
      if (category in categories) {
        return this.$t(categories[category]['slug']);
      }
      return "";
    },
    removeCategory(category) {
      const index = this.searchCategories.indexOf(category);
      if (index > -1)
        this.searchCategories.splice(index, 1);
    },
    async fetchUser() {
      try {
        const params = {
          columns: ['ref_location', 'map_ecats']
        }
        this.user = (await axios.get(`api/v1/webusers/${this.userId}`, {params: params})).data;
        if (this.user.ref_location !== null)
          this.refLocation = new GeolocationCoords(this.user.ref_location);
      }
      catch (error) {
        this.snackbarError(error);
      }
    },
    async updateGeoLocation() {
      // Has the user activated geolocation?
      if ('geolocation' in navigator) {
        // Get the position
        try {
          const position = await new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve, reject, {
              maximumAge: 10000,
              timeout: 5000,
              enableHighAccuracy: true
            });
          });

          if (this.geoLocation instanceof GeolocationCoords)
            this.geoLocation.update(position);
          else
            this.geoLocation = new GeolocationCoords(position);
        }
        catch {}
      }
    },
    async setCenterAtGeoLocation() {
      await this.updateGeoLocation();
      if (this.geoLocation instanceof GeolocationCoords)
        this.leafletCenter = this.geoLocation.leafletLatLng;
      else
        this.snackbarError(this.$t('enable-geolocation-to-use-feature'));
    },
    async setCenterAtRefLocation() {
      if (this.refLocation instanceof GeolocationCoords)
        this.leafletCenter = this.refLocation.leafletLatLng;
      else
        this.snackbarError(this.$t('set-a-reflocation-to-use-feature'));
    },
    openFlap(name) {
      this.flapOpened = true;
      this.flapSelected = name;

      const flap = this.$el.querySelector("#flap");
      if (this.windowWidth < 700) {
        flap.style.width = "calc(100% - 2 * .5rem)";
        flap.style.left = "0.5rem";
      } else {
        if (this.flapSelected === 'settings') {
          flap.style.width = "550px";
        } else if (this.flapSelected === 'filters') {
          flap.style.width = "450px";
        }
        flap.style.left = "calc(100% - " + flap.style.width + " - 0.5rem)";
      }
    },
    closeFlap() {
      if (this.flapOpened) {
        const flap = this.$el.querySelector("#flap");
        flap.style.left = "100%";
      }
    },
    async fetchRoutedItem() {
      try {
        const routedItem = (await axios.get(`/api/v1/items/${this.itemId}`)).data;
        if (routedItem.location !== null) {
          this.routedItemLocation = new GeolocationCoords(routedItem.location);
          this.preLeafletCenter = this.routedItemLocation.leafletLatLng;
        } else {
          this.routedItemError = true;
          this.snackbarError(this.$t('this-item-doesnt-have-a-location'));
        }
      }
      catch (error) {
        this.routedItemError = true;
        this.snackbarError(error);
      }
    },
    async fetchItems() {
      if (this.zoom >= this.minZoomToShowElements) {
        try {
          const params = this.params;
          params['bounds'] = [this.searchBounds[0].toString(), this.searchBounds[1].toString()];

          const items = (await axios.get("/api/v1/actives/", {params: params})).data;

          if (items.length > 0) {
            this.items = items.filter(item =>
                item['location'] !== null
            ).map(item => {
              return {
                ...item,
                icon: itemTypeIcons[item['type']] || greyIcon,
                location: new GeolocationCoords(item.location)
              };
            });
          } else {
            this.items = [];
          }
        } catch (error) {
          console.log(error);
        }
      }
    },
    async fetchExtraLayersMakers() {
      if (this.zoom >= this.minZoomToShowElements) {
        const elements = await Promise.all([
          this.getFallingFruitElements(),
          this.getOverPassElements('public_bookcase'),
          this.getOverPassElements('defibrillator'),
          this.getOverPassElements('give_box'),
          this.getOverPassElements('food_bank'),
          this.getOverPassElements('food_sharing'),
          this.getOverPassElements('soup_kitchen'),
          this.getOverPassElements('drinking_water'),
          this.getOverPassElements('free_shop'),
        ]);

        const tmpExtraCategories = {...this.extraCategories};

        for (const [key, extraCategory] of Object.entries(tmpExtraCategories)) {
          if (key === 'FLF') {
            tmpExtraCategories['FLF']['markers'] = elements[0].filter(element =>
              element['id'] != null && element['lat'] != null && element['lng'] != null
            ).map(element => {
              return {
                id: element['id'],
                type: 'ffruit',
                name: element['type_names'][0],
                description: element['description'],
                location: new GeolocationCoords(element['lng'], element['lat'])
              }
            });
          } else {
            const opKey = Object.keys(this.extraLayersTagsOverpass).indexOf(extraCategory.tagValue);
            if (opKey !== -1) {
              tmpExtraCategories[key]['markers'] = elements[opKey + 1].filter(element =>
                element['id'] != null && element['lat'] != null && element['lon'] != null
              ).map(element => {
                return {
                  id: element['id'],
                  type: extraCategory.tagValue,
                  name: element['tags']['name'],
                  location: new GeolocationCoords(element['lon'], element['lat'])
                }
              });
            }
          }
        }

        this.extraCategories = tmpExtraCategories;
      }
    },
    getMarkerURL(category, markerId) {
      if (category === 'FLF') {
        return "http://fallingfruit.org/locations/" + markerId + "&locale=" + this.$i18n.locale;
      } else {
        return "https://openstreetmap.org/node/" + markerId;
      }
    },
    async getFallingFruitElements() {
      try {
        const ffbaseURL = 'https://fallingfruit.org/api/0.3/locations?api_key=EEQRBBUB&locale=' + this.$i18n.locale + '&muni=false';
        const ffcoords = '&bounds=' + this.bounds.getSouthWest().lat + ',' + this.bounds.getSouthWest().lng + '|' + this.bounds.getNorthEast().lat + ',' + this.bounds.getNorthEast().lng;
        const ffURL = ffbaseURL + ffcoords;
        return (await axios.get(ffURL, {
          transformRequest: (data, headers) => {
            delete headers.common['Authorization'];
            return data;
          }
        })).data;
      }
      catch (error) {
        console.log(error);
        return [];
      }
    },
    async getOverPassElements(tagValue) {
      try {
        const bounds = `${this.bounds.getSouth()},${this.bounds.getWest()},${this.bounds.getNorth()},${this.bounds.getEast()}`;
        const nodeQuery = `node["${this.extraLayersTagsOverpass[tagValue]}"="${tagValue}"](${bounds});`;
        const data = `[out:json][timeout:15];(${nodeQuery});out body geom;`;

        // http://overpass-api.de/api
        // https://overpass.kumi.systems/api
        const baseURL = "https://maps.mail.ru/osm/tools/overpass/api";

        return (await axios.get("/interpreter", {params: {data}, baseURL})).data['elements'];
      }
      catch (error) {
        console.log(error);
        return [];
      }
    },
    async boundsUpdated() {
      clearTimeout(this.timeouts['boundsUpdated']);
      this.timeouts['boundsUpdated'] = setTimeout(async () => {
        this.mapLoading = true;

        const NWCoords = [this.bounds.getNorthWest().lng, this.bounds.getNorthWest().lat];
        const SECoords = [this.bounds.getSouthEast().lng, this.bounds.getSouthEast().lat];
        if (this.searchBounds === null) {
          this.searchBounds = [new GeolocationCoords(NWCoords), new GeolocationCoords(SECoords)];
        } else {
          this.searchBounds[0].update(NWCoords);
          this.searchBounds[1].update(SECoords);
        }

        await this.fetchItems();

        if (!this.initialItemsLoadDone) {
          if (this.itemId !== null && !this.routedItemError) {
            this.$nextTick(() => {
              this.$refs[`marker-item-${this.itemId}`][0].mapObject.openPopup();
            });
          }

          this.initialItemsLoadDone = true;
        }

        await this.fetchExtraLayersMakers();

        this.mapLoading = false;
      }, 600);
    },
    async fetchMathElements() {
      this.mapLoading = true;
      await this.fetchItems();
      await this.fetchExtraLayersMakers();
      this.mapLoading = false;
    },
    windowSizeChanged() {
      if (this.flapOpened) {
        if (this.windowWidth < 700) {
          const flap = this.$el.querySelector("#flap");
          flap.style.width = "calc(100% - 2 * 0.5rem)";
          flap.style.left = "0.5rem";
        } else {
          if (this.flapSelected === 'settings') {
            flap.style.width = "550px";
          } else if (this.flapSelected === 'filters') {
            flap.style.width = "450px";
          }
          flap.style.left = "calc(100% - " + flap.style.width + " - 0.5rem)";
        }
      }
    }
  }
}
</script>

<style>
@media screen and (max-width: 1023px) {
  #wrapper > .section {
    padding: 1.5rem !important;
  }
}
</style>

<style lang="scss" scoped>

#selected-categories {
  .selected-category {
    padding: 0;
    margin: 0 0 5px 0;
    font-size: 0.75rem;
    background-color: white;
    border-radius: 5px;

    .column.name {
      padding: 10px;
      white-space: nowrap;
      text-overflow: ellipsis;
      overflow: hidden;
    }

    .column.close {
      flex: 0 0 40px;
      padding: 10px;
      text-align: center;
      cursor: pointer;

      i {
        vertical-align: middle;
      }
    }

    &:last-child {
      margin-bottom: 0.75rem !important;
    }
  }
}

#leaflet-map {
  height: calc(100vh - 52px - 2 * 3rem);
  z-index: 1;
}

.fa-external-link-alt {
  margin-right: 0.25rem;
}

.control-zoom-info {
  margin-left: -10px;
  margin-bottom: -10px;
}

#map-surrounding {
  position: relative;
  overflow: hidden;
}

#flap {
  position: absolute;
  top: 0.5rem;
  bottom: 0.5rem;
  left: 100%;
  z-index: 1;
  transition: left 0.25s;

  .inner {
    padding: 1.25rem;
    background-color: #fff;
    overflow: auto;
    border-radius: 5px;
    max-height: 100%;

    .title {
      width: 100%;
      line-height: 40px;
    }

    .close {
      flex: 0 0 auto;
    }
  }
}

@media screen and (max-width: 1024px) {
  #leaflet-map {
    height: calc(100vh - 52px - 2 * 1.5rem);
  }
}

@media screen and (max-width: 700px) {
  #flap .inner .settings .content .columns {
    display: block;

    & > .column {
      width: 100%;
      padding: 0 0 0.5rem 0 !important;
    }
  }
}
</style>
