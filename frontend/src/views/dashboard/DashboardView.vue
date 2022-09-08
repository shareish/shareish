<template>
    <div class="page-dashboard">
        <nav class="level">
            <h1 class="level-left">
                {{ $t('welcome') }}
            </h1>
            <button class="button level-right" @click="show = !show">
                <p v-if="show">{{ $t('hide') }}</p>
                <p v-else>{{ $t('showFilter') }}</p>
            </button>
        </nav>
        <Transition>
            <div v-if="show" class="columns is-multiline is-mobile">
                <div class="column is-two-thirds">
                    <div class="field">
                        <label>{{ $t('filter-name') }}</label>
                        <div class="control">
                            <input type="text" class="input" name="name" v-model="filter.name" >
                        </div>
                    </div>
                </div>
                <div class="column is-one-third">
                    <div class="field">
                        <label>{{ $t('filter-type') }}</label>
                        <div class="control">
                            <div class="select">
                                <select name="type" id="type" v-model="filter.item_type" >
                                    <option value=null>{{ $t('all') }}</option>
                                    <option value="BR">{{ $t('request') }}</option>
                                    <option value="DN">{{ $t('donation') }}</option>
                                    <option value="LN">{{ $t('loan') }}</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="column is-quarter">
                    <div class="field">
                        <label>{{ $t('category') }}</label>
                        <div class="control">
                            <div class="select">
                                <select id="category" name="category" v-model="filter.category" >
                                    <option value="FD">{{ $t('food') }}</option>
                                    <option value="AN">{{ $t('animals') }}</option>
                                    <option value="EN">{{ $t('aee') }}</option>
                                    <option value="CL">{{ $t('collectors') }}</option>
                                    <option value="HL">{{ $t('hh') }}</option>
                                    <option value="DY">{{ $t('diy') }}</option>
                                    <option value="BT">{{ $t('beauty') }}</option>
                                    <option value="CH">{{ $t('childhood') }}</option>
                                    <option value="IT">{{ $t('it') }}</option>
                                    <option value="GD">{{ $t('garden') }}</option>
                                    <option value="HS">{{ $t('house') }}</option>
                                    <option value="HD">{{ $t('holidays') }}</option>
                                    <option value="BK">{{ $t('book') }}</option>
                                    <option value="SP">{{ $t('sport') }}</option>
                                    <option value="TS">{{ $t('transport') }}</option>
                                    <option value="OT">{{ $t('other') }}</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="column is-full">
                    <div class="field">
                        <button class="button is-success" @click="getItemsLocation">{{ $t('search') }}</button>
                    </div>
                </div>
            </div>
        </Transition>
        
        <div class="p-3"></div>
        <div id="mapid"></div>
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
export default {
    name: 'Dashboard',
    data() {
        return {
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
            latitude: null,
            longitude: null,
            zoom: null,
            item_images: {},
            popup: {},
        }
    },
    async mounted() {
        document.title = "Shareish | Map"

        this.item_images = new Map()
        this.popup = L.popup({minWidth : 100, closeButton : false})

        const setPosition = (position) => {
            this.map.setView([position.coords.latitude, position.coords.longitude], this.zoom)
        }

        const success = (position) => {
            this.latitude = position.coords.latitude
            this.longitude = position.coords.longitude
            this.zoom = 16
            this.map = L.map('mapid').setView([this.latitude, this.longitude], this.zoom)
            L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png ', {
                maxZoom: 19,
                zoom: 16,
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>'
            }).addTo(this.map);

            L.easyButton('<i class="fa fa-map-marker"><i>', function(btn, map){
                navigator.geolocation.getCurrentPosition(setPosition)
            }).addTo(this.map);

            this.filter.item_type = 'null'
            this.markers = new L.markerClusterGroup({
		disableClusteringAtZoom: 16,
		chunkedLoading: true,
	    })
            this.getItemsLocation()
        }

        const error = () => {
            this.latitude = 50.586276
            this.longitude = 5.560470
            this.zoom = 14
            this.map = L.map('mapid').setView([this.latitude, this.longitude], this.zoom)
            L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png ', {
                maxZoom: 19,
                zoom: 16,
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>'
            }).addTo(this.map);

            this.filter.item_type = 'null'
	    this.markers = new L.markerClusterGroup({
		disableClusteringAtZoom: 16})
            this.getItemsLocation()
        }

        navigator.geolocation.getCurrentPosition(success, error)

        
    },
    methods: {
        async getItemsLocation(){
            await axios
                .post('/api/v1/requestFilter/', this.filter)
                .then(response => {
                    this.locations = []
                    this.items = response.data
                    for(let i = 0; i < response.data.length; i++){
                        if(response.data[i]['location'] != null){
			    //console.log(response.data[i])
			    //console.log("---")
                            let refinedLocation = response.data[i]['location'].slice(17, -1)
                            const arrlocations = refinedLocation.split(" ")
                            let location = {
                                'location_x': arrlocations[1],
                                'location_y': arrlocations[0],
                                'id': response.data[i]['id'],
                                'increment': i
                            }
                            this.locations.push(location)
                        }
                    }
                    this.addMarkersLocation()
                })
                .catch(error => {
                    console.log(error)
                })    
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
            this.popup.setLatLng(e.latlng)
            //this.popup.setContent("Coucou ça charge")
            this.popup.openOn(this.map)
            if(this.item_images.has(e.target.item_id) == false){
                const formData = new FormData()
                formData.append('id', e.target.item_id)
                axios
                    .post('/api/v1/getItemImage/', formData)
                    .then(response => {
                        const localhost = 'https://' + window.location.hostname
                        this.item_images.set(e.target.item_id, localhost.concat(response.data['image']))
                        this.popup.setContent('<figure class="image"><img src="' + localhost.concat(response.data['image']) + '" alt="Placeholder image" style="object-fit: cover; width: 100%; height: 100%"></figure>')
                    })
                    .catch(error => {
                        console.log(error)
                    })
            }else{
                this.popup.setContent('<figure class="image"><img src="' + this.item_images.get(e.target.item_id) + '" alt="Placeholder image" style="object-fit: cover; width: 100%; height: 100%"></figure>')
            }
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

        onMarkerOut(e){
            this.popup.close()            
        },

	closeEdit(){
            let elem = document.getElementById("modal")
            elem.classList.remove("is-active")
            this.modalToShow = {}
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
		popupAnchor: [1, -34],
		shadowSize: [41, 41]
	    });
	    var yellowIcon = new L.Icon({
		iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-yellow.png',
		shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
		iconSize: [25, 41],
		iconAnchor: [12, 41],
		popupAnchor: [1, -34],
		shadowSize: [41, 41]
	    });
	    var redIcon = new L.Icon({
		iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
		shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
		iconSize: [25, 41],
		iconAnchor: [12, 41],
		popupAnchor: [1, -34],
		shadowSize: [41, 41]
	    });
	    var greyIcon = new L.Icon({
		iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-grey.png',
		shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
		iconSize: [25, 41],
		iconAnchor: [12, 41],
		popupAnchor: [1, -34],
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
                //this.markers.addLayer(marker)
            }
	    this.markers.addLayers(markerList)
            //this.map.addLayer(this.markers)
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
