<template>
    <div class="page-barter">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Barters</h1>
            </div>

            <div class="column is-3" v-for="barter in barters" v-bind:key="barter.id">
                <!-- <div class="box">
                    <h3 class="is-size-4 mb-4">{{ barter.name }}</h3>
                    <router-link :to="{ name: 'barterDetail', params: { id: barter.id }}" class="button is-light">Details</router-link>
                </div> -->

                <div class="card">
                    <div class="card-image">

                        <figure v-if="getImageURL(barter.id)" class="image is-4by3">
                            <img :src="getImageURL(barter.id)" alt="Placeholder image">
                        </figure>
                        <div v-else class="image is-4by3">
                            No content Image
                        </div>
                    </div>
                    <div class="card-content">
                        <div class="media">
                            <div class="media-left">
                                <figure class="image is-48x48">
                                <!-- <img :src="getSmallImageURL(barter.id)" alt="Placeholder image"> -->User's photo
                                </figure>
                            </div>
                            <div class="media-content">
                                <p class="title is-4">{{ barter.name }}</p>
                                <p class="subtitle is-6">{{ barter.category1 }}</p>
                            </div>
                        </div>

                        <div class="content">
                            {{ barter.description }}
                            <br>
                            <router-link :to="{ name: 'barterDetail', params: { id: barter.id }}" class="button is-light">Details</router-link>
                        </div>
                    </div>
                </div>


            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'Barter',
    data() {
        return {
            barters: [],
            images: {},
            images2: {}
        }
    },
    mounted() {
        this.getBarters()
    },
    methods: {
        //ATTENTION le code est pas beau mais ça marchait pas sinon et je ne comprends pas pourquoi
        // async getBarters() {
        //     await axios
        //         .get('/api/v1/barters/')
        //         .then(response => {
        //             for(let i = 0; i < response.data.length; i++){
        //                 this.barters.push(response.data[i])
        //                 if(response.data[i]['images'][0]){
        //                     var image = this.getImage(response.data[i]['images'][0])
        //                     console.log(image)
        //                     const localhost = 'http://localhost:8000'
        //                     image = localhost.concat(image)
        //                     this.images[response.data[i]['id']] = image
        //                     if(response.data[i]['images'][1]){
        //                         let image2 = this.getImage(response.data[i]['images'][1])
        //                         const localhost = 'http://localhost:8000'
        //                         image2 = localhost.concat(image2)
        //                         this.images2[response.data[i]['id']] = image2
        //                     }
        //                 }
        //             }
        //         })
        //         .catch(error => {
        //             console.log(JSON.stringify(error))
        //         })
        // },

        getBarters() {
            axios
                .get('/api/v1/barters/')
                .then(response => {
                    console.log(response)
                    for(let i = 0; i < response.data.length; i++){
                        this.barters.push(response.data[i])
                        if(response.data[i]['images'][0]){
                            axios
                                .get(`/api/v1/images/${response.data[i]['images'][0]}`)
                                .then(response2 => {
                                    var image = response2.data['image']
                                    console.log(image)
                                    const localhost = 'http://localhost:8000'
                                    image = localhost.concat(image)
                                    this.images[response.data[i]['id']] = image

                                    // if(response.data[i]['user']){
                                    //     axios
                                    //         .get(`/api/v1/users/${response.data[i]['user']}`)
                                    //         .then(response3 => {
                                    //             var image2 = response3.data['image']
                                    //             image2 = localhost.concat(image2)
                                    //             this.images2[response.data[i]['id']] = image2
                                    //         })
                                    //         .catch(error => {
                                    //             console.log(JSON.stringify(error))
                                    //         })
                                    // }.
                                    // A voir plus tard pour la photo de profil de l'utilisateur
                                })
                                .catch(error => {
                                    console.log(JSON.stringify(error))
                                })
                        }
                    }
                    console.log(this.images)
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        },
        async getImage(image_id){
            var imageURL = ''
            console.log(image_id)
            await axios
                .get(`/api/v1/images/${image_id}`)
                .then(response => {
                    imageURL = response.data['image']
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
            return imageURL
        },
        async getImage2(image_id){
            var imageURL = ''
            await axios
                .get(`/api/v1/images/${image_id}`)
                .then(response => {
                    imageURL = response.data['image']
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
            return imageURL
        },
        getImageURL(index){
            return this.images[index]
        },
        getSmallImageURL(index){
            return this.images2[index]
        }
    },
}
</script>