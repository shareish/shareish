<template>
    <div class="page-item">
        <div class="columns is-multiline">
            <div class="column is-full">
                <h1 class="title">{{ item.name }} {{ item.id }}</h1>
            </div>
            <div class="column is-half">
                <h2 class="subtitle">Details</h2>

                <p v-if="item.category1">{{ item.category1 }}</p>
                <p v-if="item.category2">{{ item.category2 }}</p>
                <p v-if="item.category3">{{ item.category3 }}</p>
                <p v-if="item.description">{{ item.description }}</p>
            </div>
            <div class="column is-half">
                <figure class="image is-128x128">
                    <img :src="getImgUrl()">
                </figure>
            </div>
        </div>
    </div>

    <button class="button is-danger" @click="deleteItem()" >Delete</button>
    
</template>

<script>
import axios from 'axios'
export default {
    name: 'ItemDetail',
    data() {
        return {
            item: {},
            image : null
        }
    },
    mounted() {
        this.getItem()
    },
    methods: {
        getImgUrl(){
            return this.image
        },
        deleteItem(){
            const itemID = this.$route.params.id
            axios
                .delete(`/api/v1/items/${itemID}`)
                .then(response => {
                    this.$router.push('/dashboard/items')
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        },
        getItem() {
            console.log(this.$store.state.user.email)
            const itemID = this.$route.params.id
            axios
                .get(`/api/v1/items/${itemID}`)
                .then(response => {
                    this.item = response.data
                    axios
                        .get(`/api/v1/images/${this.item['images'][0]}`)
                        .then(response => {
                            this.image = response.data['image']
                            const localhost = 'http://localhost:8000'
                            this.image = localhost.concat(this.image)
                            console.log(this.image)
                        })
                        .catch(error => {
                            console.log(JSON.stringify(error))
                        })
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        }
    },
}
</script>