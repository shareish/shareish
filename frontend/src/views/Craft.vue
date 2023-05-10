<template>
    <div class="file is-boxed is-large">
      <label class="file-label">
        <input accept="image/*" :v-model="file" class="file-input" type="file" @change="uploadFile">
        <span class="file-cta">
          <span class="file-icon"><i class="fas fa-upload"></i></span>
          <span class="file-label">Choose a file…</span>
        </span>
        <span v-if="file" class="file-name">{{ file.name }}</span>
      </label>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  export default {
    name: "Craft",
    data() {
      return {
        file: null,
        filePreview: null
      }
    },
    methods: {
      async uploadFile(event) {
        this.loading = true;
        this.file = event.target.files[0];
        const reader = new FileReader();
        reader.addEventListener('load', (event) => {
          this.filePreview = event.target.result
        });
        reader.readAsDataURL(this.file);
        await this.fetchPredictions();
        this.name = this.suggestedName;
        this.category1 = this.suggestedCategory;
        this.description = this.suggestedDescription;
        this.step = 2;
        this.loading = false;
      },
      async fetchPredictions() {
        try {
          let data = new FormData();
          data.append('image', this.file);
          const response = (await axios.post("/api/v1/analyze/", data)).data;
          console.log(response);
        }
        catch (error) {
          this.snackbarError(error);
        }
      }
    }
  }
  </script>
  