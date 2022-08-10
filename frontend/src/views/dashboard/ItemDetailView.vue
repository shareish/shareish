<template>
    <div class="page-item">
        <div class="columns is-multiline">
            <div class="column is-full">
                <h1 class="title">{{ item.name }}</h1>
            </div>
            <div class="column is-half">
                <div class="columns is-multiline">
                    <div class="container" id="edit" v-if="$store.state.user.id == item.user">
                        <div v-if="showModal">
                            <div class="modal is-active">
                                <div class="modal-background"></div>
                                    <div class="modal-content">
                                        <div class="box">
                                            <label class="label">Name</label>
                                            <p class="control has-icon has-icon-right">
                                                <input class="input" placeholder="Name..." type="text" v-model="changes.name">
                                            </p>
                                            <label class="label">Item type</label>
                                            <div class="control has-icon has-icon-right">
                                                <div class="select">
                                                    <select  v-model="changes.item_type">
                                                        <option value="BR">Request</option>
                                                        <option value="DN">Donation</option>
                                                        <option value="LN">Loan</option>
                                                    </select>
                                                </div>
                                            </div>

                                            <label class="label">Category 1</label>
                                            <div class="control has-icon has-icon-right">
                                                <div class="select">
                                                    <select v-model="changes.category1">
                                                        <option value="FD">Food</option>
                                                        <option value="AN">Animals</option>
                                                        <option value="EN">Arts and Entertainments</option>
                                                        <option value="CL">Collectors</option>
                                                        <option value="HL">Helping hand</option>
                                                        <option value="DY">DIY</option>
                                                        <option value="BT">Beauty and Well-being</option>
                                                        <option value="CH">Childhood</option>
                                                        <option value="IT">IT and Multimedia</option>
                                                        <option value="GD">Garden</option>
                                                        <option value="HS">House</option>
                                                        <option value="HD">Holidays and Week-end</option>
                                                        <option value="BK">Books, CDs and DVDs</option>
                                                        <option value="SP">Sport and Leisure</option>
                                                        <option value="TS">Transport and vehicle</option>
                                                        <option value="OT">Other</option>
                                                    </select>
                                                </div>
                                            </div>

                                            <label class="label">Category 2</label>
                                            <div class="control has-icon has-icon-right">
                                                <div class="select">
                                                    <select v-model="changes.category2">
                                                        <option value="FD">Food</option>
                                                        <option value="AN">Animals</option>
                                                        <option value="EN">Arts and Entertainments</option>
                                                        <option value="CL">Collectors</option>
                                                        <option value="HL">Helping hand</option>
                                                        <option value="DY">DIY</option>
                                                        <option value="BT">Beauty and Well-being</option>
                                                        <option value="CH">Childhood</option>
                                                        <option value="IT">IT and Multimedia</option>
                                                        <option value="GD">Garden</option>
                                                        <option value="HS">House</option>
                                                        <option value="HD">Holidays and Week-end</option>
                                                        <option value="BK">Books, CDs and DVDs</option>
                                                        <option value="SP">Sport and Leisure</option>
                                                        <option value="TS">Transport and vehicle</option>
                                                        <option value="OT">Other</option>
                                                    </select>
                                                </div>
                                            </div>

                                            <label class="label">Category 3</label>
                                            <div class="control has-icon has-icon-right">
                                                <div class="select">
                                                    <select v-model="changes.category3">
                                                        <option value="FD">Food</option>
                                                        <option value="AN">Animals</option>
                                                        <option value="EN">Arts and Entertainments</option>
                                                        <option value="CL">Collectors</option>
                                                        <option value="HL">Helping hand</option>
                                                        <option value="DY">DIY</option>
                                                        <option value="BT">Beauty and Well-being</option>
                                                        <option value="CH">Childhood</option>
                                                        <option value="IT">IT and Multimedia</option>
                                                        <option value="GD">Garden</option>
                                                        <option value="HS">House</option>
                                                        <option value="HD">Holidays and Week-end</option>
                                                        <option value="BK">Books, CDs and DVDs</option>
                                                        <option value="SP">Sport and Leisure</option>
                                                        <option value="TS">Transport and vehicle</option>
                                                        <option value="OT">Other</option>
                                                    </select>
                                                </div>
                                            </div>

                                            <label class="label">Description</label>
                                            <p class="control">
                                                <textarea class="textarea" placeholder="Describe the item!" maxlength="500" v-model="changes.description">

                                                </textarea>
                                            </p>

                                            <label>Address</label>
                                            <div class="control has-icon has-icon-right">
                                                <input type="text" class="input" placeholder="Address..." v-model="changes.address">
                                            </div>

                                            <label>Images</label>
                                            <div class="field">
                                                <div class="control">
                                                    <div class="file has-name is-fullwidth">
                                                        <label class="file-label">
                                                            <input class="file-input" type="file" accept="image/*" multiple @change="uploadImage">
                                                            <span class="file-cta">
                                                            <span class="file-icon">
                                                                <i class="fas fa-upload"></i>
                                                            </span>
                                                            <span class="file-label">
                                                                Choose a file… (The previous images will be kept with the new ones)
                                                            </span>
                                                            </span>
                                                        </label>
                                                    </div>
                                                </div>
                                            </div>

                                            <label>Recurrent item</label>
                                            <div class="control">
                                                <input type="checkbox" name="is_recurrent" v-model="changes.is_recurrent">
                                            </div>

                                            <label>Start date</label>
                                            <div class="control">
                                                <input class="column is-4 m-2" type="date" v-model="changes.startdate">
                                            </div>

                                            <label>End date</label>
                                            <div class="control">
                                                <input class="column is-4 m-2" type="date" v-model="changes.enddate">
                                            </div>

                                            <button class="button is-success" @click="editItem()">Save changes</button>
                                        </div>
                                    </div>
                                <button class="modal-close is-large" @click="closeEdit()">
                                    Close
                                </button>
                            </div>
                        </div>                   
                    </div>
                    
                    <div class="column is-full" v-if="$store.state.user.id == item.user">
                        <button type="button" class="button is-info" @click="showModal = true">
                            Edit Item
                        </button>
                    </div>

                    <div class="column box is-full m-2">
                        <label class="subtitle">Description</label>
                        <p v-if="item.description">{{ item.description }}</p>
                        <p v-else>None were given.</p>
                    </div>

                    <div class="column box is-full m-2">
                        <div class="columns is-multiline">
                            <div class="column is-full">
                                <label class="subtitle">Categories</label>
                            </div>

                            <div class="column is-third">
                                <p v-if="item.category1">{{ item.category1 }}</p>
                                <p v-else>None were given.</p>
                            </div>

                            <div class="column is-third">
                                <p v-if="item.category2">{{ item.category2 }}</p>
                            </div>

                            <div class="column is-third">
                                <p v-if="item.category3">{{ item.category3 }}</p>
                            </div>
                        </div>
                    </div>

                    <div class="column box is-full m-2">
                        <label class="subtitle">Location</label>
                        <p v-if="item.location">{{ item.address }}</p>
                        <p v-else>None were given.</p>
                    </div>

                    <div class="column is-full box m-2">
                        <div class="columns is-multiline">
                            <label class="column is-full subtitle">Disponibility</label>
                            <p class="column is-6">From {{ item.startdate }}</p>
                            <p class="column is-6" v-if="item.enddate">To {{ item.enddate }}</p>
                            <p class="column is-6" v-else>No end date communicated</p>
                        </div> 
                    </div>

                    <div class="column is-full box m-2">
                        <label class="sutitle">Owner</label>
                        <br>
                        <div class="columns is-multiline">
                            <router-link v-if="item.user !== undefined" :to="{ name: 'userDetail', params: { id: item.user }}" class="column is-3 ml-5">
                                <figure v-if="getSmallImageURL()" class="image is-96x96">
                                    <img class="is-rounded" :src="getSmallImageURL()" alt="Placeholder image">
                                </figure>
                                <figure class="image is-inline-block is-responsive is-96x96" v-else>
                                    <img class="is-rounded" src="https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg">
                                </figure>
                            </router-link>
                            <p class="column is-offset3 is-6 is-vcentered">{{ userName }}</p>
                        </div>
                        <div class="column is-full"></div>
                    </div>
                </div>
                
                <!-- We could show the info in a more beautiful way and the location on a small map -->
            </div>
            <div class="column is-third is-offset-3">
                <figure class="image is-256x256">
                    <img :src="getImgUrl()">
                </figure>
            </div>
        </div>
    </div>

    <div class="columns is-multiline">
        <div class="column is-3 m-2">
            <button class="button is-info" @click="beginConversation()" >Begin a conversation</button>

        </div>
        <div v-if="item.is_recurrent && item.user == $store.state.user.id">
            <div class="column is-3 is-offset-3 m-2">
                <button class="button is-danger" @click="removeItem()" >Remove recurrent Item</button>  
            </div>
            <div class="column is-3 is-offset-3 m-2">
                <button class="button is-danger" @click="deleteItem()" >Delete Item</button>  
            </div>
        </div>
        <div v-else>
            <div class="column is-3 is-centered m-2" v-if="item.user == $store.state.user.id">
                <button class="button is-danger" @click="deleteItem()" >Delete Item</button>  
            </div>
        </div>
        
    </div>

    
</template>

<script>
import axios from 'axios'
export default {
    name: 'ItemDetail',
    data() {
        return {
            item: {},
            image: null,
            showModal: false,
            changes: {},
            files: '',
            userImage: null,
            userName: '',
        }
    },
    async mounted() {
        await this.getItem()
    },
    methods: {
        getImgUrl(){
            return this.image
        },
        deleteItem(){
            axios
                .delete(`/api/v1/items/${this.item['id']}/`)
                .then(response => {
                    this.$router.push('/dashboard/items')
                })
                .catch(error => {
                    alert('You cannot delete this item.')
                    console.log(JSON.stringify(error))
                })
        },
        removeItem(){
            this.item['in_progress'] = false
            const formData = new FormData()
            formData.append('in_progress', false)
            axios
                .patch(`/api/v1/recurrents/${this.item['id']}/`, formData)
                .then(response => {
                    this.$router.push('/dashboard/items')
                })
                .catch(error => {
                    alert('You cannot delete this item.')
                    console.log(JSON.stringify(error))
                })
        },
        async getItem() {
            const itemID = this.$route.params.id
            await axios
                .get(`/api/v1/items/${itemID}/`)
                .then(async response => {
                    this.item = response.data
                    if(this.item['images'][0]){
                        await axios
                        .get(`/api/v1/images/${this.item['images'][0]}`)
                        .then(response2 => {
                            this.image = response2.data['image']
                            const localhost = 'http://localhost:8000'
                            this.image = localhost.concat(this.image)
                        })
                        .catch(error => {
                            console.log(JSON.stringify(error))
                        })
                    }
                    if(this.item['location'] != null){
                        await axios
                            .post('/api/v1/address/', this.item['location'])
                            .then(response3 => {
                                this.item['address'] = response3.data
                            })
                            .catch(error => {
                                console.log(JSON.stringify(error))
                            })
                    }
                    await this.getUserImage()
                    this.changes = Object.assign({}, this.item)
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
            console.log(this.item['user'])
        },
        async getUserImage(){
            await axios
                    .get((`/api/v1/users/${this.item['user']}/`))
                    .then(response => {
                        if(response.data['image']){
                            this.userImage = response.data['image']
                        }
                        this.userName = response.data['email'] + ' (' + response.data['username'] + ')'
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })
        },
        getSmallImageURL(){
            return this.userImage
        },
        editItem(){
            if(this.changes['startdate'] == undefined){
                this.changes['startdate'] = moment().format('YYYY-MM-DD')
            }
            if(this.changes['enddate']){
                if(this.changes['enddate'] < this.changes['startdate']){
                    alert('The end date is invalid.')
                    this.closeEdit()
                    return false
                }
            }
            let address = ''
            if("address" in this.changes){
                address = this.changes["address"]
                this.changes["location"] = address
                delete this.changes["address"]  
            }
            axios
                .put(`/api/v1/items/${this.item['id']}/`, this.changes)
                .then(response => {
                    if(Object.keys(this.files).length > 0){
                        let formData = new FormData();
                        formData.append('itemID', this.item['id'])
                        for( var i = 0; i < this.files.length; i++ ){
                            let file = this.files[i];
                            formData.append('files', file);
                        }
                        axios
                            .post('/api/v1/images/', formData)
                            .catch(error => {
                                console.log(JSON.stringify(error));
                            });   
                    }
                    this.showModal = false
                    this.item = response.data
                    this.item["address"] = address
                    this.changes = Object.assign({}, this.item)
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        },
        closeEdit(){
            this.changes = Object.assign({}, this.item)
            this.showModal = false
        },
        uploadImage(event){
            this.files = event.target.files;
        },
        beginConversation(){
            if(this.item['user'] == this.$store.state.user.id){
                alert('You cannot begin a conversation with yourself.')
                return false
            }
            const formData = {
                'name': "" + this.item['id'] + this.item['user'] + this.$store.state.user.id,
                'owner': this.item['user'],
                'buyer': this.$store.state.user.id,
                'messages': [],
            }
            axios
                .post('api/v1/conversations/', formData)
                .then(response => {
                    this.$router.push(`/dashboard/conversations/${response.data['id']}`)
                })
                .catch(error => {
                    console.log(error)
                })
        }
    },
}
</script>

<style scoped>
.is-vcentered {
  display: flex;
  flex-wrap: wrap;
  align-content: center; /* used this for multiple child */
  align-items: center; /* if an only child */
}
</style>