<template>
  <div id="page-map">
    <items-filters
        @update:selectedType="selectedType = $event"
        @update:selectedCategory="selectedCategory = $event"
        @update:searchString="searchString = $event"
    />

    <l-map :bounds.sync="bounds" :center.sync="leafletCenter" :zoom.sync="zoom" style="height: 800px"
           @update:bounds="boundsUpdated">
      <l-tile-layer :attribution="attribution" :options="tileLayerOptions" :url="url"></l-tile-layer>
      <l-control class="control-geolocation">
        <b-button type="is-primary" @click="setCenterAtGeoLocation">
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

      <l-marker v-if="geoLocation" :icon="geoLocationIcon" :lat-lng="geoLocation.leafletLatLng" />

      <l-layer-group>
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
      <l-feature-group v-if="zoom >= minZoomForExtraLayers">
        <l-layer-group>
          <v-marker-cluster :options="extraLayersMarkerClusterGroupOptions">
            <template v-for="extraLayer in extraLayers">
              <l-marker
                  v-for="marker in extraLayer.markers"
                  :key="marker.id"
                  :icon="extraLayersIcons[extraLayer.id]"
                  :lat-lng="marker.location.leafletLatLng"
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
import {GeolocationCoords} from "@/functions";
import {LatLng} from "leaflet/dist/leaflet-src.esm";

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
      preLeafletCenter: new LatLng(50.6450944, 5.5736112),
      leafletCenter: new LatLng(50.6450944, 5.5736112),
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
      geoLocation: null,
      geoLocationIcon: blueIcon,
      routedItemLocation: null,
      searchString: null,
      selectedType: null,
      selectedCategory: null,
      items: [],

      routedItemError: false,
    }
  },
  async created() {
    document.title = `Shareish | ${this.$t('map')}`;

    await this.updateGeoLocation();
    if (this.geoLocation instanceof GeolocationCoords)
      this.preLeafletCenter = this.geoLocation.leafletLatLng;

    if (this.itemId !== null)
      await this.fetchRoutedItem();

    this.leafletCenter = this.preLeafletCenter;

    await this.fetchExtraLayersMakers();
    await this.fetchItems();

    if (this.itemId !== null && !this.routedItemError) {
      this.$nextTick(() => {
        this.$refs[`marker-item-${this.itemId}`][0].mapObject.openPopup();
      });
    }

    this.mapLoading = false;
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
      return (this.$route.query.id) ? Number(this.$route.query.id) : null;
    }
  },
  watch: {
    async filterParams() {
      this.mapLoading = true;
      await this.fetchItems();
      this.mapLoading = false;
    },
  },
  methods: {
    async updateGeoLocation() {
      // Has the user activated geolocation?
      if ('geolocation' in navigator) {
        // Get the position
        try {
          const position = await new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve, reject);
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
      if (!this.mapLoading) {
        await this.updateGeoLocation();
        if (this.geoLocation instanceof GeolocationCoords)
          this.leafletCenter = this.geoLocation.leafletLatLng;
        else
          this.snackbarError(this.$t('enable-geolocation-to-use-feature'));
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
          console.log("Routed id location is null");
        }
      }
      catch (error) {
        this.routedItemError = true;
        console.log(error);
      }
    },
    async fetchItems() {
      try {
        let items = (await axios.get("/api/v1/items", {params: this.filterParams})).data;

        this.items = items.filter(item =>
            item['location'] !== null
        ).map(item => {
          return {
            ...item,
            icon: itemTypeIcons[item['type']] || greyIcon,
            location: new GeolocationCoords(item.location)
          };
        });
      }
      catch (error) {
        console.log(error);
      }
    },
    async fetchExtraLayersMakers() {
      if (this.bounds !== null && this.zoom >= this.minZoomForExtraLayers) {
        this.extraLayers = await Promise.all(
          this.extraLayers.map(async extraLayer => {
            try {
              if (extraLayer.tagKey === 'ff') {
                const elements = await this.getFallingFruitElements();
                const markers = elements.filter(element =>
                  (element['id'] != null) && (element['lat'] != null) && (element['lng'] != null)
                ).map(element => {
                  return {
                    location: new GeolocationCoords(element['lng'], element['lat']),
                    type: 'ffruit',
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
                    location: new GeolocationCoords(element['lon'], element['lat']),
                    type: element['tags'][extraLayer.tagKey],
                    name: element['tags']['name'],
                    id: element['id']
                  }
                });
                return {...extraLayer, markers};
              }
            } catch (error) {
              console.log(error);
              return extraLayer;
            }
          })
        );
      }
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
    async boundsUpdated() {
      this.mapLoading = true;
      await this.fetchExtraLayersMakers();
      await this.fetchItems();
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
