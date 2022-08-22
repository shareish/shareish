<template>
    <div class="page-my-account">
        <div class="columns is-centered is-multiline">
            <div class="column is-6 p-3 has-text-centered">
                <figure class="image is-inline-block is-responsive is-96x96" v-if="getImageURL()">
                    <img :src="getImageURL()" class="is-rounded">
                </figure>
                <figure class="image is-inline-block is-responsive is-96x96" v-else>
                    <img src="https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg">
                </figure>
                <div class="tile mt-5 pt-5 is-child pink card-bio">
                    <h2 id="isse" class="title pt-5 is-2 name">Hi, I'm {{ user.first_name }} {{ user.last_name }} (AKA {{ user.username }})</h2>
                    <p>{{ user.description }}</p>
                    <hr class="hr mx-auto has-text-centered">

                    <div class="container">
                        <h2 class="is-size-3 has-text-centered mt-5">Last Items</h2>
                        <hr class="hr mx-auto has-text-centered">
                        <div class="columns is-multiline is-centered">
                            <div class="column is-6" v-for="item in items" v-bind:key="item.id">
                                <div class="card">
                                    <div class="card-image">

                                        <figure v-if="getImageItemURL(item.id)" class="image is-4by3">
                                            <img :src="getImageItemURL(item.id)" alt="Placeholder image">
                                        </figure>
                                        <div v-else class="image is-4by3">
                                            <img :src="require('@/assets/categories/' + getImageURLDefault(item.category1))" alt="Placeholder image">
                                        </div>
                                    </div>
                                    <div class="card-content">
                                        <div class="media">
                                            <div class="media-left">
                                                <figure class="image is-48x48">
                                                <!-- <img :src="getSmallImageURL(item.id)" alt="Placeholder image"> -->User's photo
                                                </figure>
                                            </div>
                                            <div class="media-content">
                                                <p class="title is-4">{{ item.name }}</p>
                                                <p class="subtitle is-6">{{ item.category1 }}</p>
                                            </div>
                                        </div>

                                        <div class="content">
                                            {{ item.description }}
                                            <br>
                                            <router-link :to="{ name: 'itemDetail', params: { id: item.id }}" class="button is-info is-normal is-responsive">Details</router-link>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <br>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import imagefinder from "../../assets/imagefinder.json"

export default {
    name: 'UserDetail',
    data() {
        return {
            user: {},
            items: [],
            images: {},
            userID: null,
        }
    },
    mounted() {
        this.userID = this.$route.params.id
        this.getUser()
    },
    methods: {
        getUser() {
            axios
                .get(`/api/v1/webusers/${this.userID}/`)
                .then(response => {
                    this.user = Object.assign({}, response.data)
                    this.changes = Object.assign({}, response.data)
                    this.getItems(response)
                    this.getImage(response)
                })
                .catch(error1 => {
                    console.log(JSON.stringify(error1))
                })
        },
        async getImage(user){
            if(user.data['image'][0]){
                await axios
                .get(`/api/v1/user_image/${user.data['image'][0]}/`)
                .then(response => {
                    var image = response.data['image']
                    const localhost = 'http://' + window.location.hostname
                    image = localhost.concat(image)
                    this.userImage = image
                })
                .catch(error => {
                    console.log(error)
                })
            }
        },
        getItems(user) {
            for(let i = 0; i < user.data['items'].length; i++){
                axios
                    .get(`/api/v1/items/${user.data['items'][i]}`)
                    .then(response => {
                        this.items.push(response.data)
                        if(response.data['images'][0]){
                            axios
                                .get(`/api/v1/images/${response.data['images'][0]}`)
                                .then(response2 => {
                                    var image = response2.data['image']
                                    const localhost = 'http://' + window.location.hostname
                                    image = localhost.concat(image)
                                    this.images[response.data['id']] = image
                                })
                                .catch(error2 => {
                                    console.log(JSON.stringify(error2))
                                })
                        }
                    })
                    .catch(error1 => {
                        console.log(JSON.stringify(error1))
                    })
            }
        },
        getImageURL(){
            return this.userImage
        },
        getImageItemURL(index){
            return this.images[index]
        },
        getSmallImageURL(index){
            return this.images2[index]
        },
        getImageURLDefault(category){
            return imagefinder[category]
        },
    },
}
</script>