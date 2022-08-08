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
                    <h2 id="isse" class="title pt-5 is-2 name">Hi, I'm {{ user.first_name }} {{ user.last_name }} (AKA {{ user.username }})</h2>
                    <p>{{ user.description }}</p>
                    <hr class="hr mx-auto has-text-centered">
                    <div class= "container" id="edit">
                        <div v-if="showModal">
                            <div class="modal is-active">
                                <div class="modal-background"></div>
                                    <div class="modal-content">
                                        <div class="box">
                                            <label class="label">Username</label>
                                            <p class="control has-icon has-icon-right">
                                                <input class="input" placeholder="Username..." type="text" v-model="changes.username">
                                            </p>
                                            <label class="label">Email</label>
                                            <p class="control has-icon has-icon-right">
                                                <input class="input" placeholder="Email..." type="email" v-model="changes.email">
                                            </p>
                                            <label class="label">First Name</label>
                                            <p class="control has-icon has-icon-right">
                                                <input class="input" placeholder="First Name..." type="text" v-model="changes.first_name">
                                            </p>
                                            <label class="label">Last Name</label>
                                            <p class="control has-icon has-icon-right">
                                                <input class="input" placeholder="Last Name..." type="text" v-model="changes.last_name">
                                            </p>
                                            <label class="label">Description</label>
                                            <p class="control">
                                                <textarea class="textarea" placeholder="Describe Yourself!" maxlength="300" v-model="changes.description">

                                                </textarea>
                                            </p>
                                            <label>Images</label>
                                            <div class="field">
                                                <div class="control">
                                                    <div class="file has-name is-fullwidth">
                                                        <label class="file-label">
                                                            <input class="file-input" type="file" accept="image/*" @change="uploadImage">
                                                            <span class="file-cta">
                                                            <span class="file-icon">
                                                                <i class="fas fa-upload"></i>
                                                            </span>
                                                            <span class="file-label">
                                                                Choose a profil picture...
                                                            </span>
                                                            </span>
                                                        </label>
                                                    </div>
                                                </div>
                                            </div>
                                            <button class="button is-success" @click="editProfil()">Save changes</button>
                                        </div>
                                    </div>
                                <button class="modal-close is-large" @click="closeEdit()">
                                    Close
                                </button>
                            </div>
                        </div>


                        <button type="button"
                                class="button is-info" 
                                @click="showModal = true">Edit profil</button>
                    </div>

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
                                            No content Image
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
            items: [],
            images: {},
            showModal: false,
            changes: {},
            files: '',
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
                    this.$store.commit('removeUserID')
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
                .get(`/api/v1/users/me/`)
                .then(response => {
                    this.user = Object.assign({}, response.data)
                    this.changes = Object.assign({}, response.data)
                    console.log(response.data)
                    this.getItems(response)
                })
                .catch(error1 => {
                    console.log(JSON.stringify(error1))
                })
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
            return image
        },
        getImageItemURL(index){
            return this.images[index]
        },
        getSmallImageURL(index){
            return this.images2[index]
        },
        editProfil(){
            const formData = {
                email: this.changes['email'],
                password: this.changes['password'],
                username: this.changes['username'],
                first_name: this.changes['first_name'],
                last_name: this.changes['last_name'],
                image: this.changes['image'],
            }
            axios
                .patch(`/api/v1/users/me/`, formData)
                .then(response => {
                    this.showModal = false
                    this.user = response.data
                })
                .catch(error => {
                    console.log(error)
                })
        },
        closeEdit(){
            this.changes = Object.assign({}, this.user)
            this.showModal = false
        },
        uploadImage(event){
            this.changes['image'] = event.target.files;
        },
    },
}
</script>

<!-- TODO Améliorer le style et le nombre de fields qu'on peut changer dans le modal mais sinon c'est bieng-->
