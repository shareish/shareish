<template>
  <b-loading v-if="loading" :active="true" :is-full-page="false" />
  <div v-else id="page-add-item" class="max-width-is-max-container" ref="page-container">
    <h1 class="title has-text-centered mb-6">
      {{ $t('add-new-item') }}
      <b-tooltip :label="$t('help_add_item')" multilined position="is-bottom">
        <i class="icon far fa-question-circle"></i>
      </b-tooltip>
    </h1>
    <div class="columns">
      <section id="images-side" class="column is-4 pl-5">
        <h2 class="is-size-4 has-text-centered mb-3">{{ $t('add-images-to-item') }}</h2>
        <b-field>
          <b-upload v-model="filesSelected" :disabled="!canStillUploadImages" accept="image/*" expanded multiple drag-drop>
            <section class="section">
              <div class="content has-text-centered">
                <p>
                  <i class="fas fa-upload fa-2x"></i>
                </p>
                <p>{{ $t('drop-or-click-to-upload') }}</p>
              </div>
            </section>
          </b-upload>
        </b-field>
        <div id="previews" v-if="images" class="mt-4">
          <h2 class="is-size-5 has-text-weight-bold mb-3">
            {{ $t('uploaded-images') }}
            <span class="tag vertical-align-middle ml-1" :class="imagesSlotsLeftColorClass">{{ images.length }} / {{ imagesSlots }}</span>
          </h2>
          <template v-if="images.length === 0">
            <p>{{ $t('no-uploaded-images') }}</p>
          </template>
          <template v-else>
            <div class="columns is-mobile is-flex-wrap-wrap">
              <div v-for="(image, index) in images" :key="index" class="column" :class="imagesPreviewColumnSizeClass">
                <div class="square">
                  <figure class="image">
                    <b-image :src="image['preview']" ratio="1by1" />
                  </figure>
                  <div class="remove" @click="removeImage(index)">
                    <svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
                      <path d="M195.2 195.2a64 64 0 0 1 90.496 0L512 421.504 738.304 195.2a64 64 0 0 1 90.496 90.496L602.496 512 828.8 738.304a64 64 0 0 1-90.496 90.496L512 602.496 285.696 828.8a64 64 0 0 1-90.496-90.496L421.504 512 195.2 285.696a64 64 0 0 1 0-90.496z" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </div>
      </section>
      <section id="form-side" class="column is-8">
        <div class="box mb-6" :class="{'is-hidden': hideRecurrentsItemsInfoBox}" style="border: 2px solid #3eaf7c;">
          <template v-if="!isRecurrentItemUsed">
            {{ $t('ask-fill-form-using-recurrents') }}
          </template>
          <template v-else>
            {{ $tc('want-an-other-recurrent', recurrentItemId) }}
          </template>
          <router-link :to="{name: 'addItemFromRecurrents'}" class="button is-primary vertical-align-middle ml-2">{{ $t('yes-please') }}</router-link>
          <b-button class="vertical-align-middle ml-2" @click="hideRecurrentsItemsInfoBox = true">{{ $t('no-thanks') }}</b-button>
        </div>
        <div id="form">
          <div class="columns">
            <div class="column">
              <b-field key="name" expanded :message="errors.first('name')" :type="{'is-danger': errors.has('name')}">
                <template #label>{{ $t('name') }}
                  <b-tooltip :label="$t('help_item_name')" multilined position="is-right">
                    <i class="icon far fa-question-circle"></i>
                  </b-tooltip>
                </template>
                <b-autocomplete
                    v-model="name"
                    :open-on-focus="true"
                    :data="suggestedNames"
                    field="name"
                    @select="option => assignCategory(option)"
                    :clearable="true"
                >
                </b-autocomplete>
              </b-field>
            </div>
            <div class="column">
              <b-field key="type" :message="errors.first('type')" :type="{'is-danger': errors.has('type')}">
                <template #label>{{ $tc('type', 1) }}
                  <b-tooltip :label="$t('help_item_type')" multilined position="is-right">
                    <i class="icon far fa-question-circle"></i>
                  </b-tooltip>
                </template>
                <div class="columns is-variable is-1">
                  <div class="column" v-for="itemType in itemTypes" :key="itemType['type']">
                    <b-button class="is-fullwidth" :class="[itemType['color'], {'is-outlined': (type !== itemType['type'])}]" @click="type = itemType['type']">{{ $t(itemType['slug']) }}</b-button>
                  </div>
                </div>
              </b-field>
            </div>
          </div>
          <div class="columns">
            <div class="column">
              <category-selector v-model="category1" :uses-tooltip="true" :number="1" expanded />
            </div>
            <div class="column">
              <category-selector v-model="category2" :number="2" expanded />
            </div>
            <div class="column">
              <category-selector v-model="category3" :number="3" expanded />
            </div>
          </div>
          <div class="columns">
            <div class="column">
              <b-field key="description" :message="errors.first('description')" :type="{'is-danger': errors.has('description')}">
                <template #label> {{ $t('description') }}
                  <b-tooltip :label="$t('help_item_description')" multilined position="is-right">
                    <i class="icon far fa-question-circle"></i>
                  </b-tooltip>
                </template>
                <b-input v-model="description" expanded type="textarea" name="description" v-validate="'required'" />
              </b-field>
            </div>
          </div>
          <b-field>
            <template #label>
              <b-tooltip :label="$t('help_item_address')" multilined position="is-right">
                {{ $t('address') }}
                <i class="icon far fa-question-circle"></i>
              </b-tooltip>
            </template>
            <b-tooltip :label="$t('use-geolocation')" type="is-info" position="is-bottom" class="mr-2">
              <b-button type="is-info" @click="fetchAddressGeoLoc">
                <i class="fas fa-street-view"></i>
              </b-button>
            </b-tooltip>
            <b-tooltip :label="$t('use-reflocation')" position="is-bottom" type="is-info">
               <b-button @click="fetchAddressRefLoc" type="is-info">
                 <i class="fas fa-home"></i>
               </b-button>
            </b-tooltip>
            <b-input v-model="address" @input="addressUpdatedByUser" class="is-expanded ml-2" name="ref_location" type="text" />
          </b-field>
          <div class="is-flex is-justify-content-flex-end mb-3">
            <b-switch v-model="use_coordinates" size="is-small" type="is-primary">{{ $t('use-coordinates') }}</b-switch>
          </div>
          <div class="columns">
            <div class="column">
              <b-field>
                <template #label> {{ $t('start-date') }}
                  <b-tooltip :label="$t('help_item_start_date')" multilined position="is-top">
                    <i class="icon far fa-question-circle"></i>
                  </b-tooltip>
                </template>
                <b-datetimepicker
                    v-model="startdate"
                    :max-datetime="enddate"
                    icon="calendar"
                    :icon-right="startdate ? 'close-circle' : ''"
                    icon-right-clickable
                    @icon-right-click="clearStartdate"
                    icon-pack="fas"
                    :locale="$i18n.locale"
                    @change="startdateChanged"
                />
              </b-field>
            </div>
            <div class="column">
              <b-field>
                <template #label> {{ $t('end-date') }}
                  <b-tooltip :label="$t('help_item_end_date')" multilined position="is-top">
                    <i class="icon far fa-question-circle"></i>
                  </b-tooltip>
                </template>
                <b-datetimepicker
                    v-model="enddate"
                    :min-datetime="startdate"
                    icon="calendar"
                    :icon-right="enddate ? 'close-circle' : ''"
                    icon-right-clickable
                    @icon-right-click="clearEnddate"
                    icon-pack="fas"
                    :locale="$i18n.locale"
                    @change="enddateChanged"
                />
              </b-field>
            </div>
          </div>
          <div class="level">
            <div class="level-left">
              <b-checkbox v-model="isRecurrent">
                <strong>{{ $t('save-as-recurrent-item') }}</strong>
                <b-tooltip :label="$t('help_item_recurrent')" multilined position="is-top">
                  <i class="icon far fa-question-circle"></i>
                </b-tooltip>
              </b-checkbox>
            </div>
            <div class="level-right">
              <p class="label m-0" style="line-height: 40px;">{{ $t('visibility') }}:</p>
              <b-dropdown v-model="visibility" aria-role="list" position="is-top-left" :class="{'ml-2': windowWidth > 768}">
                <template v-if="visibility === 'PB'" #trigger>
                  <b-button :label="$t('item_visibility__PB')" type="is-primary" icon-left="globe-europe" icon-right="menu-down" />
                </template>
                <template v-else-if="visibility === 'UL'" #trigger>
                  <b-button :label="$t('item_visibility__UL')" type="is-primary" icon-left="eye-slash" icon-right="menu-down" />
                </template>
                <template v-else-if="visibility === 'DR'" #trigger>
                  <b-button :label="$t('item_visibility__DR')" type="is-primary" icon-left="lock" icon-right="menu-down" />
                </template>
                <b-dropdown-item value="PB" aria-role="listitem">
                  <div class="media">
                    <b-icon class="media-left" pack="fas" icon="globe-europe" size="is-medium"></b-icon>
                    <div class="media-content">
                      <h3>{{ $t('item_visibility__PB') }}</h3>
                      <small>{{ $t('help_item_visibility__PB') }}</small>
                    </div>
                  </div>
                </b-dropdown-item>
                <b-dropdown-item value="UL" aria-role="listitem">
                  <div class="media">
                    <b-icon class="media-left" pack="fas" icon="eye-slash" size="is-medium"></b-icon>
                    <div class="media-content">
                      <h3>{{ $t('item_visibility__UL') }}</h3>
                      <small>{{ $t('help_item_visibility__UL') }}</small>
                    </div>
                  </div>
                </b-dropdown-item>
                <b-dropdown-item value="DR" aria-role="listitem">
                  <div class="media">
                    <b-icon class="media-left" pack="fas" icon="lock" size="is-medium"></b-icon>
                    <div class="media-content">
                      <h3>{{ $t('item_visibility__DR') }}</h3>
                      <small>{{ $t('help_item_visibility__DR') }}</small>
                    </div>
                  </div>
                </b-dropdown-item>
              </b-dropdown>
            </div>
          </div>
        </div>
        <div class="container has-text-centered mt-5">
          <b-button :type="visibility !== 'DR' ? 'is-primary' : 'is-warning'" class="mt-2 ml-2" :class="formBottomButtonsSize" :loading="waitingFormResponse" @click="submit">{{ $t(visibility !== 'DR' ? 'publish-item' : 'save') }}</b-button>
          <br />
          <a class="is-inline-block mt-5 has-text-danger" :class="formBottomButtonsSize" @click="resetForm">{{ $t('reset-form') }}</a>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CategorySelector from "@/components/CategorySelector.vue";
import ErrorHandler from "@/mixins/ErrorHandler";
import moment from "moment/moment";
import WindowSize from "@/mixins/WindowSize";
import {GeolocationCoords} from "@/functions";

export default {
  name: 'TheAddItemView',
  mixins: [ErrorHandler, WindowSize],
  $_veeValidate: {
    validator: 'new'
  },
  components: {CategorySelector},
  data() {
    return {
      itemTypes: [
        {'type': "DN", 'slug': "donation", 'color': 'is-success'},
        {'type': "LN", 'slug': "loan", 'color': 'is-warning'},
        {'type': "RQ", 'slug': "request", 'color': 'is-danger'},
        {'type': "EV", 'slug': "event", 'color': 'is-purple'}
      ],

      loading: false,
      step: 0,

      filesSelected: [],
      images: [],
      imagesSlots: 12,
      imagesPreviewColumnSizeClass: 'is-one-third',
      formBottomButtonsSize: 'is-large',

      hideRecurrentsItemsInfoBox: false,

      probabilities: [],
      suggestedNames: [],

      recurrentItem: null,

      name: "",
      description: "",
      type: '',
      category1: '',
      category2: '',
      category3: '',
      address_text: "",
      address_coords: new GeolocationCoords(),
      address: "",
      use_coordinates: false,
      user_updated_address_field: false,
      startdate: null,
      enddate: null,
      isRecurrent: false,
      visibility: 'PB',

      geoLocation: null,
      refLocation : null,
      waitingFormResponse: false
    }
  },
  created() {
    if (this.isRecurrentItemUsed)
      this.fetchRecurrentItem();
      
    if (this.isMapMarkerUsed) {
      this.fetchMapMarkerAddress(this.mapMarkerLat, this.mapMarkerLng);
      this.type = this.$route.params.type;
    }

    // Has the user activated geolocation?
    if ('geolocation' in navigator) {
      // Get the position
      navigator.geolocation.getCurrentPosition(
        position => {
          this.geoLocation = new GeolocationCoords(position);
        },
        null,
        {
          maximumAge: 10000,
          timeout: 5000,
          enableHighAccuracy: true
        }
      );
    }

    document.title = `Shareish | ${this.$t('add-new-item')}`;
  },
  computed: {
    canStillUploadImages() {
      return this.imagesSlots > this.images.length;
    },
    imagesSlotsLeft() {
      return this.imagesSlots - this.images.length;
    },
    imagesSlotsLeftColorClass () {
      if (this.imagesSlotsLeft >= 6)
        return 'is-primary';
      else if (this.imagesSlotsLeft >= 3)
        return 'is-warning';
      else
        return 'is-danger';
    },
    recurrentItemId() {
      return Number(this.$route.params.id);
    },
    isRecurrentItemUsed() {
      return this.recurrentItemId > 0;
    },
    mapMarkerLat() {
      return Number(this.$route.params.lat);
    },
    mapMarkerLng() {
      return Number(this.$route.params.lng);
    },
    isMapMarkerUsed() {
      return (this.mapMarkerLat > 0 && this.mapMarkerLng > 0);	  
    }
  },
  watch: {
    filesSelected() {
      if (this.filesSelected.length > 0) {
        if (this.imagesSlotsLeft) {
          if (this.filesSelected.length <= this.imagesSlotsLeft) {
            for (const i in this.filesSelected)
              this.processImage(this.filesSelected[i]);
          } else {
            this.snackbarError(this.$tc('too-many-images-selected-to-upload', this.imagesSlotsLeft));
          }
        } else {
          this.snackbarError(this.$t('max-images-uploaded-reached'));
        }
        this.filesSelected = [];
      }
    },
    use_coordinates() {
      if (!this.user_updated_address_field)
        this.updateAddressField();
    }
  },
  methods: {
    async fetchRecurrentItem() {
      if (this.isRecurrentItemUsed) {
        try {
          this.recurrentItem = (await axios.get(`/api/v1/recurrents/${this.recurrentItemId}`)).data;
          await this.setFieldFromRecurrentItem();
        }
        catch (error) {
          this.snackbarError(error);
          await this.$router.push("/add-item");
        }
      }
    },
    async fetchMapMarkerAddress(lat, lng) {
      try {
        const coords = new GeolocationCoords(lng, lat);
	      if (coords instanceof GeolocationCoords) {
		      this.address_text = await this.fetchAddress(coords);
		      this.address = this.address_text;
          this.address_coords = coords;
        }
      }
      catch (error) {
        this.snackbarError(error);
      }
    },
    async setFieldFromRecurrentItem() {
      if (this.recurrentItem !== null) {
        this.name = this.recurrentItem.name;
        this.description = this.recurrentItem.description;
        this.type = this.recurrentItem.type;
        this.category1 = this.recurrentItem.category1;
        this.category2 = this.recurrentItem.category2;
        this.category3 = this.recurrentItem.category3;
        this.isRecurrent = false;

        try {
          const images = JSON.parse((await axios.get(`/api/v1/items/${this.recurrentItemId}/images/base64`)).data);
          for (const i in images)
            this.images.push({
              'filename': images[i].name,
              'predictions': [],
              'preview': images[i].base64_url,
              'probability': 0
            });
        }
        catch (error) {
          this.snackbarError(error);
        }

        this.address = await this.fetchAddress(new GeolocationCoords(this.recurrentItem.location));
      }
    },
    async fetchAddressRefLoc() {
      try {
        const params = {
          columns: ['ref_location']
        }
        const userId = Number(this.$store.state.user.id);
        const refLocation = (await axios.get(`api/v1/webusers/${userId}`, {params: params})).data.ref_location;
        if (refLocation !== null) {
          this.refLocation = new GeolocationCoords(refLocation);
          if (this.refLocation instanceof GeolocationCoords) {
            this.user_updated_address_field = false;
            this.address_text = await this.fetchAddress(this.refLocation);
            this.address_coords = this.refLocation;
            this.updateAddressField();
          }
        } else {
          this.snackbarError(this.$t('set-a-reflocation-to-use-feature'));
        }
      }
      catch (error) {
        this.snackbarError(error);
      }
    },
    async fetchAddressGeoLoc() {
      if (this.geoLocation instanceof GeolocationCoords) {
        this.user_updated_address_field = false;
        this.address_text = await this.fetchAddress(this.geoLocation);
        this.address_coords = this.geoLocation;
        this.updateAddressField();
      } else {
        this.snackbarError(this.$t('enable-geolocation-to-use-feature'));
      }
    },
    async fetchAddress(location) {
      if (location instanceof GeolocationCoords) {
        try {
          return (await axios.post("/api/v1/address/reverse", location)).data;
        }
        catch (error) {
          this.fullErrorHandling(error);
        }
      }
      return null;
    },
    updateAddressField() {
      if (!this.use_coordinates)
        this.address = this.address_text;
      else
        this.address = this.address_coords.toStringForUser();
    },
    addressUpdatedByUser() {
      if (!this.user_updated_address_field)
        this.user_updated_address_field = true;
    },
    async processImage(file) {
      this.loading = true;

      const reader = new FileReader();
      reader.addEventListener('load', () => {
        this.images.push({"filename": file.name, 'predictions': [], 'preview': reader.result, 'probability': 0});
        this.fetchPredictions(file, this.images.length - 1);
      });
      reader.readAsDataURL(file);

      this.loading = false;
    },
    async fetchPredictions(file, position) {
      try {
        let data = new FormData();
        data.append('image', file);
        const response = (await axios.post("/api/v1/predictClass/", data)).data;
        const probabilities = response['probabilities'];
        this.images[position]['predictions'] = probabilities;

        for (let i in probabilities) {
          let found = false;
          for (let j in this.probabilities) {
            if (this.probabilities[j]['class'] === probabilities[i]['class']) {
              this.probabilities[j]['probability'] += probabilities[i]['probability'];
              found = true;
              break;
            }
          }
          if (!found)
              this.probabilities.push({...probabilities[i]});
        }

        this.sortPredictions();
        this.refreshSuggestedNames();

        this.description += response['detected_text']

        if (this.probabilities[0])
          this.category1 = this.probabilities[0]['category'];
      }
      catch (error) {
        this.snackbarError(error);
      }
    },
    removeImage(index) {
      const imagePredictionsToRemove = this.images[index]['predictions'];
      for (let i in imagePredictionsToRemove) {
        for (let j in this.probabilities) {
          if (this.probabilities[j]['class'] === imagePredictionsToRemove[i]['class']) {
            this.probabilities[j]['probability'] -= imagePredictionsToRemove[i]['probability'];
            break;
          }
        }
      }

      let j = 0;
      while (j < this.probabilities.length) {
        if (this.probabilities[j]['probability'] <= 0)
          this.probabilities.splice(j, 1);
        else
          j++;
      }

      this.sortPredictions();
      this.refreshSuggestedNames();

      this.images.splice(index, 1);
    },
    sortPredictions() {
      this.probabilities.sort(function(first, second) {
        return second['probability'] - first['probability'];
      });
    },
    refreshSuggestedNames() {
      this.suggestedNames = [];
      const predictionsLength = (this.probabilities.length < 5) ? this.probabilities.length : 5;
      for (let i = 0; i < predictionsLength; i++)
        this.suggestedNames.push(this.probabilities[i]['class']);
    },
    assignCategory(option) {
      for (let i in this.probabilities) {
        if (this.probabilities[i]['class'] === option) {
          this.category1 = this.probabilities[i]['category'];
          break;
        }
      }
    },
    async submit() {
      this.waitingFormResponse = true;

      let result = await this.$validator.validateAll();
      if (result) {
        let startDate;
        if (this.startdate)
          startDate = moment(this.startdate).format("YYYY-MM-DD[T]HH:mm:ss");
        else
          startDate = moment().format("YYYY-MM-DD[T]HH:mm:ss");

        let endDate;
        if (this.enddate)
          endDate = moment(this.enddate).format("YYYY-MM-DD[T]HH:mm:ss");
        else
          endDate = null;

        try {
          let item = (await axios.post("/api/v1/items/", {
            name: this.name,
            type: this.type,
            category1: this.category1,
            category2: this.category2,
            category3: this.category3,
            description: this.description,
            location: this.address,
            use_coordinates: this.use_coordinates,
            is_recurrent: this.isRecurrent,
            startdate: startDate,
            enddate: endDate,
            visibility: this.visibility,
            images: []
          })).data;

          if (this.images.length > 0) {
            try {
              let data = new FormData();
              data.append('item_id', item.id);

              for (let i in this.images) {
                const blob = await (await fetch(this.images[i]['preview'])).blob();
                const tempFile = new File([blob], this.images[i]['filename']);
                data.append('images', tempFile);
              }

              await axios.post("/api/v1/images/", data);
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

      this.waitingFormResponse = false;
    },
    resetForm() {
      this.name = "";
      this.description = "";
      this.type = '';
      this.category1 = '';
      this.category2 = '';
      this.category3 = '';
      this.startdate = null;
      this.enddate = null;
      this.isRecurrent = false;
      this.recurrentItem = null;

      this.images['files'] = [];
      this.images['previews'] = [];
    },
    clearStartdate() {
      this.startdate = null;
      this.startdateChanged();
    },
    clearEnddate() {
      this.enddate = null;
      this.enddateChanged();
    },
    startdateChanged() {
      if (this.enddate && this.startdate) {
        if (this.startdate > this.enddate)
          this.enddate = this.startdate;
      }
    },
    enddateChanged() {
      if (this.enddate && this.startdate) {
        if (this.enddate < this.startdate)
          this.startdate = this.enddate;
      }
    },
    windowWidthChanged() {
      let imagesPreviewColumnSizeClass = "is-one-third";
      let formBottomButtonsSize = "is-large";
      if (this.windowWidth <= 1500) {
        imagesPreviewColumnSizeClass = "is-2";
        if (this.windowWidth < 1100) {
          imagesPreviewColumnSizeClass = "is-one-quarter";
          if (this.windowWidth < 768) {
            imagesPreviewColumnSizeClass = "is-one-third";
            formBottomButtonsSize = "is-normal";
            if (this.windowWidth < 550) {
              imagesPreviewColumnSizeClass = "is-half";
              if (this.windowWidth < 380) {
                imagesPreviewColumnSizeClass = "is-full";
              }
            }
          }
        }
      }
      this.formBottomButtonsSize = formBottomButtonsSize;
      this.imagesPreviewColumnSizeClass = imagesPreviewColumnSizeClass;
    }
  }
};
</script>

<style scoped>

@media screen and (max-width: 1500px) {
  #page-add-item > .columns {
    display: block;
  }

  #page-add-item > .columns > .column {
    width: 100%;
  }

  #form-side > .box {
    margin-top: 1.5rem !important;
  }
}

.max-width-is-max-container {
  margin: 0 auto;
  max-width: 1344px;
}

#previews .column {
  height: 33%;
}

.vertical-align-middle {
  margin-top: -1px;
  vertical-align: middle;
}

#previews .square {
  position: relative;
}

#previews .square .remove {
  position: absolute;
  top: 8px;
  right: 8px;
  height: 20%;
  width: 20%;
  padding: 5px;
  border-radius: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  cursor: pointer;
}

#previews .square .remove svg {
  position: absolute;
  top: 50%;
  left: 50%;
  height: 60%;
  width: 60%;
  transform: translate(-50%, -50%);
  fill: white;
}
</style>
