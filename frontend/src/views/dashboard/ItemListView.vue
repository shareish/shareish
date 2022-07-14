<template>
    <div class="page-item">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Items</h1>
            </div>

            <div class="column is-3" v-for="item in items" v-bind:key="item.id">
                <!-- <div class="box">
                    <h3 class="is-size-4 mb-4">{{ item.name }}</h3>
                    <router-link :to="{ name: 'itemDetail', params: { id: item.id }}" class="button is-light">Details</router-link>
                </div> -->

                <div class="card">
                    <div class="card-image">

                        <figure v-if="getImageURL(item.id)" class="image is-4by3">
                            <img :src="getImageURL(item.id)" alt="Placeholder image">
                        </figure>
                        <div v-else class="image is-4by3">
                           <img :src="require('@/assets/categories/' + getImageURLDefault(item.category1))" alt="Placeholder image">
                        </div>
                    </div>
                    <div class="card-content">
                        <div class="media">
                            <div class="media-left">
                                <figure v-if="getSmallImageURL(item.id)" class="image is-48x48">
                                    <img class="is-rounded" :src="getSmallImageURL(item.id)" alt="Placeholder image">
                                </figure>
                                <figure class="image is-inline-block is-responsive is-48x48" v-else>
                                    <img class="is-rounded" src="https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg">
                                </figure>
                            </div>
                            <div class="media-content">
                                <p class="title is-4">{{ item.name }}</p>
                                <p class="subtitle is-6">{{ item.category1 }}</p>
                            </div>
                        </div>

                        <div class="content has-text-centered">
                            {{ item.description }}
                            <br>
                            <br>
                            <router-link :to="{ name: 'itemDetail', params: { id: item.id }}" class="button is-info is-normal is-responsive">Details</router-link>
                        </div>
                    </div>
                </div>


            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import imagefinder from "../../assets/imagefinder.json"
export default {
    name: 'Item',
    data() {
        return {
            items: [],
            images: {},
            images2: []
        }
    },
    async mounted() {
        await this.getItems()
    },
    methods: {
        //ATTENTION le code est pas beau mais ça marchait pas sinon et je ne comprends pas pourquoi
        // async getItems() {
        //     await axios
        //         .get('/api/v1/items/')
        //         .then(response => {
        //             for(let i = 0; i < response.data.length; i++){
        //                 this.items.push(response.data[i])
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

        async getItems() {
            await axios
                .get('/api/v1/items/')
                .then(response => {
                    for(let i = 0; i < response.data.length; i++){
                        this.items.push(response.data[i])
                        if(response.data[i]['images'][0]){
                            axios
                                .get(`/api/v1/images/${response.data[i]['images'][0]}`)
                                .then(response2 => {
                                    var image = response2.data['image']
                                    const localhost = 'http://localhost:8000'
                                    image = localhost.concat(image)
                                    this.images[response.data[i]['id']] = image
                                })
                                .catch(error => {
                                    console.log(JSON.stringify(error))
                                })
                        }
                        if(response.data[i]['user']){
                            axios
                                .get(`/api/v1/users/${response.data[i]['user']}`)
                                .then(response3 => {
                                    this.images2[response.data[i]['id']] = response3.data['image']
                                })
                                .catch(error => {
                                    console.log(JSON.stringify(error))
                                })
                        }
                    }
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        },
        async getImage(image_id){
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
        getImageURLDefault(category){
            console.log('coucou')
            return imagefinder[category]
        },
        getSmallImageURL(index){
            if(this.images2[index] == '' || this.images2[index] == undefined){
                return ''
            }
            return this.images2[index]   
        }
    },
}
</script>