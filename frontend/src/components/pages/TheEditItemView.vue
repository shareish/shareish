<template>
  <b-loading v-if="loading" :active="true" :is-full-page="false" />
  <div v-else id="page-add-item" class="max-width-is-max-container" ref="page-container">
    <h1 class="title has-text-centered mb-6">
      {{ $t('edit-item') }}
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
                  <figure class="image">
                    <b-image :src="preview" ratio="1by1" />
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
        <div id="form">
          <div class="columns">
            <div class="column">
              <b-field key="name" :message="errors.first('name')" :type="{'is-danger': errors.has('name')}">
                <template #label>{{ $t('name') }}
                  <b-tooltip :label="$t('help_item_name')" multilined position="is-right">
                    <i class="icon far fa-question-circle"></i>
                  </b-tooltip>
                </template>
                <b-input v-model="internalItem.name" name="name" v-validate="'required'" />
              </b-field>
            </div>
            <div class="column">
              <b-field key="type" :message="errors.first('type')" :type="{'is-danger': errors.has('type')}">
                <template #label>{{ $t('item-type') }}
                  <b-tooltip :label="$t('help_item_type')" multilined position="is-right">
                    <i class="icon far fa-question-circle"></i>
                  </b-tooltip>
                </template>
                <b-select v-model="internalItem.type" expanded name="type" v-validate="'required'">
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
              <category-selector v-model="internalItem.category1" :uses-tooltip="true" :number="1" expanded />
            </div>
            <div class="column">
              <category-selector v-model="internalItem.category2" :number="2" expanded />
            </div>
            <div class="column">
              <category-selector v-model="internalItem.category3" :number="3" expanded />
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
                <b-input v-model="internalItem.description" expanded type="textarea" name="description" v-validate="'required'" />
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
                    v-model="internalItem.startdate"
                    :max-datetime="internalItem.enddate"
                    icon="calendar"
                    :icon-right="internalItem.startdate ? 'close-circle' : ''"
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
                    v-model="internalItem.enddate"
                    :min-datetime="minEnddate"
                    icon="calendar"
                    :icon-right="internalItem.enddate ? 'close-circle' : ''"
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
          <b-checkbox v-model="internalItem.is_recurrent">
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
          <b-button class="button is-primary mt-2 ml-2" :class="formBottomButtonsSize" :loading="waitingFormResponse" @click="submit">{{ $t('save') }}</b-button>
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
  name: 'TheEditItemView',
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

      item: {},
      internalItem: {},
      location: "",
      initialStartdate: Date.now(),

      geoLocation: null,
      waitingFormResponse: false
    }
  },
  created() {
    this.fetchItem();

    // Has the user activated geolocation?
    if ('geolocation' in navigator) {
      // Get the position
      navigator.geolocation.getCurrentPosition(
        position => {
          this.geoLocation = position;
        },
        null,
        {
          maximumAge: 10000,
          timeout: 5000,
          enableHighAccuracy: true
        }
      );
    }

    document.title = `Shareish | ${this.$t('edit-item')}`;
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
    itemId() {
      return Number(this.$route.params.id);
    },
    minEnddate() {
      const now = new Date();
      if (this.internalItem.startdate) {
        const startdate = new Date(this.internalItem.startdate);
        return (startdate > now) ? startdate : now;
      }
      return now;
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
    async fetchItem() {
      try {
        this.item = (await axios.get(`/api/v1/user_items/${this.itemId}`)).data;
        this.setFieldFromItem();
      } catch (error) {
        this.snackbarError(error);
        await this.$router.push("/items");
      }
    },
    async setFieldFromItem() {
      if (this.item !== null) {

        this.internalItem = {...this.item};

        if (this.internalItem.startdate) {
          this.internalItem.startdate = new Date(this.internalItem.startdate);
          this.initialStartdate = this.internalItem.startdate;
        }

        if (this.internalItem.enddate)
          this.internalItem.enddate = new Date(this.internalItem.enddate);

        try {
          this.images['files'] = [];
          this.images['previews'] = [];

          const images = JSON.parse((await axios.get(`/api/v1/items/${this.itemId}/images/base64`)).data);
          for (const i in images) {
            this.images['files'].push(images[i].name);
            this.images['previews'].push(images[i].base64_url);
          }
        } catch (error) {
          this.snackbarError(error);
        }

        this.fetchAddress(this.internalItem.location);
      }
    },
    async fetchAddressGeoLoc() {
      // We need to transform this.geoloc to SRID=4326;POINT (50.695118 5.0868788)
      if (this.geoLocation !== null) {
        const geoLocPoint = "SRID=4326;POINT (" + this.geoLocation.coords.latitude + " " + this.geoLocation.coords.longitude + ")";
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

      this.loading = false;
    },
    removeImage(index) {
      this.images['files'].splice(index, 1);
      this.images['previews'].splice(index, 1);
    },
    async submit() {
      this.waitingFormResponse = true;

      if (await this.$validator.validateAll()) {
        let startDate;
        if (this.internalItem.startdate)
          startDate = moment(this.internalItem.startdate).format("YYYY-MM-DD[T]HH:mm:ss");
        else
          startDate = moment().format("YYYY-MM-DD[T]HH:mm:ss");

        let endDate;
        if (this.internalItem.enddate)
          endDate = moment(this.internalItem.enddate).format("YYYY-MM-DD[T]HH:mm:ss");
        else
          endDate = null;

        try {
          const item = (await axios.patch(`/api/v1/items/${this.item.id}/`, {
            name: this.internalItem.name,
            type: this.internalItem.type,
            category1: this.internalItem.category1,
            category2: this.internalItem.category2,
            category3: this.internalItem.category3,
            description: this.internalItem.description,
            location: this.location,
            is_recurrent: this.internalItem.is_recurrent,
            startdate: startDate,
            enddate: endDate
          })).data;

          if (this.images['files'].length > 0) {
            try {
              const data = new FormData();
              data.append('item_id', item.id);

              for (let i in this.images['files']) {
                const blob = await (await fetch(this.images['previews'][i])).blob();
                const tempFile = new File([blob], this.images['files'][i]);
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
    reset() {
      this.setFieldFromItem();
    },
    clearStartdate() {
      this.internalItem.startdate = this.initialStartdate;
      this.startdateChanged();
    },
    clearEnddate() {
      this.internalItem.enddate = null;
      this.enddateChanged();
    },
    startdateChanged() {
      if (this.internalItem.enddate && this.internalItem.startdate) {
        if (this.internalItem.startdate > this.internalItem.enddate)
          this.internalItem.enddate = this.internalItem.startdate;
      }
    },
    enddateChanged() {
      if (this.internalItem.enddate && this.internalItem.startdate) {
        if (this.internalItem.enddate < this.internalItem.startdate)
          this.internalItem.startdate = this.internalItem.enddate;
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
