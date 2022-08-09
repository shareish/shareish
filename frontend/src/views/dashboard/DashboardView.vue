<template>
    <div class="page-dashboard">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title has-text-centered"> {{ $t('welcome') }} </h1>
            </div>
        </div>

        <nav class="level-right">
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
                        <button class="button is-success" @click="submitFilters">{{ $t('search') }}</button>
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

        await this.getItemsLocation()
        console.log(this.locations)

        var markers = new L.MarkerClusterGroup();

        for(let i = 0; i < this.locations.length; i++){
            markers.addLayer(L.marker([this.locations[i]['location_y'], this.locations[i]['location_x']]));
        }

        this.map.addLayer(markers);
    },
    methods: {
        async getItemsLocation(){
            await axios
                .get('/api/v1/actives/')
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
                    console.log(response.data)
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