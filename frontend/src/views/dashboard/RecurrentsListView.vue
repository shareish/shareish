<template>
    <div class="page-item">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Your recurrent Items</h1>
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
                            <div class="media-content">
                                <p class="title is-4">{{ item.name }}</p>
                                <p class="subtitle is-6">{{ item.category1 }}</p>
                            </div>
                        </div>

                        <div class="content has-text-centered">
                            {{ item.description }}
                            <br>
                            <br>
                            <router-link :to="{ name: 'addItem', params: { id: item.id }}" class="button is-info is-normal is-responsive">Submit again</router-link>
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
    name: 'Recurrents',
    data() {
        return {
            items: [],
            images: {},
        }
    },
    async mounted() {
        await this.getItems()
    },
    methods: {
        async getItems() {
            await axios
                .get('/api/v1/recurrents/')
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
                    }
                })
                .catch(error => {
                    console.log(error)
                })
        },
        getImageURLDefault(category){
            return imagefinder[category]
        },
        getImageURL(index){
            return this.images[index]
        },
    },
}
</script>