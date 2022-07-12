<template>
    <div class="page-add-barter">
        <div class="columns is-multiline is-mobile">
            <div class="column is-full">
                <h1 class="title">Add barter</h1>
            </div>
            <div class="column is-two-thirds">
                <div class="field">
                    <label>Name of the article</label>
                    <div class="control">
                        <input type="text" class="input" name="name" v-model="barter.name" required>
                    </div>
                </div>
                <!-- And keep going with the form -->
            </div>
            <div class="column is-one-third">
                <div class="field">
                    <label>Type of the article</label>
                    <div class="control">
                        <div class="select">
                            <select name="type" id="type" v-model="barter.barter_type" required>
                                <option value="BR">Barter</option>
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
                            <select id="category1" name="category1" v-model="barter.category1" required>
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
                            <select id="category2" name="category2" v-model="barter.category2" required>
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
                            <select id="category3" name="category3" v-model="barter.category3" required>
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

        <div class="columns">
            <div class="column is-half">
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
                            </label>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        

        <div class="columns is-multiline">
            <div class="column is-two-third">
                <label for="descriptionBarter">Description</label>
                <div class="field">
                    <div class="control">
                        <textarea class="textarea" maxlength="500" id="description" placeholder="Description..." name="description" v-model="barter.description" required>
                        </textarea>
                    </div>
                </div>
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
import axios from 'axios'
export default {
    name: "AddBarter",
    data() {
        return {
            barter: {},
            images: '',
        }
    },
    mounted() {
        
    },
    methods: {
        uploadFile(event){
            this.files = event.target.files;
        },
        submitForm(){
            this.barter['images'] = []
            axios
                .post('/api/v1/barters/', this.barter)
                .then(response => {
                    this.barter['id'] = response.data['id']
                    let formData = new FormData();
                    formData.append('barterID', this.barter['id'])
                    for( var i = 0; i < this.files.length; i++ ){
                        let file = this.files[i];
                        formData.append('files', file);
                    }
                    axios
                        .post('/api/v1/images/', formData)
                        .then(response => {
                            this.$router.push('/dashboard/barters')
                        })
                        .catch(error => {
                            console.log(JSON.stringify(error));
                        });
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        }
    },
}
</script>