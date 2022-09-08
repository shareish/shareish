<template>
    <div class="page-my-account">
        <h1 class="title has-text-centered">My Account</h1>

        <div id="notif" class="is-centered notification is-success is-light" style="display: none;">
            <button class="delete" @click="hideNotification()"></button>
            Profile succesfully edited.
        </div>

        <div class="columns is-centered is-multiline">
            <div class="column is-6 p-3 has-text-centered">
                <figure class="image is-inline-block is-responsive is-512x512" v-if="userImage">
                    <img id="profilPicture" :src="userImage" class="is-rounded">
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
                                    <p class="modal-card-title">Edit Profile</p>
                                    <button class="delete" aria-label="close" @click="closeEdit"></button>
                                </header>
                                <div class="modal-card-body">
                                    <div class="box">
                                        <p id="errorLog" class="is-danger" style="display: none;">
                                            The changes applied are not valid.
                                        </p>
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
                                                            Choose a profile picture...
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
                            <button type="button" class="column p-2 is-3 button is-info" @click="openModal">Edit profile</button>
                            <button @click="logout()" class="button column p-2 is-3 is-offset-3 is-danger">Log out</button>
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
                                        <figure v-else class="image is-4by3">
                                        <img :src="require('@/assets/categories/' + getImageURLDefault(item.category1))" alt="Placeholder image">
                                        </figure>
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
            userImage: null,
            changes: {},
            files: '',
            newImage: '',
        }
    },
    mounted() {
        document.title = "Shareish | My Account"
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
            try {
                this.items = (await axios.get('/api/v1/user_items/')).data;
                for (const item of this.items) {
                    if (item['images'].length > 0) {
                        try {
                            const uri = `/api/v1/images/${item['images'][0]}`;
                            this.images[item['id']] = (await axios.get(uri)).data['url'];
                        }
                        catch (error) {
                            console.log(JSON.stringify(error))
                        }
                    }
                }
            }
            catch (error) {
                console.log(JSON.stringify(error))
            }
        },
        async getImage(){
            if(this.user['image'].length > 0){
              try {
                const uri = `/api/v1/user_image/${this.user['image'][0]}/`;
                const data = (await axios.get(uri)).data;
                this.userImage = data['url'];
              }
              catch(error) {
                  console.log(error)
              }
            }
        },
        getImageItemURL(index){
            return this.images[index]
        },
        getSmallImageURL(index){
            return this.imaes2[index]
        },
        async editProfil(){
            let logAlert = document.getElementById("errorLog")
            logAlert.style.display = 'none'
            const formData = {
                email: this.changes['email'],
                password: this.changes['password'],
                username: this.changes['username'],
                first_name: this.changes['first_name'],
                last_name: this.changes['last_name'],
                description: this.changes['description'],
            }

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
                            .then(response2 => {
                                this.userImage = response2.data['url']
                            })
                            .catch(error => {
                                console.log(JSON.stringify(error));
                            });
                    }
                    this.showNotification()
                    this.closeEdit()
                })
                .catch(error => {
                    logAlert.style.display = 'block'
                    console.log(JSON.stringify(error))
                })
        },
        openModal(){
            let elem = document.getElementById("modal")
            elem.classList.add("is-active")
            this.hideNotification()
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
        hideNotification(){
            let elem = document.getElementById('notif')
            elem.style.display = "none"
        },
        showNotification(){
            let elem = document.getElementById('notif')
            elem.style.display = "block"
        },
    },
}
</script>
