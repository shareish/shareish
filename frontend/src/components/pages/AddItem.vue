<template>
<div class="page-add-item">
  <h1 class="title">{{$t('add-new-item')}} <b-tooltip position="is-bottom" :label="$t('help_add_item')" multilined> <i class="icon far fa-question-circle"></i> </b-tooltip></h1>
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
    <div class="columns">
      <section class="column is-four-fifths">
        <b-field>
	  <template #label>{{$t('name')}}
	  <b-tooltip position="is-right" :label="$t('help_item_name')" multilined><i class="icon far fa-question-circle"></i></b-tooltip></template>
          <b-input v-model="name" />
        </b-field>

	<b-field>
	  <template #label>{{$t('item-type')}}
	  <b-tooltip position="is-right" :label="$t('help_item_type')" multilined><i class="icon far fa-question-circle"></i></b-tooltip></template>
          <b-select v-model="type" expanded>
            <option value="BR">{{ $t('request') }}</option>
            <option value="DN">{{ $t('donation') }}</option>
            <option value="LN">{{ $t('loan') }}</option>
	    <option value="EV">{{ $t('event') }}</option>
          </b-select>
        </b-field>

	<div class="columns">
	  <b-tooltip position="is-right" :label="$t('help_item_category')" multilined>
          <category-selector class="column" :number="1" v-model="category1" :nullable="false" expanded/>
          <category-selector class="column" :number="2" v-model="category2" :nullable="false" expanded/>
          <category-selector class="column" :number="3" v-model="category3" :nullable="false" expanded/>
	  </b-tooltip>
        </div>
        <b-field>
	  <template #label>{{$t('address')}}
	  <b-tooltip position="is-right" :label="$t('help_item_address')" multilined> <i class="icon far fa-question-circle"></i></b-tooltip></template>
          <b-input v-model="location" />
        </b-field>
        <b-field>
	  <template #label> {{$t('description')}}
	  <b-tooltip position="is-right" :label="$t('help_item_description')" multilined> <i class="icon far fa-question-circle"></i></b-tooltip></template>
          <b-input type="textarea" expanded v-model="description" />
        </b-field>
        <b-field grouped>
          <b-field expanded>
	    <template #label> {{$t('start-date')}}
	      <b-tooltip position="is-top" :label="$t('help_item_start_date')" multilined> <i class="icon far fa-question-circle"></i></b-tooltip></template>
            <b-datetimepicker
              icon-pack="fas"
              icon="calendar"
              v-model="startDate"
            >
            </b-datetimepicker>
          </b-field>
          <b-field expanded>
	    <template #label> {{$t('end-date')}}
	      <b-tooltip position="is-top" :label="$t('help_item_end_date')" multilined> <i class="icon far fa-question-circle"></i></b-tooltip></template>
            <b-datetimepicker
              icon-pack="fas"
              icon="calendar"
              v-model="endDate"
              :min-date="startDate"
            >
            </b-datetimepicker>
          </b-field>
        </b-field>
        <b-field>
          <b-checkbox v-model="isRecurrent">
            <strong>{{$t('save-as-recurrent-item')}}</strong><b-tooltip position="is-top" :label="$t('help_item_recurrent')" multilined><i class="icon far fa-question-circle"></i></b-tooltip>
          </b-checkbox>
        </b-field>
        <div class="container has-text-centered">
          <button class="button is-primary" @click="submit">{{$t('submit')}}</button>
        </div>
      </section>
      <div class="column">
        <figure class="image is-256x256" v-if="filePreview">
          <img :src="filePreview" />
        </figure>
      </div>
    </div>
  </template>
  <template v-else>
    <div class="container has-text-centered buttons centered-container">
      <b-tooltip position="is-bottom" :label="$t('help_item_ihaveimage')" multilined><button class="button is-primary is-large" @click="step = 1">{{$t('i-have-image')}}</button></b-tooltip>  &nbsp; &nbsp;    <b-tooltip position="is-bottom" :label="$t('help_item_noimage')" multilined><button class="button is-primary is-large is-outlined" @click="step = 2">{{$t('i-do-not-have-image')}}</button></b-tooltip>
      
    </div>
    <recurrent-items-list @submitAgain="setRecurrentItem"/>
  </template>
</div>
</template>

<script>
import RecurrentItemsList from '@/components/RecurrentItemsList';
import axios from 'axios';
import CategorySelector from '@/components/CategorySelector';
import moment from 'moment/moment';
export default {
  name: 'AddItem',
  components: {CategorySelector, RecurrentItemsList},
  data() {
    return {
      loading: false,
      step: 0,
      errorCode: null,
      errorMessage: null,

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
  computed: {
    error() {
      return {
        code: this.errorCode,
        message: this.errorMessage
      }
    },
  },
  watch: {
    error() {
      this.$buefy.snackbar.open({
        duration: 5000,
        type: 'is-danger',
        message: `Error ${this.error.code}: ${this.error.message}`,
        pauseOnHover: true,
      })
    }
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
    },
    async submit() {
      this.errorCode = null;
      this.errorMessage = null;

      let startDate;
      if (this.startDate) {
        startDate = moment(this.startDate).format('YYYY-MM-DD[T]HH:mm:ss');
      }
      else {
        startDate = moment().format('YYYY-MM-DD[T]HH:mm:ss');
      }

      let endDate;
      if (this.endDate) {
        endDate = moment(this.endDate).format('YYYY-MM-DD[T]HH:mm:ss');
      }

      try {
        let uri = '/api/v1/items/';
        const item = (await axios.post(uri, {
          name: this.name,
          item_type: this.type,
          category1: this.category1,
          category2: (this.category2) ? this.category2 : '',
          category3: (this.category3) ? this.category3 : '',
          description: this.description,
          location: this.location,
          is_recurrent: this.isRecurrent,
          startdate: startDate,
          enddate: endDate,
          images: []
        })).data;

        if (this.file && this.filePreview) {
          const id = item.id;
          try {
            let uri = `/api/v1/images/`;
            let formData = new FormData();
            formData.append('itemID', id);
            let files = [this.file];
            let previews = [this.filePreview];
            for(let i = 0; i < Object.keys(files).length; i++){
              const file = files[i];
              const preview = previews[i];
              const blob = await (await fetch(preview)).blob();
              const newFile = new File([blob], file.name);
              formData.append('files', newFile);
            }
            await axios.post(uri, formData);

          }
          catch (error) {
            console.log(error);
            const response = error.response;
            this.errorCode = response.status;
            if (response.data.message) {
              this.errorMessage = response.data.message;
            }
            else {
              this.errorMessage = JSON.stringify(response.data);
            }
          }
        }

        await this.$router.push('/items');
      }
      catch (error) {
        console.log(error);
        const response = error.response;
        this.errorCode = response.status;
        if (response.data.message) {
          this.errorMessage = response.data.message;
        }
        else {
          this.errorMessage = JSON.stringify(response.data);
        }
      }
    },
    async setRecurrentItem(item) {
      this.name = item.name;
      this.description = item.description;
      this.type = item.item_type;
      this.category1 = item.category1;
      this.category2 = item.category2;
      this.category3 = item.category3;

      if (item.location !== null) {
        try {
          this.location = (await axios.post(`/api/v1/address/`, item.location)).data;
        }
        catch (error) {
          console.log(error);
        }
      }

      //TODO: set image files

      this.step = 2;
    }
  },
  mounted() {
    document.title = `Shareish | ${this.$t('add-new-item')}`;
  }
};
</script>

<style scoped>
.centered-container, .file {
  justify-content: center;
}
</style>
