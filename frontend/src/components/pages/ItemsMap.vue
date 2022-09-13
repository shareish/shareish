<template>
    <div class="page-dashboard">
      <items-filters />

      <l-map style="height: 800px" :zoom.sync="zoom" :center.sync="center">
        <l-tile-layer :url="url" :attribution="attribution" :options="tileLayerOptions"></l-tile-layer>
        <l-control class="control-geolocation">
          <button class="button" @click="setGeolocalizedPosition">
            <i class="fas fa-street-view"></i>
          </button>
        </l-control>
<!--        <l-marker :lat-lng="markerLatLng"></l-marker>-->
      </l-map>
<!--        <nav class="level">-->
<!--            <h1 class="level-left">-->
<!--                {{ $t('welcome') }}-->
<!--            </h1>-->
<!--            <button class="button level-right" @click="show = !show">-->
<!--                <p v-if="show">{{ $t('hide') }}</p>-->
<!--                <p v-else>{{ $t('showFilter') }}</p>-->
<!--            </button>-->
<!--        </nav>-->
<!--        <Transition>-->
<!--            <div v-if="show" class="columns is-multiline is-mobile">-->
<!--                <div class="column is-two-thirds">-->
<!--                    <div class="field">-->
<!--                        <label>{{ $t('filter-name') }}</label>-->
<!--                        <div class="control">-->
<!--                            <input type="text" class="input" name="name" v-model="filter.name" >-->
<!--                        </div>-->
<!--                    </div>-->
<!--                </div>-->
<!--                <div class="column is-one-third">-->
<!--                    <div class="field">-->
<!--                        <label>{{ $t('filter-type') }}</label>-->
<!--                        <div class="control">-->
<!--                            <div class="select">-->
<!--                                <select name="type" id="type" v-model="filter.item_type" >-->
<!--                                    <option value=null>{{ $t('all') }}</option>-->
<!--                                    <option value="BR">{{ $t('request') }}</option>-->
<!--                                    <option value="DN">{{ $t('donation') }}</option>-->
<!--                                    <option value="LN">{{ $t('loan') }}</option>-->
<!--                                </select>-->
<!--                            </div>-->
<!--                        </div>-->
<!--                    </div>-->
<!--                </div>-->
<!--                <div class="column is-quarter">-->
<!--                    <div class="field">-->
<!--                        <label>{{ $t('category') }}</label>-->
<!--                        <div class="control">-->
<!--                            <div class="select">-->
<!--                                <select id="category" name="category" v-model="filter.category" >-->
<!--                                    <option value="FD">{{ $t('food') }}</option>-->
<!--                                    <option value="AN">{{ $t('animals') }}</option>-->
<!--                                    <option value="EN">{{ $t('aee') }}</option>-->
<!--                                    <option value="CL">{{ $t('collectors') }}</option>-->
<!--                                    <option value="HL">{{ $t('hh') }}</option>-->
<!--                                    <option value="DY">{{ $t('diy') }}</option>-->
<!--                                    <option value="BT">{{ $t('beauty') }}</option>-->
<!--                                    <option value="CH">{{ $t('childhood') }}</option>-->
<!--                                    <option value="IT">{{ $t('it') }}</option>-->
<!--                                    <option value="GD">{{ $t('garden') }}</option>-->
<!--                                    <option value="HS">{{ $t('house') }}</option>-->
<!--                                    <option value="HD">{{ $t('holidays') }}</option>-->
<!--                                    <option value="BK">{{ $t('book') }}</option>-->
<!--                                    <option value="SP">{{ $t('sport') }}</option>-->
<!--                                    <option value="TS">{{ $t('transport') }}</option>-->
<!--                                    <option value="OT">{{ $t('other') }}</option>-->
<!--                                </select>-->
<!--                            </div>-->
<!--                        </div>-->
<!--                    </div>-->
<!--                </div>-->
<!--                <div class="column is-full">-->
<!--                    <div class="field">-->
<!--                        <button class="button is-success" @click="getItemsLocation">{{ $t('search') }}</button>-->
<!--                    </div>-->
<!--                </div>-->
<!--            </div>-->
<!--        </Transition>-->
        
        <div class="p-3"></div>
<!--        <div id="mapid"></div>-->
        <div class="container" id="edit">
            <div class="modal" id="modal" style="z-index: 600;">
                <div class="modal-background"></div>
                <div class="modal-card">
                    <header class="modal-card-head">
                        <p class="modal-card-title">{{ nameToShow }}</p>
                        <button class="delete" aria-label="close" @click="closeEdit"></button>
                    </header>
                    <div class="modal-card-body">
                        <p>{{ descriptionToShow }}</p>
                    </div>
                    <footer class="modal-card-foot">
                        <div v-if="modalToShow['id']">
                            <router-link :to="{ name: 'itemDetail', params: { id: modalToShow['id']}}" class="button is-info is-small is-responsive">Details</router-link>
                        </div>
                    </footer>
                </div>
            </div>                  
        </div>
    </div>
</template>

<script>
import * as L from 'leaflet';
import 'leaflet.markercluster';
import 'leaflet-easybutton';
import axios from 'axios'
import ItemsFilters from '@/components/ItemsFilters';

import { latLng } from "leaflet";
import { LMap, LTileLayer, LControl, LMarker, LPopup, LTooltip } from "vue2-leaflet";

export default {
    name: 'ItemsMap',
  components: {ItemsFilters, LMap, LTileLayer, LControl},
  data() {
        return {
          zoom: 14,
          center: latLng(50.586276, 5.560470),
          url: 'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>',
          tileLayerOptions: {
            zoom: 14,
            maxZoom: 19
          },

          searchString: null,
          selectedTypes: null,
          selectedCategories: null,


            map: {},
            locations: [],
            show: false,
            filter: {},
            items: [],
	    item_type : {},
            markers: {},
            modalToShow: {},
            nameToShow: '',
            descriptionToShow: '',
	    typeToShow: '',
	    userToShow: '',
            latitude: null,
            longitude: null,
            item_images: {},
            popup: {},
        }
    },
    async mounted() {
      document.title = "Shareish | Map";
      this.setGeolocalizedPosition();


        this.item_images = new Map()
        this.popup = L.popup({minWidth : 100, closeButton : false})


        const success = (position) => {
            this.markers = new L.markerClusterGroup({
		disableClusteringAtZoom: 16,
		chunkedLoading: true,
		maxClusterRadius: 20
	    })
            this.getItemsLocation()
	    this.addExternalMarkersLocation()
        }

    },
    methods: {
      setGeolocalizedPosition() {
        navigator.geolocation.getCurrentPosition(position => {
          const coords = position.coords;
          this.center = latLng(coords.latitude, coords.longitude);
        })
      },
      async getItemsLocation(){
        try {
          let items = (await axios.post('/api/v1/requestFilter', {
            name: this.searchString,
            item_type: this.selectedTypes,
            category: this.selectedCategories
          })).data;

          this.items = items.map(item => {
            let latLong = item['location'].slice(17, -1).split(' ');
            return {...item, latitude: latLong[0], longitude: latLong[1]};
          })
        }
        catch (error) {
          console.log(error);
        }
      },
	
        async onMarkerClick(e){
            this.modalToShow = this.items[e.target.increment]
            await axios
                .get(`/api/v1/mapnd/${this.modalToShow['id']}`)
                .then(response => {
                    this.nameToShow = response.data['name']
                    this.descriptionToShow = response.data['description']
		    this.typeToShow = response.data['item_type']
                })
                .catch(error => {
                    console.log(error)
                })
            let elem = document.getElementById("modal")
            elem.classList.add("is-active")
        },
	
        async onMarkerHover(e){
            const itemId = e.target.item_id;
	    await this.getItemNameUser(itemId)
            this.popup.setLatLng(e.latlng);
            this.popup.openOn(this.map);
            try {
                let url;
                if(this.item_images.has(itemId) === false){
                    const uri = `/api/v1/item/${itemId}/image/first`;
                    const data = (await axios.get(uri)).data;
                    this.item_images.set(itemId, data['url']);
                    url = data['url'];
                }
                else {
                    url = this.item_images.get(itemId);
                }
                this.popup.setContent(
                    '<figure class="image">' +
                    '<img src="' + url +
		    '" style="object-fit: cover; width: 100%; height: 100%">' +
			'<br>' + this.nameToShow + 
			'<br>' + this.item_type + ' by ' + this.userToShow + 
                    '</figure>'
                );
            }
            catch (error) {
                console.log(error);
            }
        },

	//on external marker hover
	async onEMarkerHover(e){
	    var etype = e.target.type;
	    var ename = e.target.name;
	    if (ename === undefined) {
		ename = ""
	    }
	    this.popup.setLatLng(e.latlng);
            this.popup.openOn(this.map);
	    this.popup.setContent(ename+' <br>'+ '('+etype+' from OSM)');
	},

	
	async getItemType(id){
	    await axios
		    .get(`/api/v1/items/${id}`)
                    .then(response => {
			this.item_type = response.data['item_type']
                    })
                .catch(error => {
                    console.log(error)
                })
	},

	async getItemNameUser(id){
	    await axios
		    .get(`/api/v1/items/${id}`)
                    .then(response => {
			this.nameToShow = response.data['name']
			var userid = response.data['user']
			axios
			    .get(`/api/v1/webusers/${userid}/`)
			    .then(response2 => {
				this.userToShow = response2.data['username']
			    })
			    .catch(error => {
				console.log(JSON.stringify(error));
			    })
		    })
	    	.catch(error => {
                    console.log(error)
                })
	},

	
	
        onMarkerOut(e){
            this.popup.close()            
        },

	closeEdit(){
            let elem = document.getElementById("modal")
            elem.classList.remove("is-active")
            this.modalToShow = {}
        },

	async fetchAsync (url) {
		let response = await fetch(url);
		let data = await response.json();
		return data;
	},


	async getOverPassElements(tagkey,tagvalue) {
	    // "amenity"="public_bookcase"; "amenity"="give_box"; "amenity"="food_sharing"; "amenity"="freeshop"; emergency=drinking_water; emergency=defibrillator
	    // social_facility=food_bank
	    var overpassQuery = "\""+tagkey+"\""+'='+"\""+tagvalue+"\""
	    var bounds = this.map.getBounds().getSouth() + ',' + this.map.getBounds().getWest() + ',' + this.map.getBounds().getNorth() + ',' + this.map.getBounds().getEast();
	    var nodeQuery = 'node[' + overpassQuery + '](' + bounds + ');';
	    var query = '?data=[out:json][timeout:15];(' + nodeQuery + ');out body geom;';
            var baseUrl = 'http://overpass-api.de/api/interpreter';
            var resultUrl = baseUrl + query;
	    var response = await this.fetchAsync(resultUrl) 
	    return(response.elements)
	},


	createExternalMarkers(elements,icon){
	    var emarkerList =[]
	    for(let i = 0; i < elements.length; i++){
		var emarker = {}
		emarker = L.marker([elements[i]['lat'], elements[i]['lon']], {icon: icon})
		console.log(elements[i])
		if (elements[i]['tags']['amenity']) {
		    emarker.type = elements[i]['tags']['amenity']
		}
		else if (elements[i]['tags']['emergency']) {
		    emarker.type = elements[i]['tags']['emergency']
		}
		emarker.name = elements[i]['tags']['name']
		emarker.on('mouseover', this.onEMarkerHover)
		emarker.on('mouseout', this.onMarkerOut)
		emarkerList.push(emarker)
	    }
	    return emarkerList
	},
	
	async addExternalMarkersLocation(){
	    //import of external markers through OSM overpass API
	    //get public bookcases
	    var public_bookcase_icon = new L.Icon({
		iconUrl: 'https://wiki.openstreetmap.org/w/images/b/b2/Public_bookcase-14.svg',
		shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
		iconSize: [25, 41],
		iconAnchor: [12, 41],
		popupAnchor: [-10, -74],
		shadowSize: [41, 41]
	    });
	    var public_bookcases = await this.getOverPassElements("amenity","public_bookcase")
	    console.log(public_bookcases)
	    this.markers.addLayers(this.createExternalMarkers(public_bookcases,public_bookcase_icon))
	    this.map.addLayer(this.markers)


	    //get defibrilators
	    var aed_icon = new L.Icon({
		iconUrl: 'https://upload.wikimedia.org/wikipedia/commons/4/4b/ISO_7010_E010.svg',
		// author: MaxxL
		shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
		iconSize: [25, 41],
		iconAnchor: [12, 41],
		popupAnchor: [-10, -74],
		shadowSize: [41, 41]
	    });
	    var aeds = await this.getOverPassElements("emergency","defibrillator")
	    console.log(aeds)
	    this.markers.addLayers(this.createExternalMarkers(aeds,aed_icon))
	    this.map.addLayer(this.markers)


	    
	    //get give_boxes
	    var give_box_icon = new L.Icon({
		iconUrl: 'https://upload.wikimedia.org/wikipedia/commons/c/c6/Fridge_icon_2.png',
		//Tommaso.sansone91, CC BY-SA 4.0
		shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
		iconSize: [20, 31],
		iconAnchor: [12, 31],
		popupAnchor: [-10, -74],
		shadowSize: [41, 41]
	    });
	    var give_boxes = await this.getOverPassElements("amenity","give_box")
	    console.log(give_boxes)
	    this.markers.addLayers(this.createExternalMarkers(give_boxes,give_box_icon))
	    this.map.addLayer(this.markers)


	    //get drinking_water spots
	    var drinking_water_icon = new L.Icon({
		iconUrl: 'https://upload.wikimedia.org/wikipedia/commons/5/52/OCHA_humicons_water.png',
		// http://www.unocha.org/story/ocha-launches-500-free-humanitarian-symbols, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons
		shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
		iconSize: [25, 31],
		iconAnchor: [12, 41],
		popupAnchor: [-10, -74],
		shadowSize: [41, 41]
	    });
	    var drinking_water_spots = await this.getOverPassElements("amenity","drinking_water")
	    console.log(drinking_water_spots)
	    this.markers.addLayers(this.createExternalMarkers(drinking_water_spots,drinking_water_icon))
	    this.map.addLayer(this.markers)


	    //get freeshops
	    var free_shop_icon = new L.Icon({
		iconUrl: 'https://wiki.openstreetmap.org/w/images/b/b2/Public_bookcase-14.svg',
		shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
		iconSize: [25, 41],
		iconAnchor: [12, 41],
		popupAnchor: [-10, -74],
		shadowSize: [41, 41]
	    });
	    var free_shops = await this.getOverPassElements("amenity","free_shop")
	    console.log(free_shops)
	    this.markers.addLayers(this.createExternalMarkers(free_shops,free_shop_icon))
	    this.map.addLayer(this.markers)

	    
	},
	
	async addMarkersLocation(){
            if(this.map.hasLayer(this.markers)){
                this.markers.clearLayers()
            }

	    var progress = document.getElementById('progress');
	    var progressBar = document.getElementById('progress-bar');

	    function updateProgressBar(processed, total, elapsed, layersArray) {
		if (elapsed > 1000) {
		    // if it takes more than a second to load, display the progress bar:
		    progress.style.display = 'block';
		    progressBar.style.width = Math.round(processed/total*100) + '%';
		}

		if (processed === total) {
		    // all markers processed - hide the progress bar:
		    progress.style.display = 'none';
		}
	    }
	    
	    //colored icons for markers
	    var greenIcon = new L.Icon({
		iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
		shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
		iconSize: [25, 41],
		iconAnchor: [12, 41],
		popupAnchor: [-10, -74],
		shadowSize: [41, 41]
	    });
	    var yellowIcon = new L.Icon({
		iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-yellow.png',
		shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
		iconSize: [25, 41],
		iconAnchor: [12, 41],
		popupAnchor: [-10, -74],
		shadowSize: [41, 41]
	    });
	    var redIcon = new L.Icon({
		iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
		shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
		iconSize: [25, 41],
		iconAnchor: [12, 41],
		popupAnchor: [-10, -74],
		shadowSize: [41, 41]
	    });
	    var greyIcon = new L.Icon({
		iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-grey.png',
		shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
		iconSize: [25, 41],
		iconAnchor: [12, 41],
		popupAnchor: [-10, -74],
		shadowSize: [41, 41]
	    });

	    var markerList = []
            for(let i = 0; i < this.locations.length; i++){
		//marker colorization based on item_type
		var marker = {}
		await this.getItemType(this.locations[i]['id'])
		if (this.item_type==="DN"){
		    marker = L.marker([this.locations[i]['location_y'], this.locations[i]['location_x']], {icon: greenIcon})
		}
		else if (this.item_type==="LN"){
		    marker = L.marker([this.locations[i]['location_y'], this.locations[i]['location_x']], {icon: yellowIcon})
		}
		else if (this.item_type==="BR"){
		    marker = L.marker([this.locations[i]['location_y'], this.locations[i]['location_x']], {icon: redIcon})
		}
		else {
		    marker = L.marker([this.locations[i]['location_y'], this.locations[i]['location_x']], {icon: greyIcon})
		}
                marker.item_id = this.locations[i]['id']
                marker.increment = this.locations[i]['increment']
                marker.on('click', this.onMarkerClick);
                marker.on('mouseover', this.onMarkerHover)
                marker.on('mouseout', this.onMarkerOut)
		markerList.push(marker)
            }
	    this.markers.addLayers(markerList)
	    this.map.addLayer(this.markers)
        }
    },
}
</script>

<style scoped>
    #mapid {
        height: 800px;
        z-index: 400;
    }
</style>
