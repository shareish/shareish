<template>
    <div class="page-item">
        <div class="columns is-multiline">
            <div class="column is-full">
                <h1 class="title">{{ item.name }} {{ item.id }}</h1>
            </div>
            <div class="column is-half">
                <h2 class="subtitle">Details</h2>

                <div class="container" id="edit" v-if="id === item['user']">
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

                                        <button class="button is-success" @click="editItem()">Save changes</button>
                                    </div>
                                </div>
                            <button class="modal-close is-large" @click="closeEdit()">
                                Close
                            </button>
                        </div>
                    </div>


                    <button type="button"
                            class="button is-info" 
                            @click="showModal = true">Edit Item</button>
                </div>

                <p v-if="item.category1">{{ item.category1 }}</p>
                <p v-if="item.category2">{{ item.category2 }}</p>
                <p v-if="item.category3">{{ item.category3 }}</p>
                <p v-if="item.description">{{ item.description }}</p>
                <p v-if="item.location">{{ item.address }}</p>
                <!-- We could show the info in a more beautiful way and the location on a small map -->
            </div>
            <div class="column is-half">
                <figure class="image is-128x128">
                    <img :src="getImgUrl()">
                </figure>
            </div>
        </div>
    </div>

    <button class="button is-info" @click="beginConversation()" >Begin a conversation</button>

    <button class="button is-danger" @click="deleteItem()" >Delete</button>
    
</template>

<script>
import axios from 'axios'
export default {
    name: 'ItemDetail',
    data() {
        return {
            item: {},
            image: null,
            id: null,
            showModal: false,
            changes: {},
            files: ''
        }
    },
    async mounted() {
        await this.getItem()
        this.id = this.$store.state.user.id
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
                    alert('You cannot delete this item.')
                    console.log(JSON.stringify(error))
                })
        },
        async getItem() {
            console.log(this.$store.state.user.email)
            const itemID = this.$route.params.id
            await axios
                .get(`/api/v1/items/${itemID}`)
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
                    this.changes = Object.assign({}, this.item)
                    console.log(this.changes)
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        },
        editItem(){
            console.log(this.changes)
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
            console.log(formData)
            axios
                .post('api/v1/conversations/', formData)
                .then(response => {
                    console.log(response)
                    this.$router.push(`/dashboard/conversations/${response.data['id']}`)
                })
                .catch(error => {
                    console.log(error)
                })
        }
    },
}
</script>