<template>
    <div class="page-dashboard">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title has-text-centered">Welcome to SHAREISH</h1>
            </div>
        </div>

        <nav class="level-right">
            <button class="button level-right" @click="show = !show">
                <p v-if="show">Hide filters</p>
                <p v-else>Show filters</p>
            </button>
        </nav>
        <Transition>
            <div v-if="show" class="columns is-multiline is-mobile">
                <div class="column is-two-thirds">
                    <div class="field">
                        <label>Text to search (in the description or in the name)</label>
                        <div class="control">
                            <input type="text" class="input" name="name" v-model="filter.name" >
                        </div>
                    </div>
                </div>
                <div class="column is-one-third">
                    <div class="field">
                        <label>Type of the article</label>
                        <div class="control">
                            <div class="select">
                                <select name="type" id="type" v-model="filter.barter_type" >
                                    <option value="BR">Barter</option>
                                    <option value="DN">Donation</option>
                                    <option value="LN">Loan</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="column is-quarter">
                    <div class="field">
                        <label>Category</label>
                        <div class="control">
                            <div class="select">
                                <select id="category" name="category" v-model="filter.category" >
                                    <option value="FD">Food</option>
                                    <option value="AN">Animals</option>
                                    <option value="EN">Arts and Entertainments</option>
                                    <option value="CL">Collectors</option>
                                    <option value="HL">Helping hand</option>
                                    <option value="DY">DIY</option>
                                    <option value="BT">Beauty and Well-being</option>
                                    <option value="CH">Childhood</option>
                                    <option value="IT">IT and Multimedia</option>
                                    <option value="GD">Garden</option>
                                    <option value="HS">House</option>
                                    <option value="HD">Holidays and Week-end</option>
                                    <option value="BK">Books, CDs and DVDs</option>
                                    <option value="SP">Sport and Leisure</option>
                                    <option value="TS">Transport and vehicle</option>
                                    <option value="OT">Other</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="column is-full">
                    <div class="field">
                        <button class="button is-success" @click="submitFilters">Search</button>
                    </div>
                </div>
            </div>
        </Transition>
        
        <div class="p-3"></div>
        <div style="display: none" id="location_x" data-json="{{ location_x }}"></div>
        <div style="display: none" id="location_y" data-json="{{ location_y }}"></div>
        <div style="display: none" id="name" data-json="{{ name }}"></div>
        <div id="mapid"></div>

    </div>
</template>

<script>
import * as L from 'leaflet';
import 'leaflet.markercluster';
import { onMounted } from 'vue';
import axios from 'axios'
export default {
    name: 'Dashboard',
    data() {
        return {
            map: {},
            locations: [],
            show: false,
            filter: {}
        }
    },
    async mounted() {
        this.map = L.map('mapid').locate({
            setView: true,
            maxZoom: 19,
            enableHighAccuracy: true,
        }).on("locationfound", (e) => this.map.setView(e.latlng, 16)).on("locationerror", () => this.map.setView([50.586276, 5.560470], 14));
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png ', {
            maxZoom: 19,
            zoom: 16,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(this.map);

        await this.getBartersLocation()
        console.log(this.locations)

        var markers = new L.MarkerClusterGroup();

        for(let i = 0; i < this.locations.length; i++){
            markers.addLayer(L.marker([this.locations[i]['location_y'], this.locations[i]['location_x']]));
        }

        this.map.addLayer(markers);

    },
    methods: {
        async getBartersLocation(){
            await axios
                .get('/api/v1/barters/')
                .then(response => {
                    for(let i = 0; i < response.data.length; i++){
                        if(response.data[i]['location'] != null){
                            let refinedLocation = response.data[i]['location'].slice(17, -1)
                            const arrlocations = refinedLocation.split(" ")
                            let location = {
                                'location_x': arrlocations[0],
                                'location_y': arrlocations[1],
                            }
                            this.locations.push(location)
                        }
                    }
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })    
        },
        readLocation(){

        },
        submitFilters(){
            axios
                .post('/api/v1/request/', this.filter)
                .then(response => {
                    console.log(response.data[0])
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        }
    },
}
</script>

<style scoped>
    #mapid {
        height: 600px;
    }

    .v-enter-active,
    .v-leave-active {
        transition: opacity 0.1s ease;
    }

    .v-enter-from,
    .v-leave-to {
        opacity: 0;
    }
</style>