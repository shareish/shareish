<template>
    <div class="page-my-account">
        <h1 class="title has-text-centered">My Account</h1>

        <div class="columns is-centered is-multiline">
            <div class="column is-6 p-3 has-text-centered">
                <figure class="image is-inline-block is-responsive is-96x96" v-if="getImageURL(user.image)">
                    <img :src="getImageURL(user.image)" class="is-rounded">
                </figure>
                <figure class="image is-inline-block is-responsive is-96x96" v-else>
                    <img src="https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg">
                </figure>
                <div class="tile mt-5 pt-5 is-child pink card-bio">
                    <h2 id="isse" class="title pt-5 is-2 name">Hi, I'm {{ user.first_name }} {{ user.last_name }}</h2>
                    <hr class="hr mx-auto has-text-centered">
                    <div class="buttons is-centered mt-2">
                        <button id="i038h" class="button is-medium is-twitter">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="30px" height="30px"><path d="M22.46 6c-.77.35-1.6.58-2.46.69.88-.53 1.56-1.37 1.88-2.38-.83.5-1.75.85-2.72 1.05C18.37 4.5 17.26 4 16 4c-2.35 0-4.27 1.92-4.27 4.29 0 .34.04.67.11.98C8.28 9.09 5.11 7.38 3 4.79c-.37.63-.58 1.37-.58 2.15 0 1.49.75 2.81 1.91 3.56-.71 0-1.37-.2-1.95-.5v.03c0 2.08 1.48 3.82 3.44 4.21a4.22 4.22 0 0 1-1.93.07 4.28 4.28 0 0 0 4 2.98 8.521 8.521 0 0 1-5.33 1.84c-.34 0-.68-.02-1.02-.06C3.44 20.29 5.7 21 8.12 21 16 21 20.33 14.46 20.33 8.79c0-.19 0-.37-.01-.56.84-.6 1.56-1.36 2.14-2.23z"></path></svg>
                        </button>
                        <button id="in64v" class="button is-medium is-linkedin">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="30px" height="30px"><path d="M7.8 2h8.4C19.4 2 22 4.6 22 7.8v8.4c0 3.2-2.6 5.8-5.8 5.8H7.8C4.6 22 2 19.4 2 16.2V7.8C2 4.6 4.6 2 7.8 2m-.2 2C5.61 4 4 5.61 4 7.6v8.8C4 18.39 5.61 20 7.6 20h8.8c1.99 0 3.6-1.61 3.6-3.6V7.6C20 5.61 18.39 4 16.4 4H7.6m9.65 1.5a1.25 1.25 0 1 1 0 2.5 1.25 1.25 0 0 1 0-2.5M12 7c2.76 0 5 2.24 5 5s-2.24 5-5 5-5-2.24-5-5 2.24-5 5-5m0 2c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"></path></svg>
                        </button>
                        <button id="ih1xx" class="button is-medium is-facebook">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="30px" height="30px"><path d="M9.04 21.54c.96.29 1.93.46 2.96.46 5.52 0 10-4.48 10-10S17.52 2 12 2 2 6.48 2 12c0 4.25 2.67 7.9 6.44 9.34-.09-.78-.18-2.07 0-2.96l1.15-4.94s-.29-.58-.29-1.5c0-1.38.86-2.41 1.84-2.41.86 0 1.26.63 1.26 1.44 0 .86-.57 2.09-.86 3.27-.17.98.52 1.84 1.52 1.84 1.78 0 3.16-1.9 3.16-4.58 0-2.4-1.72-4.04-4.19-4.04-2.82 0-4.48 2.1-4.48 4.31 0 .86.28 1.73.74 2.3.09.06.09.14.06.29l-.29 1.09c0 .17-.11.23-.28.11-1.28-.56-2.02-2.38-2.02-3.85 0-3.16 2.24-6.03 6.56-6.03 3.44 0 6.12 2.47 6.12 5.75 0 3.44-2.13 6.2-5.18 6.2-.97 0-1.92-.52-2.26-1.13l-.67 2.37c-.23.86-.86 2.01-1.29 2.7v-.03z"></path></svg>
                        </button>
                        <button id="ilw2u" class="button is-medium is-github">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="30px" height="30px"><path d="M16.42 18.42A57.5 57.5 0 0 0 15 13.17c.5-.07 1-.11 1.58-.11h.02c.93 0 1.95.12 3.06.37a7.788 7.788 0 0 1-3.24 4.99M12 19.8c-1.74 0-3.34-.57-4.64-1.54.28-.45.87-1.32 1.82-2.22.96-.93 2.32-1.89 4.05-2.46.59 1.67 1.13 3.57 1.54 5.71-.86.33-1.77.51-2.77.51M4.2 12v-.11c.22.01.51.01.85.01h.01c1.56-.01 4.3-.14 7.08-1.01.15.33.3.67.45 1.03-1.86.62-3.32 1.61-4.4 2.58-1.03.96-1.74 1.89-2.15 2.5a7.704 7.704 0 0 1-1.84-5m4.35-7c.55.65 1.63 2.06 2.79 4.25-2.34.71-4.73.87-6.16.87h-.13c-.24 0-.45 0-.62-.01C5 7.87 6.5 6 8.55 5M12 4.2c1.84 0 3.53.64 4.86 1.71C15.84 7.14 14.5 8 13.03 8.65 12 6.67 11 5.25 10.34 4.38c.54-.11 1.09-.18 1.66-.18m6.13 2.98a7.823 7.823 0 0 1 1.66 4.45 15.32 15.32 0 0 0-3.19-.35h-.01c-.8 0-1.55.07-2.26.19-.17-.42-.33-.82-.52-1.21 1.58-.69 3.09-1.68 4.32-3.08M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"></path></svg>
                        </button>
                    </div>
                    <div class="content has-text-left has-text-grey description" v-if="user.description" >
                        <p id="i93xf">
                            {{ user.description }}
                        </p>
                    </div>
                    <div class="container">
                        <h2 class="is-size-3 has-text-centered mt-5">Last Barters</h2>
                        <hr class="hr mx-auto has-text-centered">
                        <div class="columns is-multiline is-centered">
                            <!-- <div class="column is-4" v-for="barter in barters" v-bind:key="barter.id">
                                <div class="box is-shadowless has-border-grey has-background-white-bis">
                                    <span class="tag is-dark is-medium">{{ barter.name }}</span>
                                    <p class="is-size-6 mt-3 has-text-grey">
                                        {{ barter.description }}
                                    </p>
                                </div>
                            </div> -->
                            <div class="column is-6" v-for="barter in barters" v-bind:key="barter.id">
                                <div class="card">
                                    <div class="card-image">

                                        <figure v-if="getImageBarterURL(barter.id)" class="image is-4by3">
                                            <img :src="getImageBarterURL(barter.id)" alt="Placeholder image">
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
                </div>
                <br>
                <div class="has-text-centered">
                    <button @click="logout()" class="button is-danger">Log out</button>                
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'MyAccount',
    data() {
        return {
            user: {},
            barters: [],
            images: {}
        }
    },
    mounted() {
        this.getUser()
    },
    methods: {
        logout() {
            axios
                .post("/api/v1/token/logout/")
                .then(response => {
                    axios.defaults.headers.common["Authorization"] = ""
                    localStorage.removeItem("token")
                    this.$store.commit('removeToken')
                    this.$router.push('/')
                })
                .catch(error => {
                    if(error.response){
                        console.log(JSON.stringify(error.response.data))
                    }else if (error.message){
                        console.log(JSON.stringify(error.message))
                    }else{
                        console.log(JSON.stringify(error))
                    }
                })
        },
        getUser() {
            axios
                .get('/api/v1/users/me/')
                .then(response => {
                    this.user = response.data
                    this.getBarters(response)
                })
                .catch(error1 => {
                    console.log(JSON.stringify(error1))
                })
        },
        getBarters(user) {
            for(let i = 0; i < user.data['barters'].length; i++){
                axios
                    .get(`/api/v1/barters/${user.data['barters'][i]}`)
                    .then(response => {
                        this.barters.push(response.data)
                        if(response.data['images'][0]){
                            axios
                                .get(`/api/v1/images/${response.data['images'][0]}`)
                                .then(response2 => {
                                    var image = response2.data['image']
                                    const localhost = 'http://localhost:8000'
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
        getImageURL(image){
            if(this.user['image'] == '' || this.user['image'] == undefined){
                return ''
            }
            const localhost = "http://localhost:8000"
            return localhost.concat(image)
        },
        getImageBarterURL(index){
            return this.images[index]
        },
        getSmallImageURL(index){
            return this.images2[index]
        }
    },
}
</script>


<!-- TODO Faire en sorte qu'on puisse clicker sur les barters-->
