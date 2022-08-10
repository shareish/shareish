<template>
    <div class="page-item">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Items</h1>
            </div>

            <div class="column is-3" v-for="item in items" v-bind:key="item.id">

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
                                <router-link :to="{ name: 'userDetail', params: { id: item.user }}" class="">
                                    <figure v-if="getSmallImageURL(item.id)" class="image is-48x48">
                                        <img class="is-rounded" :src="getSmallImageURL(item.id)" alt="Placeholder image">
                                    </figure>
                                    <figure class="image is-inline-block is-responsive is-48x48" v-else>
                                        <img class="is-rounded" src="https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg">
                                    </figure>
                                </router-link>
                                
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
    name: 'ResultsSearch',
    data() {
        return {
            items: [],
            images: {},
            images2: [],
            search: '',
        }
    },
    async mounted() {
        this.search = this.$route.params['data']
        //TODO faire une recherche axios sur un nouveau ItemViewSet qu'il faut faire pour envoyer une liste d'id et en retirer cette liste.
        await this.getItems()
    },
    methods: {
        async getItems() {
            const formData = new FormData()
            formData.append('search', this.search)
            await axios
                .post('/api/v1/requestItems/', formData)
                .then(response => {
                    this.items = response.data
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
            console.log(this.items)
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