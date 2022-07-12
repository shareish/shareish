<template>
    <div class="page-barter">
        <div class="columns is-multiline">
            <div class="column is-full">
                <h1 class="title">{{ barter.name }} {{ barter.id }}</h1>
            </div>
            <div class="column is-half">
                <h2 class="subtitle">Details</h2>

                <p v-if="barter.category1">{{ barter.category1 }}</p>
                <p v-if="barter.category2">{{ barter.category2 }}</p>
                <p v-if="barter.category3">{{ barter.category3 }}</p>
                <p v-if="barter.description">{{ barter.description }}</p>
            </div>
            <div class="column is-half">
                <figure class="image is-128x128">
                    <img :src="getImgUrl()">
                </figure>
            </div>
        </div>
    </div>

    <button class="button is-danger" @click="deleteBarter()" >Delete</button>
    
</template>

<script>
import axios from 'axios'
export default {
    name: 'BarterDetail',
    data() {
        return {
            barter: {},
            image : null
        }
    },
    mounted() {
        this.getBarter()
    },
    methods: {
        getImgUrl(){
            return this.image
        },
        deleteBarter(){
            const barterID = this.$route.params.id
            axios
                .delete(`/api/v1/barters/${barterID}`)
                .then(response => {
                    this.$router.push('/dashboard/barters')
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        },
        getBarter() {
            console.log(this.$store.state.user.email)
            const barterID = this.$route.params.id
            axios
                .get(`/api/v1/barters/${barterID}`)
                .then(response => {
                    this.barter = response.data
                    axios
                        .get(`/api/v1/images/${this.barter['images'][0]}`)
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