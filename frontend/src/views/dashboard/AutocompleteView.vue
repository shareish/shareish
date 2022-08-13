<template>
    <h1 class="title">
        Autocomplete adder
    </h1>
    <h2 class="subtitle">
        Insert your image here:
    </h2>
    <label>Images</label>
    <div class="field">
        <div class="control">
            <div class="file has-name is-fullwidth">
                <label class="file-label">
                    <input class="file-input" type="file" accept="image/*" @change="uploadFile">
                    <span class="file-cta">
                        <span class="file-icon">
                            <i class="fas fa-upload"></i>
                        </span>
                        <span class="file-label">
                            Choose a file…
                        </span>
                    </span>
                    <span class="file-name" v-if="file.length == 1">
                        <div>
                            {{ file[0].name }}
                        </div>
                    </span>
                </label>
            </div>
        </div>
    </div>
    <div class="field">
        <button class="button is-success" @click="submitForm">Submit</button>
    </div>
</template>

<script>
import axios from 'axios'
import imagefinder from "../../assets/imagefinder.json"
export default {
    name: 'Autocomplete',
    data() {
        return {
            file: "",
        }
    },
    methods: {
        uploadFile(event){
            this.file = event.target.files
            console.log(this.file)
        },
        submitForm(){
            // With more time I could have linked every outputs of ImageNet dataset to one of my categories and I could propose a category on top of a name.
            // TODO Pass the image to AddItem => BUG
            
            axios
                .post('/api/v1/predictClass/', this.file)
                .then(response => {
                    this.$router.push({ name: 'addItem', params: { name: response.data}})
                })
                .catch(error => {
                    console.log(error)
                })
        },
    },
}
</script>