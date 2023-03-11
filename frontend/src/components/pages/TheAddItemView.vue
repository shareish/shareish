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
        <div id="previews" v-if="images['previews']" class="mt-4">
          <h2 class="is-size-5 has-text-weight-bold mb-3">
            {{ $t('uploaded-images') }}
            <span class="tag vertical-align-middle ml-1" :class="imagesSlotsLeftColorClass">{{ images['previews'].length }} / {{ imagesSlots }}</span>
          </h2>
          <template v-if="images['previews'].length === 0">
            <p>{{ $t('no-uploaded-images') }}</p>
          </template>
          <template v-else>
            <div class="columns is-mobile is-flex-wrap-wrap">
              <div v-for="(preview, index) in images['previews']" :key="index" class="column" :class="imagesPreviewColumnSizeClass">
                <div class="square">
                  <div class="square-fill">
                    <div class="img-fill">
                      <div class="remove" @click="removeImage(index)">
                        <svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
                          <path d="M195.2 195.2a64 64 0 0 1 90.496 0L512 421.504 738.304 195.2a64 64 0 0 1 90.496 90.496L602.496 512 828.8 738.304a64 64 0 0 1-90.496 90.496L512 602.496 285.696 828.8a64 64 0 0 1-90.496-90.496L421.504 512 195.2 285.696a64 64 0 0 1 0-90.496z" />
                        </svg>
                      </div>
                      <img :src="preview" />
                    </div>
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
          <router-link to="/add-item/from-recurrents" class="button is-primary vertical-align-middle ml-2">{{ $t('yes-please') }}</router-link>
          <b-button class="vertical-align-middle ml-2" @click="hideRecurrentsItemsInfoBox = true">{{ $t('no-thanks') }}</b-button>
        </div>
        <div id="form">
          <div class="columns">
            <div class="column">
              <b-field key="name" :message="errors.first('name')" :type="{'is-danger': errors.has('name')}">
                <template #label>{{ $t('name') }}
                  <b-tooltip :label="$t('help_item_name')" multilined position="is-right">
                    <i class="icon far fa-question-circle"></i>
                  </b-tooltip>
                </template>
                <b-input v-model="name" name="name" v-validate="'required'" />
              </b-field>
            </div>
            <div class="column">
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
          <div class="columns">
            <div class="column">
              <b-field>
                <template #label>
                  <b-tooltip :label="$t('help_item_address')" multilined position="is-right">
                    {{ $t('address') }}
                    <i class="icon far fa-question-circle"></i>
                  </b-tooltip>
                </template>
                <b-button type="is-primary" @click="fetchAddressGeoLoc">
                  <i class="icon fas fa-map-marker-alt"></i>
                </b-button>
                <b-input v-model="location" class="is-expanded ml-2" name="ref_location" type="text" />
              </b-field>
            </div>
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
          <div class="columns">
          <div class="column">
          <b-checkbox v-model="isRecurrent">
            <strong>{{ $t('save-as-recurrent-item') }}</strong>
            <b-tooltip :label="$t('help_item_recurrent')" multilined position="is-top">
              <i class="icon far fa-question-circle"></i>
            </b-tooltip>
          </b-checkbox>
          </div>
          </div>
        </div>
        <div class="container has-text-centered mt-5">
          <a class="button mt-2" :class="formBottomButtonsSize" @click="reset">{{ $t('reset') }}</a>
          <b-button class="button is-primary mt-2 ml-2" :class="formBottomButtonsSize" :loading="waitingFormResponse" @click="submit">{{ $t('publish-item') }}</b-button>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CategorySelector from "@/components/CategorySelector";
import ErrorHandler from "@/components/ErrorHandler";
import moment from "moment/moment";
import WindowSize from "@/components/WindowSize";

export default {
  name: 'TheAddItemView',
  mixins: [ErrorHandler, WindowSize],
  $_veeValidate: {
    validator: 'new'
  },
  components: {CategorySelector},
  data() {
    return {
      loading: false,
      step: 0,

      filesSelected: [],
      images: {
        'files': [],
        'previews': []
      },
      imagesSlots: 12,
      imagesPreviewColumnSizeClass: 'is-one-third',
      formBottomButtonsSize: 'is-large',

      hideRecurrentsItemsInfoBox: false,

      // suggestedName: null,
      // suggestedCategory: null,
      // suggestedDescription: null,

      recurrentItem: null,

      name: "",
      description: "",
      type: '',
      category1: '',
      category2: '',
      category3: '',
      location: "",
      startdate: null,
      enddate: null,
      isRecurrent: false,

      geoloc: null,
      waitingFormResponse: false
    }
  },
  created() {
    this.fetchRecurrentItem();

    // Has the user activated geolocation?
    if ('geolocation' in navigator) {
      // Get the position
      navigator.geolocation.getCurrentPosition(
        positon => {
          this.geoloc = positon;
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
      return this.imagesSlots > this.images['previews'].length;
    },
    imagesSlotsLeft() {
      return this.imagesSlots - this.images['previews'].length;
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
    }
  },
  methods: {
    async fetchRecurrentItem() {
      if (this.isRecurrentItemUsed) {
        try {
          this.recurrentItem = (await axios.get(`/api/v1/recurrents/${this.recurrentItemId}`)).data;
          this.setFieldFromRecurrentItem();
        } catch (error) {
          this.snackbarError(error);
          await this.$router.push("/add-item");
        }
      }
    },
    async setFieldFromRecurrentItem() {
      if (this.recurrentItem !== null) {
        this.name = this.recurrentItem.name;
        this.description = this.recurrentItem.description;
        this.type = this.recurrentItem.item_type;
        this.category1 = this.recurrentItem.category1;
        this.category2 = this.recurrentItem.category2;
        this.category3 = this.recurrentItem.category3;
        this.isRecurrent = false;

        try {
          const images = JSON.parse((await axios.get(`/api/v1/items/${this.recurrentItemId}/images/base64`)).data);
          for (const i in images) {
            this.images['files'].push(images[i].name);
            this.images['previews'].push(images[i].base64_url);
          }
        } catch (error) {
          this.snackbarError(error);
        }

        this.fetchAddress(this.recurrentItem.location);
      }
    },
    async fetchAddressGeoLoc() {
      // We need to transform this.geoloc to SRID=4326;POINT (50.695118 5.0868788)
      if (this.geoloc !== null) {
        let geoLocPoint = "SRID=4326;POINT (" + this.geoloc.coords.latitude + " " + this.geoloc.coords.longitude + ")";
        this.fetchAddress(geoLocPoint);
      } else {
        this.snackbarError(this.$t('enable-geolocation-to-use-feature'));
      }
    },
    async fetchAddress(location) {
      if (location !== null) {
        try {
          this.location = (await axios.post("/api/v1/address/", location)).data;
        }
        catch (error) {
          this.fullErrorHandling(error);
        }
      }
    },
    async processImage(file) {
      this.loading = true;

      this.images['files'].unshift(file.name);
      const reader = new FileReader();
      reader.addEventListener('load', () => {
        this.images['previews'].unshift(reader.result)
      });
      reader.readAsDataURL(file);

      // await this.fetchPredictions(file);
      // this.name = this.suggestedName;
      // this.category1 = this.suggestedCategory;
      // this.description = this.suggestedDescription;

      this.loading = false;
    },
    removeImage(index) {
      this.images['files'].splice(index, 1);
      this.images['previews'].splice(index, 1);
    },
    // async fetchPredictions(file) {
    //   try {
    //     let data = new FormData();
    //     data.append('image', file);
    //     const predictions = (await axios.post("/api/v1/predictClass/", data)).data;
    //     this.suggestedName = predictions['suggested_class'];
    //     this.suggestedCategory = predictions['suggested_category'];
    //     this.suggestedDescription = predictions['suggested_class'] + ": " + predictions['detected_text'];
    //   }
    //   catch (error) {
    //     this.snackbarError(error);
    //   }
    // },
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
            item_type: this.type,
            category1: this.category1,
            category2: this.category2,
            category3: this.category3,
            description: this.description,
            location: this.location,
            is_recurrent: this.isRecurrent,
            startdate: startDate,
            enddate: endDate
          })).data;

          if (this.images['files'].length > 0) {
            try {
              let data = new FormData();
              data.append('item_id', item.id);

              for (let i in this.images['files']) {
                const blob = await (await fetch(this.images['previews'][i])).blob();
                const image = new File([blob], this.images['files'][i]);
                data.append('images', image);
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
    reset() {
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

.square {
  position: relative;
  overflow: hidden;
}

.square:before {
  content: "";
  display: block;
  padding-top: 100%;
}

.square-fill {
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
}

.img-fill {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  height: 100%;
}

.img-fill .remove {
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

.img-fill .remove svg {
  position: absolute;
  top: 50%;
  left: 50%;
  height: 60%;
  width: 60%;
  transform: translate(-50%, -50%);
  fill: white;
}

.img-fill img {
  flex-shrink: 0;
  min-width: 100%;
  min-height: 100%;
  max-width: inherit;
}
</style>
