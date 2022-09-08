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
            <div id="more" class="column is-3">
                <a @click="showMore">
                    <div class="card">
                        <div class="card-image">
                            <figure class="image is-1by1">
                                <img class="is-rounded" src="../../../public/mymap/images/plus.png" alt="ShowMoreImage">
                            </figure>
                        </div>
                        <div class="card-content">
                            <div class="content has-text-centered">
                                Show more
                            </div>
                        </div>
                    </div>
                </a>
            </div>
            <div class="column is-3 is-vcentered">
                <progress id="loading" style="display: none;" class="progress is-danger " max="100">30%</progress>
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
            imageUsers: [],
            search: '',
            apiCall: '',
            pageNumber: 1
        }
    },
    async mounted() {
        this.apiCall = '/api/v1/requestItems/?page=1'
        this.search = this.$route.params['data']
        document.title = "Shareish | Search for " + this.search
        this.toggleMoreLoad()
        await this.getItems()
        this.toggleMoreLoad()
    },
    methods: {
        async getItems() {
            let plus = document.getElementById('more')
            let loading = document.getElementById('loading')
            plus.style.display = "none"
            loading.style.display = "block"
            const formData = new FormData()
            formData.append('search', this.search)

            await axios
                .post(this.apiCall, formData)
                .then(async response => {
                    let data = response.data.results
                    if(response.data.next == null){
                        let plus = document.getElementById('more')
                        let loading = document.getElementById('loading')
                        if(plus != null && loading != null){
                            plus.remove()
                            loading.remove()
                        }
                    }else{
                        this.pageNumber++
                        this.apiCall = '/api/v1/requestItems/?page=' + this.pageNumber
                    }
                    for(let i = 0; i < data.length; i++){
                        this.items.push(data[i])
                        if(data[i]['images'][0]){
                            await axios
                                .get(`/api/v1/images/${data[i]['images'][0]}`)
                                .then(response2 => {
                                    this.images[data[i]['id']] = response2.data['url']
                                })
                                .catch(error => {
                                    console.log(JSON.stringify(error))
                                })
                        }
                        if(data[i]['user']){
                            await axios
                                .get(`/api/v1/webusers/${data[i]['user']}`)
                                .then(async response3 => {
                                    if(response3.data['image'][0]){
                                        await axios
                                        .get(`/api/v1/user_image/${response3.data['image'][0]}/`)
                                        .then(responseImage => {
                                            this.imageUsers[data[i]['id']] =
                                                responseImage.data['url']
                                        })
                                        .catch(error => {
                                            console.log(error)
                                        })
                                    }
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
            loading.style.display = "none"
            plus.style.display = "block"
        },
        async getUserImage(image_id){
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
        toggleMoreLoad(){
            let plus = document.getElementById('more')
            let loading = document.getElementById('loading')
            if(plus != null && loading != null && plus.style != null && loading.style != null){
                if(plus.style.display == 'block'){
                    plus.style.display = 'none'
                    loading.style.display = 'block'
                }else{
                    plus.style.display = 'block'
                    loading.style.display = 'none'
                }
            }
        },
        getImageURL(index){
            return this.images[index]
        },
        getImageURLDefault(category){
            return imagefinder[category]
        },
        getSmallImageURL(index){
            return this.imageUsers[index] 
        },
        showMore(){
            this.getItems()
        }
    },
}
</script>

<style scoped>
.is-vcentered {
  display: flex;
  flex-wrap: wrap;
  align-content: center;
  align-items: center;}
</style>