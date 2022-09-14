<template>
<div class="page-add-item">
  <h1 class="title">{{$t('add-new-item')}}</h1>
  <b-loading :active="loading" :is-full-page="false" />
  <template v-if="step === 1">
    <h2 class="subtitle">{{$t('upload-your-item-image')}}</h2>
    <div class="container has-text-centered centered-container">
        <div class="file is-boxed is-large">
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
            <span class="file-name" v-if="file && file.length === 1">
                {{ file[0].name }}
            </span>
          </label>
      </div>
    </div>
  </template>
  <template v-else-if="step === 2">
    <section>
      <b-field :label="$t('name')">
        <b-input v-model="name" />
      </b-field>
      <b-field :label="$t('item-type')">
        <b-select v-model="type" expanded>
          <option value="BR">{{ $t('request') }}</option>
          <option value="DN">{{ $t('donation') }}</option>
          <option value="LN">{{ $t('loan') }}</option>
        </b-select>
      </b-field>
      <div class="columns">
        <category-selector class="column" number="1" v-model="category1" :nullable="false" expanded/>
        <category-selector class="column" number="2" v-model="category2" :nullable="false" expanded/>
        <category-selector class="column" number="3" v-model="category3" :nullable="false" expanded/>
      </div>
      <b-field :label="$t('address')">
        <b-input v-model="location" />
      </b-field>
      <b-field :label="$t('description')">
        <b-input type="textarea" expanded v-model="description" />
      </b-field>

    </section>
  </template>
  <template v-else>
    <div class="container has-text-centered buttons centered-container">
      <button class="button is-primary is-large" @click="step = 1">{{$t('i-have-image')}}</button>
      <button class="button is-primary is-large is-outlined" @click="step = 2">{{$t('i-do-not-have-image')}}</button>
    </div>
    <recurrent-items-list />
  </template>
</div>
</template>

<script>
import RecurrentItemsList from '@/components/RecurrentItemsList';
import axios from 'axios';
import CategorySelector from '@/components/CategorySelector';
export default {
  name: 'AddItem',
  components: {CategorySelector, RecurrentItemsList},
  data() {
    return {
      loading: false,
      step: 0,

      file: null,
      filePreview: null,

      suggestedName: null,
      suggestedDescription: null,

      name: '',
      description: '',
      type: null,
      category1: null,
      category2: null,
      category3: null,
      location: '',

      isRecurrent: false,
      startDate: null,
      endDate: null
    }
  },
  watch: {
  },
  methods: {
    async uploadFile(event) {
      this.loading = true;

      this.file = event.target.files;
      const reader = new FileReader();
      reader.addEventListener('load', (event) => {
        this.filePreview = event.target.result
      });
      reader.readAsDataURL(this.file[0]);
      await this.fetchPredictions();

      this.name = this.suggestedName;
      this.description = this.suggestedDescription;
      this.step = 2;
      this.loading = false;
    },
    async fetchPredictions() {
      try {
        const predictions = (await axios.post('/api/v1/predictClass/', this.file)).data;
        this.suggestedName = predictions['suggested_class'];
        this.suggestedDescription = predictions['detected_text'];
      }
      catch (error) {
        console.log(error);
      }
    }
  }
};
</script>

<style scoped>
.centered-container, .file {
  justify-content: center;
}
</style>