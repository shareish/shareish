<template>
    <div class="page-dashboard">
      <items-filters
        @update:selectedType="selectedType = $event"
        @update:selectedCategory="selectedCategory = $event"
        @update:searchString="searchString = $event"
      />

      <l-map
        style="height: 800px"
        :zoom.sync="zoom"
        :center.sync="center"
        :bounds.sync="bounds"
        @update:bounds="fetchMarkers"
      >
        <l-tile-layer :url="url" :attribution="attribution" :options="tileLayerOptions"></l-tile-layer>
        <l-control class="control-geolocation">
          <button class="button" @click="setGeolocalizedPosition">
            <i class="fas fa-street-view"></i>
          </button>
        </l-control>
        <l-control position="bottomleft">
          <div class="control-loading">
            <i class="fas fa-spinner fa-2x fa-pulse" v-show="mapLoading"></i>
          </div>
          <div v-show="zoom < minZoomForExtraLayers" class="control-zoom-info leaflet-control-attribution">
            {{$t('too-small-zoom')}}
          </div>
        </l-control>

        <l-marker
          v-if="userPosition"
          :lat-lng="userPosition"
          :icon="userPositionIcon"
        />


        <l-layer-group ref="layer">
          <v-marker-cluster :options="markerClusterGroupOptions">
            <l-marker
              v-for="item in items"
              :key="item.id"
              :lat-lng="item.latLng"
              :icon="item.icon"
            >
              <l-popup :options="{className:'item-popup', maxWidth: '500'}">
                <item-map-popup :item="item" />
              </l-popup>
            </l-marker>
          </v-marker-cluster>
        </l-layer-group>
        <l-feature-group ref="markersFeatureGroup" v-if="zoom >= minZoomForExtraLayers">
          <l-layer-group>
            <v-marker-cluster :options="extraLayersMarkerClusterGroupOptions">
              <template v-for="extraLayer in extraLayers">
                <l-marker
                  v-for="marker in extraLayer.markers"
                  :key="marker.id"
                  :lat-lng="marker.latLng"
                  :icon="extraLayersIcons[extraLayer.id]"
                  :visible="extraLayer.visible"
                >
                  <l-popup>
                    <div v-if="marker.name"><strong>{{marker.name}}</strong></div>
                    <div class="is-grey">{{$t(extraLayer.slugMarker)}}</div>
                    <div class="is-grey is-size-7 has-text-right is-italic">
                      <a :href="`https://openstreetmap.org/node/${marker.id}`" target="_blank">
                        <span>
                          <i class="fas fa-external-link-alt"></i>
                        </span>
                        <span>{{$t('from-osm')}}</span>
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
          :type="extraLayer.color"
          :disabled="zoom < minZoomForExtraLayers"
        >
          {{$t(extraLayer.id)}}
        </b-checkbox>
      </div>

    </div>
</template>

<script>
import * as L from 'leaflet'; // do not remove for markercluster
import 'leaflet.markercluster';
import 'leaflet-easybutton';
import axios from 'axios'
import ItemsFilters from '@/components/ItemsFilters';

import {
  greenIcon,
  yellowIcon,
  redIcon,
  greyIcon,
  publicBookcaseIcon,
  aedIcon,
  giveBoxIcon,
  drinkingWaterIcon, freeShopIcon, blueIcon
} from '@/map-icons';

import { latLng } from "leaflet";
import {LMap, LTileLayer, LControl, LMarker, LPopup, LFeatureGroup, LLayerGroup} from 'vue2-leaflet';
import Vue2LeafletMarkercluster from 'vue2-leaflet-markercluster';
import ItemMapPopup from '@/components/ItemMapPopup';

const itemTypeIcons = {
  "DN": greenIcon,
  "LN": yellowIcon,
  "BR": redIcon
}

const GEOLOCATION_TIMEOUT = 10000;

export default {
  name: 'ItemsMap',
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
          center: latLng(0,0),
          bounds: null,
          url: 'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>',
          tileLayerOptions: {
            zoom: 14,
            maxZoom: 19
          },
          markerClusterGroupOptions: {
            // disableClusteringAtZoom: 16,
            chunkedLoading: true,
            maxClusterRadius: 20
          },
          minZoomForExtraLayers: 10,
          extraLayersMarkerClusterGroupOptions: {
            disableClusteringAtZoom: 16,
            chunkedLoading: true,
            maxClusterRadius: 50
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
              visible: true,
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
              color: 'is-danger'
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
            }
          ],
          extraLayersIcons: {
            'bookcases': publicBookcaseIcon,
            'defibrillators': aedIcon,
            'give-boxes': giveBoxIcon,
            'drinking-water-spots': drinkingWaterIcon,
            'free-shops': freeShopIcon
          },
          userPosition: null,
          userPositionIcon: blueIcon,
          userPositionWatcherId: null,
          searchString: null,
          selectedType: null,
          selectedCategory: null,
          items: [],
        }
    },
    async mounted() {
      document.title = "Shareish | Map";
      this.setGeolocalizedPosition();
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
  watch: {
      async selectedType() {
        this.mapLoading = true;
        await this.getItemsLocation();
        this.mapLoading = false;
      },
      async selectedCategory() {
        this.mapLoading = true;
        await this.getItemsLocation();
        this.mapLoading = false;
      },
      async searchString() {
        this.mapLoading = true;
        await this.getItemsLocation();
        this.mapLoading = false;
      }
    },
    methods: {
      setGeolocalizedPosition() {
        navigator.geolocation.getCurrentPosition(position => {
          const coords = position.coords;
          this.center = latLng(coords.latitude, coords.longitude);
          this.userPosition = this.center;
        }, (error) => {
          this.zoom = 2;
          console.log(error.message);
        }, {timeout: GEOLOCATION_TIMEOUT});
      },
      async getItemsLocation() {
        try {
          let items = (await axios.post('/api/v1/requestFilter/', {
            name: this.searchString,
            item_type: this.selectedType,
            category: this.selectedCategory
          })).data;

          this.items = items.filter(item =>
            // should not happen, but happens :)
            item['location'] !== null
          ).map(item => {
            let latLong = item['location'].slice(17, -1).split(' ');
            return {
              ...item,
              icon: itemTypeIcons[item['item_type']] || greyIcon,
              latitude: latLong[0],
              longitude: latLong[1],
              latLng: latLng(...latLong)
            };
          })
        }
        catch (error) {
          console.log(error);
        }
      },
      async fetchExtraLayersMakers() {
        if (this.bounds === null || this.zoom < this.minZoomForExtraLayers) {
          return;
        }

        this.extraLayers = await Promise.all(this.extraLayers.map(async extraLayer => {
          try {
            const elements = await this.getOverPassElements(extraLayer.tagKey, extraLayer.tagValue);
            const markers = elements.filter(element =>
              element['lat'] !== null && element['lon'] !== null
            ).map(element => {
              return {
                latitude: element['lat'],
                longitude: element['lon'],
                latLng: latLng(element['lat'], element['lon']),
                type: element['tags'][extraLayer.tagKey],
                name: element['tags']['name'],
                id: element['id']
              }
            });
            return {...extraLayer, markers};
          }
          catch (error) {
            console.log(error)
            return extraLayer;
          }
        }));
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
        const baseURL = 'https://maps.mail.ru/osm/tools/overpass/api';

        try {
          return (await axios.get('/interpreter', {params: {data}, baseURL})).data['elements'];
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
      },
    },
}
</script>

<style scoped>
.extra-layers-selector {
  margin-top: 0.75rem;
}

>>> .item-popup .leaflet-popup-content, >>> .item-popup .leaflet-popup-content p {
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
