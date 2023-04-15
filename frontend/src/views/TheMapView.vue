<template>
  <div id="page-map">
    <div class="columns">
      <div class="column">
        <div id="filters">
          <div class="title has-background-primary p-3 is-size-4 has-text-white">{{ $tc('filter', 0) }}</div>
          <div class="list">
            <div class="search">
              <template v-if="windowWidth >= 1024">
                <b-field :label="$t('search')">
                  <b-input
                      v-model="searchString"
                      :placeholder="$t('name') + ', ' + lcall($t('description')) + ' ' + lcall($t('or')) + ' ' + lcall($t('author'))" />
                </b-field>
              </template>
              <div v-else class="columns is-mobile">
                <div class="column pr-2">
                  <b-field :label="$t('search')">
                    <b-input
                        v-model="searchString"
                        :placeholder="$t('name') + ', ' + lcall($t('description')) + ' ' + lcall($t('or')) + ' ' + lcall($t('author'))" />
                  </b-field>
                </div>
                <div class="column pl-1" style="flex-grow: 0; padding-top: calc(24px + 0.5rem + 0.75rem);">
                  <b-button
                      type="is-primary"
                      :outlined="!isMoreFiltersOpened"
                      @click="isMoreFiltersOpened = !isMoreFiltersOpened">
                    <template v-if="!isMoreFiltersOpened">
                      <template v-if="windowWidth >= 400">
                        {{ $t('show-filters') }}<i class="fas fa-chevron-down ml-2" style="margin-top: -1px; vertical-align: middle;"></i>
                      </template>
                      <template v-else>
                        <i class="fas fa-plus"></i>
                      </template>
                    </template>
                    <template v-else>
                      <template v-if="windowWidth >= 400">
                        {{ $t('hide-filters') }}<i class="fas fa-chevron-up ml-2"></i>
                      </template>
                      <template v-else>
                        <i class="fas fa-times"></i>
                      </template>
                    </template>
                  </b-button>
                </div>
              </div>
            </div>
            <div class="other-filters mt-4" :class="{'is-opened': windowWidth >= 1024 || isMoreFiltersOpened}">
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
                  <p v-if="timeUnit === 'days'">{{ $t('only-items-created-on') }} <b>{{ formattedDay(minCreationdate) }}</b> {{ $t('or-later-will-be-showed') }}.</p>
                  <p v-else>{{ $t('only-items-created-at') }} <b>{{ formattedHour(minCreationdate) }}</b> {{ $t('on-day') }} <b>{{ formattedDay(minCreationdate) }}</b> {{ $t('or-later-will-be-showed') }}.</p>
                </template>
              </toggle-box>
            </div>
          </div>
        </div>
      </div>
      <div class="column">
        <l-map
            :bounds.sync="bounds"
            :center.sync="leafletCenter"
            :zoom.sync="zoom"
            id="leaflet-map"
            @update:bounds="boundsUpdated"
        >
          <l-tile-layer :attribution="attribution" :options="tileLayerOptions" :url="url"></l-tile-layer>
          <l-control position="topright">
            <b-tooltip :label="$t('use-geolocation')" position="is-left" type="is-primary" :delay="1000">
              <b-button type="is-primary" @click="setCenterAtGeoLocation">
                <i class="fas fa-street-view"></i>
              </b-button>
            </b-tooltip>
            <b-tooltip :label="$t('use-reflocation')" position="is-left" type="is-info" :delay="1000">
              <b-button type="is-info ml-2" @click="setCenterAtRefLocation">
                <i class="fas fa-home"></i>
              </b-button>
            </b-tooltip>
            <b-tooltip :label="$t('open-map-settings')" position="is-left" type="is-danger" :delay="1000">
              <b-button type="is-danger ml-2" @click="openSettingsModal">
                <i class="fas fa-cog"></i>
              </b-button>
            </b-tooltip>
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
import TheMapSettingsModal from "@/components/TheMapSettingsModal.vue";

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
      leafletMapHeight: "1200px",

      routedItemError: false,
      timeouts: {}
    }
  },
  async created() {
    document.title = `Shareish | ${this.$t('map')}`;

    await this.updateGeoLocation();
    await this.fetchUser();

    if (this.geoLocation instanceof GeolocationCoords)
      this.preLeafletCenter = this.geoLocation.leafletLatLng;
    else if (this.refLocation instanceof GeolocationCoords)
      this.preLeafletCenter = this.refLocation.leafletLatLng;

    if (this.itemId !== null)
      await this.fetchRoutedItem();

    this.leafletCenter = this.preLeafletCenter;

    this.mapLoading = false;
  },
  beforeMount() {
    this.leafletMapHeight = (this.windowHeight - 300) + "px";
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
    openSettingsModal() {
      this.$buefy.modal.open({
        parent: this,
        props: {
          map_ecats: this.user.map_ecats,
        },
        component: TheMapSettingsModal,
        hasModalCard: true,
        trapFocus: true
      });
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
        const FFelements = await this.getFallingFruitElements();
        if (FFelements.length > 0) {
          this.extraCategories['FLF']['markers'] = FFelements.filter(element =>
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
        }

        for (const [key, extraCategory] of Object.entries(this.extraCategories)) {
          const OPelements = await this.getOverPassElements(extraCategory.tagValue);
          if (OPelements.length > 0) {
            this.extraCategories[key]['markers'] = OPelements.filter(element =>
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
    windowHeightChanged() {
      this.leafletMapHeight = (this.windowHeight - 300) + "px";
    }
  }
}
</script>

<style lang="scss" scoped>
$filtersWidth: 400px;

#page-map > .columns > .column:first-child {
  flex: 0 0 $filtersWidth;
  max-width: $filtersWidth;
}

#filters {
  border-radius: 5px;
  box-shadow: 0 0.5em 1em -0.125em rgba(10, 10, 10, 0.1), 0 0 0 1px rgba(10, 10, 10, 0.02);
  max-width: calc(#{$filtersWidth} - 2 * 0.75rem);

  .title {
    margin-bottom: 0;
    border-radius: 5px 5px 0 0;
  }

  .list {
    padding: 0.75rem;
    border-radius: 0 0 5px 5px;
  }
}

#selected-categories {
  .selected-category {
    padding: 0;
    margin: 0 0 5px 0;
    font-size: 0.75rem;
    background-color: white;
    border-radius: 5px;

    .column.name {
      flex: 0 0 calc(400px - 0.75rem * 6 - 40px - 2px);
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

@media screen and (max-width: 1215px) and (min-width: 1024px) {
  $filtersWidth: 360px;

  #page-map > .columns > .column:first-child {
      flex: 0 0 $filtersWidth;
      max-width: $filtersWidth;
  }
}

@media screen and (max-width: 1023px) {
  $filtersWidth: 100%;

  #page-map > .columns {
    display: block;

    & > .column:first-child {
      flex: 0 0 $filtersWidth;
      max-width: $filtersWidth;
    }
  }

  #filters {
    min-width: $filtersWidth;

    .other-filters:not(.is-opened) {
      display: none;
    }
  }
}

@media screen and (max-width: 499px) {
  #filters {
    margin-bottom: 0.25rem;
  }
}

#leaflet-map {
  min-height: 800px;
  height: v-bind(leafletMapHeight);
  z-index: 1;
}

.fa-external-link-alt {
  margin-right: 0.25rem;
}

.control-zoom-info {
  margin-left: -10px;
  margin-bottom: -10px;
}
</style>
