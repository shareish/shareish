<template>
    <div class="page-dashboard">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title has-text-centered">Welcome to SHAREISH</h1>
            </div>
        </div>
        <div style="display: none" id="location_x" data-json="{{ location_x }}"></div>
        <div style="display: none" id="location_y" data-json="{{ location_y }}"></div>
        <div style="display: none" id="name" data-json="{{ name }}"></div>
        <div id="mapid"></div>

    </div>
</template>

<script>
import leaflet from "leaflet";
import { onMounted } from 'vue';
import axios from 'axios'
export default {
    name: 'Dashboard',
    data() {
        return {
            map: {},
            locations: []
        }
    },
    async mounted() {
        this.map = leaflet.map('mapid').locate({
            setView: true,
            maxZoom: 19,
            enableHighAccuracy: true,
        }).on("locationfound", (e) => this.map.setView(e.latlng, 16)).on("locationerror", () => this.map.setView([50.586276, 5.560470], 14));
        leaflet.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png ', {
            maxZoom: 19,
            zoom: 16,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(this.map);

        await this.getBartersLocation()
        console.log(this.locations)

        for(let i = 0; i < this.locations.length; i++){
            console.log(this.locations[i])
            leaflet.marker([this.locations[i]['location_y'], this.locations[i]['location_x']], {
            }).addTo(this.map);
        }

        // var markers = new leaflet.MarkerClusterGroup();

        // for(let i = 0; i < this.locations.length; i++){
        //     markers.addLayer(leaflet.marker([this.locations[i]['location_y'], this.locations[i]['location_x']]));
        // }

        // this.map.addLayer(markers);

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
    },
}
</script>

<style scoped>
    #mapid {
        height: 400px;
    }
</style>