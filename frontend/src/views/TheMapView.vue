<template>
  <div id="page-map">
    <items-filters
        @update:selectedType="selectedType = $event"
        @update:selectedCategory="selectedCategory = $event"
        @update:searchString="searchString = $event"
    />

    <l-map :bounds.sync="bounds" :center.sync="center" :zoom.sync="zoom" style="height: 800px"
           @update:bounds="fetchMarkers">
      <l-tile-layer :attribution="attribution" :options="tileLayerOptions" :url="url"></l-tile-layer>
      <l-control class="control-geolocation">
        <b-button type="is-primary" @click="setGeolocalizedPosition">
          <i class="fas fa-street-view"></i>
        </b-button>
      </l-control>
      <l-control position="bottomleft">
        <div class="control-loading">
          <i v-show="mapLoading" class="fas fa-spinner fa-2x fa-pulse"></i>
        </div>
        <div v-show="zoom < minZoomForExtraLayers" class="control-zoom-info leaflet-control-attribution">
          {{ $t('too-small-zoom') }}
        </div>
      </l-control>

      <l-marker v-if="userPosition" :icon="userPositionIcon" :lat-lng="userPosition" />

      <l-layer-group ref="layer">
        <v-marker-cluster :options="markerClusterGroupOptions">
          <l-marker
              v-for="item in items"
              :key="item.id"
              :ref="`marker-item-${item.id}`"
              :icon="item.icon"
              :lat-lng="item.latLng"
              @ready="openRoutedItemPopup(item.id)"
          >
            <l-popup :options="{className:'item-popup', maxWidth: '500'}">
              <item-map-popup :item="item" />
            </l-popup>
          </l-marker>
        </v-marker-cluster>
      </l-layer-group>
      <l-feature-group v-if="zoom >= minZoomForExtraLayers" ref="markersFeatureGroup">
        <l-layer-group>
          <v-marker-cluster :options="extraLayersMarkerClusterGroupOptions">
            <template v-for="extraLayer in extraLayers">
              <l-marker
                  v-for="marker in extraLayer.markers"
                  :key="marker.id"
                  :icon="extraLayersIcons[extraLayer.id]"
                  :lat-lng="marker.latLng"
                  :visible="extraLayer.visible"
              >
                <l-popup>
                  <div v-if="marker.name"><strong>{{ marker.name }}</strong></div>
                  <div class="is-grey">{{ $t(extraLayer.slugMarker) }}</div>
                  <div v-if="marker.description">{{ marker.description }}</div>
                  <div class="is-grey is-size-7 has-text-right is-italic">
                    <a :href="getExtraMarkerURL(marker)" target="_blank">
                        <span>
                          <i class="fas fa-external-link-alt"></i>
                        </span>
                      <!--<span>{{$t('from-osm')}}</span>//-->
                      <span>{{ $t(getExtraMarkerSourceTransSlug(marker)) }}</span>
                    </a>
                  </div>
                </l-popup>
              </l-marker>
            </template>
          </v-marker-cluster>
        </l-layer-group>
      </l-feature-group>
    </l-map>
    <div class="extra-layers-selector block">
      <b-checkbox
          v-for="extraLayer in extraLayers"
          :key="`${extraLayer.id}-visibility`"
          v-model="extraLayer.visible"
          :disabled="zoom < minZoomForExtraLayers"
          :type="extraLayer.color"
      >
        {{ $t(extraLayer.id) }}
      </b-checkbox>
    </div>

  </div>
</template>

<script>
import * as L from 'leaflet'; // do not remove for markercluster
import "leaflet.markercluster";
import "leaflet-easybutton";
import axios from "axios"
import ItemsFilters from "@/components/ItemsFilters.vue";

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

import {latLng} from "leaflet";
import {LMap, LTileLayer, LControl, LMarker, LPopup, LFeatureGroup, LLayerGroup} from "vue2-leaflet";
import Vue2LeafletMarkercluster from "vue2-leaflet-markercluster";
import ItemMapPopup from "@/components/ItemMapPopup.vue";
import ErrorHandler from "@/mixins/ErrorHandler";

const itemTypeIcons = {
  'DN': greenIcon,
  'LN': yellowIcon,
  'RQ': redIcon,
  'EV': eventIcon
}

const GEOLOCATION_TIMEOUT = 10000;

export default {
  name: 'TheMapView',
  mixins: [ErrorHandler],
  components: {
    ItemMapPopup,
    ItemsFilters,
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
      center: latLng(0, 0),
      bounds: null,
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
      minZoomForExtraLayers: 12,
      extraLayersMarkerClusterGroupOptions: {
        disableClusteringAtZoom: 15,
        chunkedLoading: true,
        maxClusterRadius: 30
      },
      extraLayers: [
        {
          id: 'bookcases',
          slugMarker: 'bookcase',
          markers: [],
          visible: true,
          tagKey: 'amenity',
          tagValue: 'public_bookcase',
          color: 'is-bookcase'
        },
        {
          id: 'defibrillators',
          slugMarker: 'defibrillator',
          markers: [],
          visible: false,
          tagKey: 'emergency',
          tagValue: 'defibrillator',
          color: 'is-defibrillator'
        },
        {
          id: 'give-boxes',
          slugMarker: 'give-box',
          markers: [],
          visible: true,
          tagKey: 'amenity',
          tagValue: 'give_box',
          color: 'is-dark'
        },
        {
          id: 'food-banks',
          slugMarker: 'food-bank',
          markers: [],
          visible: true,
          tagKey: 'social_facility',
          tagValue: 'food_bank',
          color: 'is-dark'
        },
	      {
          id: 'food-sharings',
          slugMarker: 'food-sharing',
          markers: [],
          visible: true,
          tagKey: 'amenity',
          tagValue: 'food_sharing',
          color: 'is-dark'
        },
        {
          id: 'soup-kitchens',
          slugMarker: 'soup-kitchen',
          markers: [],
          visible: true,
          tagKey: 'social_facility',
          tagValue: 'soup_kitchen',
          color: 'is-dark'
        },
        {
          id: 'drinking-water-spots',
          slugMarker: 'drinking-water-spot',
          markers: [],
          visible: true,
          tagKey: 'amenity',
          tagValue: 'drinking_water',
          color: 'is-drinking-water'
        },
        {
          id: 'free-shops',
          slugMarker: 'free-shop',
          markers: [],
          visible: true,
          tagKey: 'amenity',
          tagValue: 'free_shop',
          color: 'is-warning'
        },
        {
          id: 'falling-fruits',
          slugMarker: 'falling-fruit',
          markers: [],
          visible: true,
          tagKey: 'ff',
          tagValue: 'ffruit',
          color: 'is-green'
        }
      ],
      extraLayersIcons: {
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
      userPosition: null,
      userPositionIcon: blueIcon,
      userPositionWatcherId: null,
      searchString: null,
      selectedType: null,
      selectedCategory: null,
      items: [],

      routedItemError: false,
    }
  },
  async mounted() {
    document.title = `Shareish | ${this.$t('map')}`;
    if (this.itemId) {
      await this.setRoutedItem();
    } else {
      this.setGeolocalizedPosition();
    }
    await Promise.all([
      this.getItemsLocation(),
      this.fetchExtraLayersMakers()
    ]);

    // Start watching user position
    // TODO: investigate why it's not working
    // this.userPositionWatcherId = navigator.geolocation.watchPosition(position => {
    //   const coords = position.coords;
    //   this.userPosition = latLng(coords.latitude, coords.longitude);
    // }, () => {}, {timeout: GEOLOCATION_TIMEOUT});
  },
  beforeDestroy() {
    // navigator.geolocation.clearWatch(this.userPositionWatcherId);
  },
  computed: {
    filterParams() {
      return {
        type: this.selectedType,
        category: this.selectedCategory,
        search: this.searchString
      };
    },
    itemId() {
      return Number(this.$route.query.id);
    }
  },
  watch: {
    async filterParams() {
      this.mapLoading = true;
      await this.getItemsLocation();
      this.mapLoading = false;
    },
  },
  methods: {
    async setRoutedItem() {
      try {
        if (this.itemId === null) {
          this.setGeolocalizedPosition();
          this.routedItemError = true;
          console.log("Routed id is null");
        } else {
          const item = (await axios.get(`/api/v1/items/${this.itemId}/`)).data;
          await axios.get(`/api/v1/items/${this.itemId}/increase_hitcount`);
          if (item['location'] === null) {
            this.setGeolocalizedPosition();
            this.routedItemError = true;
            console.log("Routed id location is null");
          } else {
            const latLong = item['location'].slice(17, -1).split(' ');
            this.center = latLng(...latLong);
          }
        }
      }
      catch (error) {
        this.setGeolocalizedPosition();
        this.routedItemError = true;
        console.log(error);
      }
    },
    openRoutedItemPopup(id) {
      if (this.itemId && this.itemId === id && !this.routedItemError) {
        this.$nextTick(() => {
          this.$refs[`marker-item-${this.itemId}`][0].mapObject.openPopup();
          //TODO: popup does not open when clustered. Probably need to to programmatically split the cluster.
        });
      }
    },
    setGeolocalizedPosition() {
      navigator.geolocation.getCurrentPosition(position => {
        const coords = position.coords;
        this.center = latLng(coords.latitude, coords.longitude);
        this.userPosition = this.center;
      }, (error) => {
        this.zoom = 2;
      }, {
        timeout: GEOLOCATION_TIMEOUT
      });
    },
    async getItemsLocation() {
      try {
        let items = (await axios.get("/api/v1/items/", {params: this.filterParams})).data;

        this.items = items.filter(item =>
            // should not happen, but happens :)
            item['location'] !== null
        ).map(item => {
          let latLong = item['location'].slice(17, -1).split(' ');
          return {
            ...item,
            icon: itemTypeIcons[item['type']] || greyIcon,
            latitude: latLong[0],
            longitude: latLong[1],
            latLng: latLng(...latLong)
          };
        });
      }
      catch (error) {
        console.log(error);
      }
    },
    async fetchExtraLayersMakers() {
      if (this.bounds === null || this.zoom < this.minZoomForExtraLayers) {
        return;
      }

      this.extraLayers = await Promise.all(
        this.extraLayers.map(async extraLayer => {
          try {
            if (extraLayer.tagKey === 'ff') {
              const elements = await this.getFallingFruitElements();
              const markers = elements.filter(element =>
                  (element['id'] != null) && (element['lat'] != null) && (element['lng'] != null)
              ).map(element => {
                return {
                  latitude: element['lat'],
                  longitude: element['lon'] || element['lng'],
                  latLng: latLng(element['lat'], element['lng']),
                  type: 'ffruit', //element['description'], //'ffruit',
                  name: element['type_names'][0],
                  description: element['description'],
                  id: element['id']
                }
              });
              return {...extraLayer, markers};
            } else {
              const elements = await this.getOverPassElements(extraLayer.tagKey, extraLayer.tagValue);
              const markers = elements.filter(element =>
                  (element['id'] != null) && (element['lat'] != null) && (element['lon'] != null)
              ).map(element => {
                return {
                  latitude: element['lat'],
                  longitude: element['lon'] || element['lng'],
                  latLng: latLng(element['lat'], element['lon']),
                  type: element['tags'][extraLayer.tagKey],
                  name: element['tags']['name'],
                  id: element['id']
                }
              });
              return {...extraLayer, markers};
            }
          }
          catch (error) {
            console.log(error)
            return extraLayer;
          }
        })
      );
    },
    getExtraMarkerURL(marker) {
      if (marker.type === 'ffruit') {
        return "http://fallingfruit.org/locations/" + marker.id + "&locale=" + this.$i18n.locale;
      } else {
        return "https://openstreetmap.org/node/" + marker.id;
      }
    },
    getExtraMarkerSourceTransSlug(marker) {
      return (marker.type === 'ffruit') ? 'from-ff' : 'from-osm';
    },
    async getFallingFruitElements() {
      try {
          const ffbaseURL = 'https://fallingfruit.org/api/0.3/locations?api_key=EEQRBBUB&locale=' + this.$i18n.locale + '&muni=false';
	  const ffcoords = '&bounds=' + + this.bounds.getSouthWest().lat + ',' + this.bounds.getSouthWest().lng + '|' + this.bounds.getNorthEast().lat + ',' + this.bounds.getNorthEast().lng;
          const ffURL = ffbaseURL + ffcoords
        return (await axios.get(ffURL,
            {
              transformRequest: (data, headers) => {
                delete headers.common['Authorization'];
                return data;
              }
            })).data;

      }
      catch (error) {
        console.log(error);
        return []; // may happen if fallingfruit API returns an error
      }
    },
    async getOverPassElements(tagKey, tagValue) {
      // "amenity"="public_bookcase"; "amenity"="give_box"; "amenity"="food_sharing"; "amenity"="freeshop"; emergency=drinking_water; emergency=defibrillator
      // social_facility=food_bank

      const overpassQuery = `"${tagKey}"="${tagValue}"`;
      const bounds = `${this.bounds.getSouth()},${this.bounds.getWest()},${this.bounds.getNorth()},${this.bounds.getEast()}`;
      const nodeQuery = `node[${overpassQuery}](${bounds});`;
      const data = `[out:json][timeout:15];(${nodeQuery});out body geom;`;

      //const baseURL = 'http://overpass-api.de/api';
      //const baseURL = 'https://overpass.kumi.systems/api';
      const baseURL = "https://maps.mail.ru/osm/tools/overpass/api";
      try {
        return (await axios.get("/interpreter", {params: {data}, baseURL})).data['elements'];
      }
      catch (error) {
        return []; // may happen if overpass API returns an error
      }
    },
    async fetchMarkers() {
      // triggered when bounds changes
      this.mapLoading = true;
      await this.fetchExtraLayersMakers();
      this.mapLoading = false;
    }
  }
}
</script>

<style scoped>
.extra-layers-selector {
  margin-top: 0.75rem;
}

>>> .item-popup .leaflet-popup-content,
>>> .item-popup .leaflet-popup-content p {
  margin: 0;
}

.fa-external-link-alt {
  margin-right: 0.25rem;
}

.control-zoom-info {
  margin-left: -10px;
  margin-bottom: -10px;
}
</style>
