<template>
  <div id="page-map">
    <div id="map-surrounding">
      <l-map
          id="leaflet-map"
          ref="map"
          :bounds.sync="bounds"
          :center.sync="leafletCenter"
          :zoom.sync="zoom"
          @contextmenu="addMarker"
          @update:bounds="boundsUpdated"
      >
        <l-control-layers position="bottomleft"></l-control-layers>
        <l-marker ref="newmarker" :icon="addIcon" :lat-lng="newmarker">
          <l-popup ref="newpopup" :options="newPopupOptions">
            <b>{{ $t('choose_add_content_type_map') }}</b> <br/><br/>
            <template v-if="newmarker.lat">
              <router-link :to="{name: 'addItemPos', params: {lat: newmarker.lat, lng: newmarker.lng, type: ' '}}">
                {{ $t('add_item') }}
              </router-link>
              <div style="display: grid;grid-template-columns:repeat(4,1fr);">
                <span v-for="(itemtype,index) in itemTypeIcons" :key="index">
                  <router-link
                      :to="{name: 'addItemPos', params: {lat: newmarker.lat, lng: newmarker.lng, type: index}}">
                    <b-tooltip :label="$t('item_type_'+index)">
                      <img :src="itemTypeIcons[index].options.iconUrl" style="height: 30px; display: inline">
                    </b-tooltip>
                  </router-link>
                </span>
              </div>
            </template>
            <br/>
            <a :href="getMarkerURLAddOSM(newmarker)" target="_blank">
              <span><i class="fas fa-external-link-alt"></i></span>
              <span>{{ $t('add_osm') }}</span>
            </a>
            <div style="display: grid;grid-template-columns:repeat(4,1fr);">
              <span v-for="(extraCategory, index) in ecatswithoutFF()" :key="index">
                <b-tooltip :label="$tc('map_ecat_'+ extraCategory.category, 1)">
                  <a :href="getMarkerURLAddSpecificOSM(newmarker,extraCategory.category)" target="_blank">
                    <img :src="extraCategoriesIcons[extraCategories[extraCategory.category].id].options.iconUrl"
                         style="width: 24px; display: inline">
                  </a>
                </b-tooltip>
              </span>
            </div>
            <br/>
            <a :href="getMarkerURLAddFF(newmarker)" target="_blank">
              <span><i class="fas fa-external-link-alt"></i></span>
              <span>
                {{ $t('add_ffruit') }}<br/>
                <b-tooltip :label="$tc('map_ecat_FLF',1)">
                  <img :src="extraCategoriesIcons[extraCategories['FLF'].id].options.iconUrl"
                       style="width: 24px; display: inline">
                </b-tooltip>
              </span>
            </a>
            <br/>
          </l-popup>
        </l-marker>
        <v-geosearch :options="geosearchOptions"></v-geosearch>
        <l-tile-layer
            v-for="tileProvider in tileProviders"
            :key="tileProvider.name"
            :attribution="tileProvider.attribution"
            :name="tileProvider.name"
            :url="tileProvider.url"
            :visible="tileProvider.visible"
            layer-type="base"/>
        <l-control position="topright">
          <div class="is-flex is-flex-direction-column">
            <b-tooltip :label="$t('use-geolocation')" class="w-75 mt-1" position="is-left" type="is-info">
              <b-button expanded type="is-info" @click="setCenterAtGeoLocation">
                <i class="fas fa-street-view"></i>
              </b-button>
            </b-tooltip>
            <b-tooltip :label="$t('use-reflocation')" class="w-75 mt-1" position="is-left" type="is-info">
              <b-button expanded type="is-info" @click="setCenterAtRefLocation">
                <i class="fas fa-home"></i>
              </b-button>
            </b-tooltip>
            <b-tooltip :label="$t('filter-items')" class="w-75 mt-1" position="is-left" type="is-primary">
              <b-button expanded type="is-primary" @click="openFlap('filters')">
                <i class="fas fa-filter"></i>
              </b-button>
            </b-tooltip>
            <b-tooltip :label="$t('open-map-settings')" class="w-75 mt-1" position="is-left" type="is-primary">
              <b-button expanded type="is-primary" @click="openFlap('settings')">
                <i class="fas fa-cog"></i>
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

        <l-marker v-if="geoLocation" :icon="geoLocationIcon" :lat-lng="geoLocation.leafletLatLng"/>
        <l-marker v-if="refLocation" :icon="refLocationIcon" :lat-lng="refLocation.leafletLatLng"/>

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
                <item-map-popup :item="item"/>
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
                    <figure class="image">
                      <img v-if="marker.image" :alt="marker.image" :src="marker.image">
                    </figure>
                    <div class="is-grey">{{ $tc('map_ecat_' + extraCategory.category, 1) }}</div>
                    <div v-if="marker.description">{{ marker.description }}</div>
                    <div class="is-grey is-size-7 has-text-right is-italic">
                      <a :href="getMarkerURLView(extraCategory.category, marker.id)" target="_blank">
                        <span><i class="fas fa-external-link-alt"></i></span>
                        <span>{{ $t(extraCategory.category === 'FLF' ? 'view-from-ff' : 'view-from-osm') }}</span>
                      </a>
                      <span> {{ $t('or') }} </span>
                      <a :href="getMarkerURLEdit(extraCategory.category, marker)" target="_blank">
                        <span><i class="fas fa-external-link-alt"></i></span>
                        <span>{{ $t('edit_minor') }}</span>
                      </a>
                      <span> {{ $t(extraCategory.category === 'FLF' ? 'from-ff' : 'from-osm') }}</span>
                      <br/>
                    </div>
                  </l-popup>
                </l-marker>
              </template>
            </v-marker-cluster>
          </l-layer-group>
        </l-feature-group>
      </l-map>
      <div id="flaps">
        <div class="flap settings">
          <div class="inner">
            <header class="is-flex">
              <h2 class="title">{{ $t('settings') }}</h2>
              <b-button
                  class="close"
                  outlined
                  type="is-dark"
                  @click="closeFlap"
              >
                <i class="fas fa-times"></i>
              </b-button>
            </header>
            <div class="content">
              <h3 class="title is-size-4 mb-1">{{ $t('external-public-resources') }}</h3>
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
                <div v-for="(extraCategory, index) in user.map_ecats" :key="index"
                     :class="{'pr-2': index % 2 === 0, 'pl-2': index % 2 !== 0}"
                     class="column is-half p-0 pb-2">
                  <b-field>
                    <b-checkbox v-model="ecatsCheckboxes" :native-value="extraCategory.category" type="is-primary">
                      <img :src="extraCategoriesIcons[extraCategories[extraCategory.category].id].options.iconUrl"
                           class="mr-1" style="width: 24px; vertical-align: middle;">
                      {{ $tc('map_ecat_' + extraCategory.category, 0) }}
                    </b-checkbox>
                  </b-field>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="flap filters">
          <div class="inner">
            <header class="is-flex">
              <h2 class="title">{{ $tc('filter', 0) }}</h2>
              <b-button
                  class="close"
                  outlined
                  type="is-dark"
                  @click="closeFlap"
              >
                <i class="fas fa-times"></i>
              </b-button>
            </header>
            <div class="content">
              <items-filters
                  :boxed="false"
                  :limited-vertical-space="false"
                  :locationFilter="false"
                  rewrite-url-page-name="map"
                  @fieldsUpdated="itemFiltersUpdated"
              />
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
import axios from "axios";
//import "leaflet-geosearch";

import {
  greenIcon,
  yellowIcon,
  redIcon,
  greyIcon,
  eventIcon,
  publicBookcaseIcon,
  aedIcon,
  giveBoxIcon,
  drinkingWaterIcon,
  freeShopIcon,
  foodSharingIcon,
  foodBankIcon,
  soupKitchenIcon,
  fallingfruitIcon,
  blueIcon,
  addIcon,
  homeIcon
} from "@/map-icons";

import {LMap, LTileLayer, LControlLayers, LControl, LMarker, LPopup, LFeatureGroup, LLayerGroup} from "vue2-leaflet";
import Vue2LeafletMarkercluster from "vue2-leaflet-markercluster";
import ItemMapPopup from "@/components/ItemMapPopup.vue";
import ErrorHandler from "@/mixins/ErrorHandler";
import {GeolocationCoords, lcall, ucfirst} from "@/functions";
import {LatLng} from "leaflet/dist/leaflet-src.esm";
import WindowSize from "@/mixins/WindowSize";
import ItemsFilters from "@/components/ItemsFilters.vue";
import {OpenStreetMapProvider} from 'leaflet-geosearch';
import VGeoSearch from "vue2-leaflet-geosearch";

export default {
  name: 'TheMapView',
  mixins: [ErrorHandler, WindowSize],
  components: {
    ItemsFilters,
    ItemMapPopup,
    LMap,
    LTileLayer,
    LControlLayers,
    LControl,
    'v-geosearch': VGeoSearch,
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
      maxZoom: 19,
      preLeafletCenter: new LatLng(50.6450944, 5.5736112),
      leafletCenter: new LatLng(50.6450944, 5.5736112),
      flapOpened: false,
      flapSelected: null,
      ecatsCheckboxes: [],
      waitingFormResponse: false,

      newmarker: [0, 0], //window middle?
      newPopupOptions: {autoPan: false, maxWidth: '200'},

      bounds: null,
      searchBounds: null,
      geoLocation: null,
      refLocation: null,
      filteredQueryValues: {},
      builtURLParams: {},

      initialItemsLoadDone: false,
      user: {},
      itemId: null,

      tileProviders: [
        {
          name: this.$t('tilemap_osm_humanitarian'),
          visible: true,
          url: "https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png",
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, tiles &copy <a href="https://www.hotosm.org/" target="_blank">Humanitarian OSM Team</a>, hosted by <a href="https://openstreetmap.fr/" target="_blank">OSM France</a>',
        },
        {
          name: this.$t('tilemap_osm_standard'),
          visible: false,
          attribution: '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
          url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        },
        {
          name: this.$t('tilemap_cyclosm'),
          visible: false,
          url: 'https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png',
          attribution: '&copy; <a href="https://github.com/cyclosm/cyclosm-cartocss-style/releases">CyclOSM</a> & <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        },
        {
          name: this.$t('tilemap_transport'),
          visible: false,
          url: 'https://tile.thunderforest.com/transport/{z}/{x}/{y}.png?apikey=a940a24136c24077857d0f9e0faa5a9f',
          attribution: '&copy;  <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, tiles &copy <a href="https://www.thunderforest.com/maps/transport/">Thunderforest</a>',
        },
        {
          name: this.$t('tilemap_transport_dark'),
          visible: false,
          url: 'https://tile.thunderforest.com/transport-dark/{z}/{x}/{y}.png?apikey=a940a24136c24077857d0f9e0faa5a9f',
          attribution: '&copy;  <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, tiles &copy <a href="https://www.thunderforest.com/maps/transport/">Thunderforest</a>',
        },

        {
          name: this.$t('tilemap_neighbourhood'),
          visible: false,
          url: 'https://tile.thunderforest.com/neighbourhood/{z}/{x}/{y}.png?apikey=a940a24136c24077857d0f9e0faa5a9f',
          attribution: '&copy;  <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, tiles &copy <a href="https://www.thunderforest.com/maps/transport/">Thunderforest</a>',
        },
        {
          name: this.$t('tilemap_outdoors'),
          visible: false,
          url: 'https://tile.thunderforest.com/outdoors/{z}/{x}/{y}.png?apikey=a940a24136c24077857d0f9e0faa5a9f',
          attribution: '&copy;  <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, tiles &copy <a href="https://www.thunderforest.com/maps/transport/">Thunderforest</a>',
        },

      ],

      geosearchOptions: {
        provider: new OpenStreetMapProvider(),
        searchLabel: this.$t('search_address'),
      },

      markerClusterGroupOptions: {
        chunkedLoading: true,
        maxClusterRadius: 15,
        disableClusteringAtZoom: 15,
      },
      minZoomToShowElements: 11,
      extraLayersMarkerClusterGroupOptions: {
        disableClusteringAtZoom: 16,
        chunkedLoading: true,
        maxClusterRadius: 40
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
          tagValue: 'freeshop'
        },
        'GVB': {
          id: 'give-boxes',
          markers: [],
          tagValue: 'give_box'
        },
        'SPK': {
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
        'freeshop': 'amenity'
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
      itemTypeIcons: {
        'DN': greenIcon,
        'LN': yellowIcon,
        'RQ': redIcon,
        'EV': eventIcon
      },
      geoLocationIcon: blueIcon,
      refLocationIcon: homeIcon,
      addIcon: addIcon,
      routedItemLocation: null,
      items: [],

      routedItemError: false,
      timeouts: {}
    }
  },
  async created() {
    document.title = `Shareish | ${this.$t('map')}`;

    if (this.isPosUsed) {
      this.routedItemLocation = new GeolocationCoords(this.PosLng, this.PosLat);
    } else if (this.$route.query.id)
      this.itemId = Number(this.$route.query.id);

    await this.updateGeoLocation();
    await this.fetchUser();

    for (const i in this.user.map_ecats) {
      if (this.user.map_ecats[i].selected === true)
        this.ecatsCheckboxes.push(this.user.map_ecats[i].category)
    }

    if (this.routedItemLocation) {
      this.preLeafletCenter = this.routedItemLocation.leafletLatLng;
    } else if (this.geoLocation instanceof GeolocationCoords)
      this.preLeafletCenter = this.geoLocation.leafletLatLng;
    else if (this.refLocation instanceof GeolocationCoords)
      this.preLeafletCenter = this.refLocation.leafletLatLng;

    if (this.itemId !== null)
      await this.fetchRoutedItem();

    this.leafletCenter = this.preLeafletCenter;

    this.mapLoading = false;

  },
  computed: {
    userId() {
      return Number(this.$store.state.user.id);
    },
    PosLat() {
      console.log(this.$route.params.lat)
      return Number(this.$route.params.lat);
    },
    PosLng() {
      console.log(this.$route.params.lng)
      return Number(this.$route.params.lng);
    },
    isPosUsed() {
      return (this.PosLat > 0 && this.PosLng > 0);
    },
  },
  watch: {
    ecatsCheckboxes() {
      this.ecatsCheckboxesUpdated();
    }
  },
  methods: {
    ucfirst,
    lcall,
    async ecatsCheckboxesUpdated() {
      for (const i in this.user.map_ecats) {
        const checkboxSelected = this.ecatsCheckboxes.includes(this.user.map_ecats[i].category);
        if (this.user.map_ecats[i].selected !== checkboxSelected) {
          try {
            await axios.patch(`/api/v1/map_ecats/${this.user.map_ecats[i].id}/`, {selected: checkboxSelected});
            this.user.map_ecats[i].selected = checkboxSelected;
          } catch (error) {
            this.snackbarError(error);
          }
        }
      }
    },
    ecatswithoutFF() {
      var catswithoutFF = [];
      for (const i in this.user.map_ecats) {
        if (this.user.map_ecats[i].category != 'FLF')
          catswithoutFF.push(this.user.map_ecats[i])
      }
      return catswithoutFF;
    },
    rewriteURL() {
      clearTimeout(this.timeouts['rewriteURL']);
      this.timeouts['rewriteURL'] = setTimeout(async () => {
        try {
          await this.$router.push({name: 'map', query: this.builtURLParams});
        } catch (error) {
          console.log("Redirected on same URL.");
        }
      }, 100);
    },
    itemFiltersUpdated(filteredQueryValues, builtURLParams) {
      this.builtURLParams = {...builtURLParams};
      this.rewriteURL();

      this.$store.commit('setItemsFilters', {
        builtURLParams: this.builtURLParams,
        keysToKeep: ['dr', 'lt', 'ordering', 'us']
      });

      clearTimeout(this.timeouts['itemFiltersUpdated']);
      this.timeouts['itemFiltersUpdated'] = setTimeout(() => {
        this.filteredQueryValues = filteredQueryValues;

        this.fetchItems(false);
      }, 600);
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
    async fetchUser() {
      try {
        const params = {
          columns: ['ref_location', 'map_ecats']
        }
        this.user = (await axios.get('/api/v1/users/me/', {params: params})).data;

        if (this.user.ref_location !== null)
          this.refLocation = new GeolocationCoords(this.user.ref_location);
      } catch (error) {
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
        } catch {
        }
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

      const flap = this.$el.querySelector(`#flaps .${this.flapSelected}`);
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
        const flap = this.$el.querySelector(`#flaps .${this.flapSelected}`);
        flap.style.left = "100%";
        this.flapSelected = null;
        this.flapOpened = false;
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
      } catch (error) {
        this.routedItemError = true;
        this.snackbarError(error);
      }
    },
    async fetchItems() {
      if (this.zoom >= this.minZoomToShowElements && this.searchBounds != null) {
        try {
          const params = {...this.filteredQueryValues};
          params['bounds'] = [this.searchBounds[0].toString(), this.searchBounds[1].toString()];

          const items = (await axios.get("/api/v1/actives/", {params: params})).data;

          if (items.length > 0) {
            this.items = items.filter(item =>
                item['location'] !== null
            ).map(item => {
              return {
                ...item,
                icon: this.itemTypeIcons[item['type']] || greyIcon,
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
          this.getOverPassElements('freeshop'),
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
                  location: new GeolocationCoords(element['lon'], element['lat']),
                  image: element['tags']['image:0'] != null ? element['tags']['image:0'] : element['tags']['image'],
                }
              });
            }
          }
        }

        this.extraCategories = tmpExtraCategories;
      }
    },
    addMarker(e) {
      this.newmarker = e.latlng;

      //this.$refs.map.mapObject.on('popupopen', function(e) {
      //    var px = this.$refs.map.mapObject.project(e.target._popup._latlng); // find the pixel location on the map where the popup anchor is
      //    px.y -= e.target._popup._container.clientHeight/2; // find the height of the popup container, divide by 2, subtract from the Y axis of marker location
      //    this.$refs.map.mapObject.panTo(map.unproject(px),{animate: true}); // pan to new center
      //});


      this.$refs.newmarker.mapObject.setOpacity(1);
      this.$refs.newmarker.mapObject.getPopup().on('remove', function () {
        this._source.setOpacity(0);
      });
      this.$refs.newmarker.mapObject.openPopup();
      //this.$refs.map.mapObject.setView(this.newmarker);

    },
    getMarkerURLView(category, markerId) {
      if (category === 'FLF') {
        return "http://fallingfruit.org/locations/" + markerId + "&locale=" + this.$i18n.locale;
      } else {
        return "https://openstreetmap.org/node/" + markerId;
      }
    },
    getMarkerURLEdit(category, marker) {
      if (category === 'FLF') {
        return "http://fallingfruit.org/locations/" + marker.id + "/edit?c=forager%2Cfreegan&locale=" + this.$i18n.locale;
      } else if (category === 'BKC') {
        return "https://mapcomplete.org/bookcases.html?z=19&lat=" + marker.location.leafletLatLng.lat + "&lon=" + marker.location.leafletLatLng.lng + "#node/" + marker.id
      } else if (category === "DEF") {
        return "https://mapcomplete.org/aed?z=19&lat=" + marker.location.leafletLatLng.lat + "&lon=" + marker.location.leafletLatLng.lng + "#node/" + marker.id
      } else if (category === "DWS") {
        return "https://mapcomplete.org/drinking_water.html?z=19&lat=" + marker.location.leafletLatLng.lat + "&lon=" + marker.location.leafletLatLng.lng + "#node/" + marker.id
      } else {
        return "https://openstreetmap.org/edit?node=" + marker.id + "#map=19/" + marker.location.leafletLatLng.lat + "/" + marker.location.leafletLatLng.lng;
      }
    },
    getMarkerURLAddOSM(marker) {
      return "https://openstreetmap.org/edit#map=20/" + marker.lat + "/" + marker.lng;
    },
    getMarkerURLAddSpecificOSM(marker, category) {
      if (category === "BKC") {
        return "https://mapcomplete.org/bookcases.html?z=19&lat=" + marker.lat + "&lon=" + marker.lng;
      } else if (category === "DEF") {
        return "https://mapcomplete.org/aed.html?z=19&lat=" + marker.lat + "&lon=" + marker.lng;
      } else if (category === "DWS") {
        return "https://mapcomplete.org/drinking_water.html?z=19&lat=" + marker.lat + "&lon=" + marker.lng;
      } else return "https://openstreetmap.org/edit#map=20/" + marker.lat + "/" + marker.lng;
    },
    getMarkerURLAddFF(marker) {
      return "http://fallingfruit.org/locations/new?lat=" + marker.lat + "&lng=" + marker.lng + "&locale=" + this.$i18n.locale;
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
      } catch (error) {
        console.log(error);
        return [];
      }
    },
    async getOverPassElements(tagValue) {
      try {
        const bounds = `${this.bounds.getSouth()},${this.bounds.getWest()},${this.bounds.getNorth()},${this.bounds.getEast()}`;
        const nodeQuery = `node["${this.extraLayersTagsOverpass[tagValue]}"="${tagValue}"](${bounds});`;
        const data = `[out:json][timeout:15];(${nodeQuery});out body geom;`;

        //const baseURL = "http://overpass-api.de/api";
        const baseURL = "https://overpass.kumi.systems/api";
        //const baseURL = "https://maps.mail.ru/osm/tools/overpass/api";

        return (await axios.get("/interpreter", {params: {data}, baseURL})).data['elements'];
      } catch (error) {
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

        await this.fetchItems(this.filteredQueryValues);

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
      await this.fetchItems(this.filteredQueryValues);
      await this.fetchExtraLayersMakers();
      this.mapLoading = false;
    },
    windowSizeChanged() {
      if (this.flapOpened) {
        const flap = this.$el.querySelector(`#flaps .${this.flapSelected}`);
        if (this.windowWidth < 700) {
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

#flaps .flap {
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
  #flaps .flap .inner .settings .content .columns {
    display: block;

    & > .column {
      width: 100%;
      padding: 0 0 0.5rem 0 !important;
    }
  }
}
</style>
