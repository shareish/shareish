<template>
    <div class="page-add-item">
        <div class="columns is-multiline is-mobile">
            <div class="column is-4 is-responsive is-left">
                <h1 class="title is-responsive">Add item</h1>
            </div>
            <div class="column is-3 is-offset-2 is-right">
                <router-link to="/dashboard/autocomplete" class="button is-light is-medium is-responsive">Try autocomplete</router-link>
            </div>
            <div class="column is-3 is-right">
                <router-link to="/dashboard/recurrents" class="button is-light is-medium is-responsive">Recurrent Items</router-link>
            </div>
            <div id="imageError" class="column is-full is-responsive is-left" style="display: none;">
                <p class="is-danger">The size of the images is too big. The size of the images must be under 5 Mo.</p>
            </div>
            <div class="column is-two-thirds">
                <div class="field">
                    <label>Name of the article</label>
                    <div class="control">
                        <input type="text" class="input" name="name" v-model="item.name" required>
                    </div>
                </div>
            </div>
            <div class="column is-one-third">
                <div class="field">
                    <label>Type of the article</label>
                    <div class="control">
                        <div class="select">
                            <select name="type" id="type" v-model="item.item_type" required>
                                <option value="BR">Request</option>
                                <option value="DN">Donation</option>
                                <option value="LN">Loan</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
            <div class="column is-quarter">
                <div class="field">
                    <label>Category 1</label>
                    <div class="control">
                        <div class="select">
                            <select id="category1" name="category1" v-model="item.category1" required>
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
                </div>
            </div>
            <div class="column is-quarter">
                <div class="field">
                    <label>Category 2</label>
                    <div class="control">
                        <div class="select">
                            <select id="category2" name="category2" v-model="item.category2" required>
                                <option value="">--</option>
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
                </div>
            </div>
            <div class="column is-quarter">
                <div class="field">
                    <label>Category 3</label>
                    <div class="control">
                        <div class="select">
                            <select id="category3" name="category3" v-model="item.category3" required>
                                <option value="">--</option>
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
                </div>
            </div>
        </div>

        <div class="columns is-multiline">
            <div class="column is-one-third">
                <label>Images</label>
                <div class="field">
                    <div class="control">
                        <div class="file has-name is-fullwidth">
                            <label class="file-label">
                                <input class="file-input" type="file" accept="image/*" multiple @change="uploadFile">
                                <span class="file-cta">
                                    <span class="file-icon">
                                        <i class="fas fa-upload"></i>
                                    </span>
                                    <span class="file-label">
                                        Choose a file…
                                    </span>
                                </span>
                                <span class="file-name" v-if="files.length == 1">
                                    <div>
                                        {{ files[0].name }}
                                    </div>
                                </span>
                                <span class="file-name" v-if="files.length > 1">
                                    <div>
                                        {{ files[0].name }},...
                                    </div>
                                </span>
                            </label>
                        </div>
                    </div>
                </div>
                <p class="is-danger">The size of the images must be under 5Mo in total.</p>
            </div>
            <div class="column is-two-thirds">
                <div class="field">
                    <label>Address</label>
                    <div class="control">
                        <input type="text" class="input" name="location" v-model="item.location" required>
                    </div>
                    <p id="errorAddress" class="is-danger" style="display: none;">
                        The address is invalid, please indicate a new address.
                    </p>
                </div>
            </div>
            <div class="column is-half" v-if="item.images != undefined">
                <div v-for="image in getImgUrls()" v-bind:key="image.id">
                    <figure class="image is-256x256">
                        <img :src="image">
                    </figure>
                </div>
            </div>
            <figure class="column is-half" id="img-preview-auto"></figure>
            <figure class="column is-half" id="img-preview"></figure>
        </div>
        

        <div class="columns is-multiline">
            <div class="column is-two-third">
                <label for="descriptionItem">Description</label>
                <div class="field">
                    <div class="control">
                        <textarea class="textarea" maxlength="500" id="description" placeholder="Description..." name="description" v-model="item.description" required>
                        </textarea>
                    </div>
                </div>
            </div>
            <div class="column is-full is-centered is-vcentered">
                <label class="checkbox is-normal">
                    <input type="checkbox" name="is_recurrent" v-model="item.is_recurrent">
                    Recurrent Item
                </label>
            </div>

            <div class="column is-4 columns is-multiline">
                <label class="column is-full">Starting date</label>
                <input class="column is-4 m-2" type="date" v-model="item.startdate">
            </div>

            <div class="column is-4 columns is-multiline">
                <label class="column is-full">End date</label>
                <input class="column is-4 m-2" type="date" v-model="item.enddate">
            </div>

            <div class="column is-full">
                <div class="field">
                    <button class="button is-success" @click="submitForm">Submit</button>
                </div>
            </div>
        </div>
    </div>
    
</template>

<script>
import axios from 'axios';
import moment from 'moment';
export default {
    name: "AddItem",
    data() {
        return {
            item: {},
            files: {},
            fileauto: '',
            image: '',
            images: [],
        }
    },
    async mounted() {
        document.title = "Shareish | Add Item"
        if(this.$route.params.id){
            await this.getItem(this.$route.params.id)
            await this.getImages(this.item['images'])
        }
        if(this.$route.params.name){
            this.item['name'] = this.$route.params.name
            await this.loadImage()
            this.previewFile()
        }
    },
    methods: {
        async loadImage(){
            const blob = await (await fetch(this.$route.params.imgData)).blob()
            this.fileauto = new File([blob], 'autocomplete.jpg', )
        },
        async getItem(itemID){
            await axios
                .get(`/api/v1/items/${itemID}`)
                .then(async response => {
                    this.item = response.data
                    if(this.item['location'] != null){
                        await axios
                            .post('/api/v1/address/', this.item['location'])
                            .then(response3 => {
                                this.item['location'] = response3.data
                            })
                            .catch(error => {
                                console.log(JSON.stringify(error))
                            })
                    }
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        },
        async getImages(imagesIDs){
            for(let i = 0; i < imagesIDs.length; i++){
                await axios
                    .get(`/api/v1/images/${imagesIDs[i]}`)
                    .then(response => {
                        let name = response.data['image']
                        const localhost = 'https://' + window.location.hostname
                        this.images.push(localhost.concat(name))
                    })
                    .catch(error => {
                        console.log(error)
                    })
            }
        },
        uploadFile(event){
            let elem = document.getElementById('imageError')
            elem.style.display = "none"
            this.files = event.target.files
            this.flushPreviewFile()
            this.previewFiles()
        },
        async previewFile(){
            let imgPreview = document.getElementById("img-preview-auto");
            imgPreview.innerHTML = ''
            imgPreview.classList.add("image")
            imgPreview.classList.add("is-256x256")
            let fileReader = new FileReader()
            fileReader.readAsDataURL(this.fileauto)
            fileReader.addEventListener("load", function () {
                imgPreview.innerHTML += '<img src="' + this.result + '" />';
            });
        },
        async previewFiles(){
            let imgPreview = document.getElementById("img-preview");
            imgPreview.innerHTML = ''
            imgPreview.classList.add("image")
            imgPreview.classList.add("is-256x256")
            for(let i = 0; i < this.files.length; i++){
                let fileReader = new FileReader()
                fileReader.readAsDataURL(this.files[i])
                fileReader.addEventListener("load", function () {
                    imgPreview.innerHTML += '<img src="' + this.result + '" />';
                });
            }
        },
        flushPreviewFile(){
            let imgPreview = document.getElementById("img-preview");
            imgPreview.innerHTML = ''
            imgPreview = document.getElementById("img-preview-auto");
            imgPreview.innerHTML = ''
        },
        submitForm(){
            let eradd = document.getElementById('errorAddress')
            let elem = document.getElementById('imageError')
            eradd.style.display = 'none'
            elem.style.display = "none"
            this.item['in_progress'] = true
            if(this.item['startdate'] == undefined){
                this.item['startdate'] = moment().format('YYYY-MM-DD')
            }
            if(this.item['enddate']){
                if(this.item['enddate'] < this.item['startdate']){
                    alert('The end date is invalid.')
                    return false
                }
            }
            if(this.item['id'] != undefined){
                delete this.item['images']
                axios
                    .patch(`/api/v1/items/${this.item['id']}/`, this.item)
                    .then(response => {
                        if(Object.keys(this.files).length > 0){
                            this.item['id'] = response.data['id']
                            let formData = new FormData();
                            formData.append('itemID', this.item['id'])
                            for(let i = 0; i < Object.keys(this.files).length; i++){
                                let file = this.files[i];
                                formData.append('files', file);
                            }
                            axios
                                .post('/api/v1/images/', formData)
                                .catch(error => {
                                    if(error.response.status == 413){
                                        let elem = document.getElementById('imageError')
                                        elem.style.display = "block"
                                    }
                                    console.log(JSON.stringify(error));
                                });
                        }
                        this.flushPreviewFile()
                        this.$router.push('/dashboard/items')
                    })
                    .catch(error => {
                        if(error.response['data']['message'] && error.response['data']['message'] == "Bad location."){
                            eradd.style.display = 'block'
                        }
                        console.log(JSON.stringify(error))
                    })
            }else{
                this.item['images'] = []
                axios
                    .post('/api/v1/items/', this.item)
                    .then(response => {
                        if(Object.keys(this.files).length > 0 || this.fileauto != ''){
                            this.item['id'] = response.data['id']
                            let formData = new FormData();
                            formData.append('itemID', this.item['id'])
                            for(let i = 0; i < Object.keys(this.files).length; i++){
                                let file = this.files[i];
                                formData.append('files', file);
                            }
                            if(this.fileauto != ''){
                                formData.append('files', this.fileauto)
                            }
                            axios
                                .post('/api/v1/images/', formData)
                                .catch(error => {
                                    if(error.response.status == 413){
                                        let elem = document.getElementById('imageError')
                                        elem.style.display = "block"
                                    }
                                    console.log(JSON.stringify(error));
                                });
                        }
                        this.fileauto = ''
                        this.$router.push('/dashboard/items')
                    })
                    .catch(error => {
                        if(error.response.data.message && error.reponse.data.message == "Bad location."){
                            eradd.style.display = 'block'
                        }
                        console.log(JSON.stringify(error))
                    })
            }
            
        },
        getImgUrls(){
            return this.images
        },
    },
}
</script>

<style scoped>
.is-vcentered {
  display: flex;
  flex-wrap: wrap;
  align-content: center;
  align-items: center;
}
</style>