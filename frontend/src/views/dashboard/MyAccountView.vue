<template>
    <div class="page-my-account">
        <h1 class="title has-text-centered">My Account</h1>

        <div class="columns is-centered is-multiline">
            <div class="column is-6 p-3 has-text-centered">
                <figure class="image is-inline-block is-responsive is-512x512" v-if="getImageURL(user.image)">
                    <img id="profilPicture" :src="getImageURL()" class="is-rounded">
                </figure>
                <figure class="image is-inline-block is-responsive is-96x96" v-else>
                    <img src="https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg">
                </figure>
                <div class="tile mt-5 pt-5 is-child pink card-bio">
                    <h2 id="isse" class="title pt-5 is-2 name">Hi, I'm {{ user.first_name }} {{ user.last_name }} (AKA {{ user.username }})</h2>
                    <p>{{ user.description }}</p>
                    <hr class="hr mx-auto has-text-centered">
                    <div class= "container" id="edit">
                        <div class="modal" id="modal">
                            <div class="modal-background"></div>
                            <div class="modal-card" style="height: 80%;">
                                <header class="modal-card-head">
                                    <p class="modal-card-title">Edit Profil</p>
                                    <button class="delete" aria-label="close" @click="closeEdit"></button>
                                </header>
                                <div class="modal-card-body">
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
                                    </div>
                                </div>
                                <footer class="modal-card-foot">
                                    <button class="button is-success" @click="editProfil()">Save changes</button>
                                </footer>
                            </div>
                        </div>

                        <div class="columns is-centered">
                            <button type="button" class="column p-2 is-3 button is-info" @click="openModal">Edit profil</button>
                            <button @click="logout()" class="button column p-2 is-3 is-offset-3 is-danger">Log out</button>
                        </div>
                        
                        <div class="has-text-centered">
                                            
                        </div>        
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
    name: 'MyAccount',
    data() {
        return {
            user: {},
            items: [],
            images: {},
            userImage: '',
            changes: {},
            files: '',
            newImage: '',
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
        async getUser() {
            await axios
                .get(`/api/v1/users/me/`)
                .then(async response => {
                    this.user = Object.assign({}, response.data)
                    this.changes = Object.assign({}, response.data)
                    await this.getItems()
                    await this.getImage()
                })
                .catch(error1 => {
                    console.log(JSON.stringify(error1))
                })
        },
        async getItems() {
            await axios
                .get('/api/v1/user_items/')
                .then(response => {
                    this.items = response.data
                    for(let i = 0; i < this.items.length; i++){
                        if(this.items[i]['images'][0]){
                            axios
                                .get(`/api/v1/images/${this.items[i]['images'][0]}`)
                                .then(response2 => {
                                    var image = response2.data['image']
                                    const localhost = 'http://' + window.location.hostname
                                    image = localhost.concat(image)
                                    this.images[this.items[i]['id']] = image
                                })
                                .catch(error2 => {
                                    console.log(JSON.stringify(error2))
                                })
                        }
                    }
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        },
        async getImage(){
            if(this.user['image'][0]){
                await axios
                .get(`/api/v1/user_image/${this.user['image'][0]}/`)
                .then(response => {
                    console.log(response.data['image'])
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
        getImageURL(){
            return this.userImage
        },
        getImageItemURL(index){
            return this.images[index]
        },
        getSmallImageURL(index){
            return this.imaes2[index]
        },
        async editProfil(){
            const formData = {
                email: this.changes['email'],
                password: this.changes['password'],
                username: this.changes['username'],
                first_name: this.changes['first_name'],
                last_name: this.changes['last_name'],
                description: this.changes['description'],
            }

            // axios
            //     .patch(`/api/v1/users/me/`, formData)
            //     .then(response => {
            //         this.user = response.data
            //         this.closeEdit()
            //     })
            //     .catch(error => {
            //         console.log(error)
            //     })

            //Faire une nouvelle fonction qui fait office de vue pour delete les images liées à l'utilisateur
            if(this.newImage != ''){
                for(let i = 0; i < this.user['image'].length; i++){
                    axios
                        .delete(`/api/v1/user_image/${this.user['image'][i]}/`)
                        .catch(error => {
                            console.log(error)
                        })
                }
                
            }
            
            this.user['image'] = []
            await axios
                .patch('/api/v1/users/me/', formData)
                .then(response => {
                    this.user = response.data
                    if(this.newImage != ''){
                        const formData2 = new FormData();
                        formData2.append('userID', this.user['id'])
                        for(let i = 0; i < this.newImage.length; i++){
                            let file = this.newImage[i];
                            formData2.append('image', file);
                        }
                        axios
                            .post('/api/v1/user_image/', formData2)
                            .then(async response2 => {
                                let image = response2.data['image']
                                const localhost = 'http://' + window.location.hostname
                                image = localhost.concat(image)
                                this.userImage = image
                                await this.getImage()
                                document.getElementById("profilPicture").src = this.getImageURL()
                                console.log(this.getImageURL())
                            })
                            .catch(error => {
                                console.log(JSON.stringify(error));
                            });
                    }
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
            this.closeEdit()
        },
        openModal(){
            let elem = document.getElementById("modal")
            elem.classList.add("is-active")
        },
        closeEdit(){
            this.changes = Object.assign({}, this.user)
            let elem = document.getElementById("modal")
            elem.classList.remove("is-active")
        },
        uploadImage(event){
            this.newImage = event.target.files
        },
        getImageURLDefault(category){
            return imagefinder[category]
        },
    },
}
</script>

<!-- TODO Améliorer le style et le nombre de fields qu'on peut changer dans le modal mais sinon c'est bieng-->
