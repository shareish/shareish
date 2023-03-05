<template>
  <div id="page-add-item">
    <h1 class="title has-text-centered mb-6">
      {{ $t('add-new-item') }}
      <b-tooltip :label="$t('help_add_item')" multilined position="is-bottom">
        <i class="icon far fa-question-circle"></i>
      </b-tooltip>
    </h1>
    <b-loading v-if="loading" :active="loading" :is-full-page="false" />
    <template v-if="step === 0">
      <div class="max-width-is-max-container has-text-centered buttons is-justify-content-center">
        <b-tooltip :label="$t('help_item_ihaveimage')" multilined position="is-bottom" class="mr-3">
          <button class="button is-primary is-large" @click="step = 1">{{ $t('i-have-image') }}</button>
        </b-tooltip>
        <b-tooltip :label="$t('help_item_noimage')" multilined position="is-bottom">
          <button class="button is-primary is-large is-outlined" @click="step = 2">{{ $t('i-do-not-have-image') }}</button>
        </b-tooltip>
      </div>
      <recurrent-items-list @submitAgain="setRecurrentItem" />
    </template>
    <template v-else-if="step === 1">
      <div class="container has-text-centered is-justify-content-center">
        <h2 class="subtitle">{{ $t('upload-your-item-image') }}</h2>
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
      </div>
    </template>
    <template v-else-if="step === 2">
      <div class="columns max-width-is-max-container">
        <section class="column is-8">
          <b-field key="name" :message="errors.first('name')" :type="{'is-danger': errors.has('name')}">
            <template #label>{{ $t('name') }}
              <b-tooltip :label="$t('help_item_name')" multilined position="is-right">
                <i class="icon far fa-question-circle"></i>
              </b-tooltip>
            </template>
            <b-input v-model="name" name="name" v-validate="'required'" />
          </b-field>

          <b-field key="type" :message="errors.first('type')" :type="{'is-danger': errors.has('type')}">
            <template #label>{{ $t('item-type') }}
              <b-tooltip :label="$t('help_item_type')" multilined position="is-right">
                <i class="icon far fa-question-circle"></i>
              </b-tooltip>
            </template>
            <b-select v-model="type" expanded name="type" v-validate="'required'">
              <option value="RQ">{{ $t('request') }}</option>
              <option value="DN">{{ $t('donation') }}</option>
              <option value="LN">{{ $t('loan') }}</option>
              <option value="EV">{{ $t('event') }}</option>
            </b-select>
          </b-field>

          <div class="columns">
            <b-tooltip :label="$t('help_item_category')" multilined position="is-right">
              <category-selector v-model="category1" :nullable="false" :number="1" class="column" expanded />
              <category-selector v-model="category2" :nullable="false" :number="2" class="column" expanded />
              <category-selector v-model="category3" :nullable="false" :number="3" class="column" expanded />
            </b-tooltip>
          </div>
          <b-field>
            <template #label>{{ $t('address') }}
              <b-tooltip :label="$t('help_item_address')" multilined position="is-right">
                <i class="icon far fa-question-circle"></i>
              </b-tooltip>
              <b-button size="is-small" @click="copyGeoLocAddress">
                <i class="icon fas fa-map-marker-alt"></i>
              </b-button>
            </template>
            <b-input v-model="location" />
          </b-field>
          <b-field key="description" :message="errors.first('description')" :type="{'is-danger': errors.has('description')}">
            <template #label> {{ $t('description') }}
              <b-tooltip :label="$t('help_item_description')" multilined position="is-right">
                <i class="icon far fa-question-circle"></i>
              </b-tooltip>
            </template>
            <b-input v-model="description" expanded type="textarea" name="description" v-validate="'required'" />
          </b-field>
          <b-field grouped>
            <b-field expanded>
              <template #label> {{ $t('start-date') }}
                <b-tooltip :label="$t('help_item_start_date')" multilined position="is-top">
                  <i class="icon far fa-question-circle"></i>
                </b-tooltip>
              </template>
              <b-datetimepicker v-model="startDate" icon="calendar" icon-pack="fas"></b-datetimepicker>
            </b-field>
            <b-field expanded>
              <template #label> {{ $t('end-date') }}
                <b-tooltip :label="$t('help_item_end_date')" multilined position="is-top">
                  <i class="icon far fa-question-circle"></i>
                </b-tooltip>
              </template>
              <b-datetimepicker v-model="endDate" :min-date="startDate" icon="calendar" icon-pack="fas"></b-datetimepicker>
            </b-field>
          </b-field>
          <b-field>
            <b-checkbox v-model="isRecurrent">
              <strong>{{ $t('save-as-recurrent-item') }}</strong>
              <b-tooltip :label="$t('help_item_recurrent')" multilined position="is-top">
                <i class="icon far fa-question-circle"></i>
              </b-tooltip>
            </b-checkbox>
          </b-field>
          <div class="container has-text-centered">
            <button class="button is-primary" @click="submit">{{ $t('submit') }}</button>
          </div>
        </section>
        <div class="column is-4">
          <template v-if="!isFromRecurrent">
            <figure v-if="filePreview" class="image is-256x256">
              <img :src="filePreview" />
            </figure>
          </template>
          <template v-else>
            <figure v-if="recurrentImages.length > 0" class="image is-256x256">
              <img :src="recurrentImages[recurrentImages.length - 1]" />
            </figure>
          </template>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import axios from 'axios';
import RecurrentItemsList from '@/components/RecurrentItemsList';
import CategorySelector from '@/components/CategorySelector';
import ErrorHandler from "@/components/ErrorHandler";
import moment from 'moment/moment';

export default {
  name: 'TheAddItemView',
  mixins: [ErrorHandler],
  $_veeValidate: {
    validator: 'new'
  },
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
      suggestedCategory: null,
      suggestedDescription: null,

      name: '',
      description: '',
      type: null,
      category1: null,
      category2: null,
      category3: null,
      location: '',
      isRecurrent: false,
      recurrentFrom: null,
      recurrentImages: [],
      startDate: null,
      endDate: null,

      geoloc: null
    }
  },
  created() {
    // Has the user activated geolocation?
    if ("geolocation" in navigator) {
      // Get the position
      navigator.geolocation.getCurrentPosition(positon => {
        this.geoloc = positon;
      }, error => {
        this.snackbarError(error);
      }, {
        maximumAge: 10000,
        timeout: 5000,
        enableHighAccuracy: true
      });
    }

    document.title = `Shareish | ${this.$t('add-new-item')}`;
  },
  computed: {
    error() {
      return {
        code: this.errorCode,
        message: this.errorMessage
      };
    },
    isFromRecurrent() {
      return this.recurrentFrom !== null;
    }
  },
  watch: {
    error() {
      this.$buefy.snackbar.open({
        duration: 5000,
        type: 'is-danger',
        message: `Error ${this.error.code}: ${this.error.message}`,
        pauseOnHover: true,
      });
    }
  },
  methods: {
    async copyGeoLocAddress() {
      if (this.geoloc !== null) {
        var geoLocPoint = 'SRID=4326;POINT (' + this.geoloc.coords.latitude + ' ' + this.geoloc.coords.longitude + ')'

        try {
          this.location = (await axios.post(`/api/v1/address/`, geoLocPoint)).data;
        }
        catch (error) {
          this.snackbarError(error);
        }
      }
    },
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
        const predictions = (await axios.post('/api/v1/predictClass/', data)).data;
        this.suggestedName = predictions['suggested_class'];
        this.suggestedCategory = predictions['suggested_category'];
        this.suggestedDescription = predictions['suggested_class'] + ": " + predictions['detected_text'];
      }
      catch (error) {
        this.snackbarError(error);
      }
    },
    async submit() {
      let result = await this.$validator.validateAll();
      if (result) {
        this.errorCode = null;
        this.errorMessage = null;

        let startDate;
        if (this.startDate) {
          startDate = moment(this.startDate).format('YYYY-MM-DD[T]HH:mm:ss');
        } else {
          startDate = moment().format('YYYY-MM-DD[T]HH:mm:ss');
        }

        let endDate;
        if (this.endDate) {
          endDate = moment(this.endDate).format('YYYY-MM-DD[T]HH:mm:ss');
        }

        try {
          let item = (await axios.post('/api/v1/items/', {
            name: this.name,
            item_type: this.type,
            category1: this.category1,
            category2: this.category2,
            category3: this.category3,
            description: this.description,
            location: this.location,
            is_recurrent: this.isRecurrent,
            startdate: startDate,
            enddate: endDate,
            images: []
          })).data;

          if (!this.isFromRecurrent) {
            if (this.file && this.filePreview) {
              try {
                let data = new FormData();
                data.append('item_id', item.id);

                let blob = await (await fetch(this.filePreview)).blob();
                let image = new File([blob], this.file.name);
                data.append('image', image);

                await axios.post("/api/v1/images/", data);
              }
              catch (error) {
                this.snackbarError(error);
              }
            }
          } else {
            try {
              await axios.get(`/api/v1/items/${item.id}/images/republish_from/${this.recurrentFrom}`);
            }
            catch (error) {
              this.snackbarError(error);
            }
          }

          this.$router.push(`/items/${item.id}`);
        }
        catch (error) {
          this.fullErrorHandling(error);
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
      this.recurrentFrom = item.id;
      this.recurrentImages = item.images;

      if (item.location !== null) {
        try {
          this.location = (await axios.post(`/api/v1/address/`, item.location)).data;
        }
        catch (error) {
          this.snackbarError(error);
        }
      }

      this.step = 2;
    }
  }
};
</script>

<style scoped>
.max-width-is-max-container {
  margin: 0 auto;
  max-width: 1344px;
}

.file {
  justify-content: center;
}
</style>
