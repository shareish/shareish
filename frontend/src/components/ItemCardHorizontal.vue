<template>
  <article class="media">
    <div class="media-left">
      <router-link :to="{name: 'item', params: {id: item.id}}">
        <figure class="image">
          <b-image :src="itemImage" ratio="1by1" />
        </figure>
      </router-link>
    </div>
    <div class="media-content">
      <div class="columns">
        <div class="column is-half">
          <div class="v-align-center" style="height: 100%;">
            <div class="inner">
              <h3 class="title is-size-4">
                <item-type-tag :type="item.type" />
                <router-link :to="{name: 'item', params: {id: item.id}}">
                  {{ item.name }}
                </router-link>
              </h3>
              <p class="subtitle is-size-6">
                {{ $t('published') }} {{ formattedDateFromNow(item.creationdate) }}
                &middot;
                <i class="far fa-eye"></i>{{ item.hitcount }} {{ $t('views') }}
              </p>
            </div>
          </div>
        </div>
        <div class="column is-half">
          <b-tooltip :label="$t('click-to-view-on-map')" position="is-bottom">
            <router-link v-if="address" :to="{name: 'map', query: {id: item.id}}">
              <span class="address">{{ address }}</span>
            </router-link>
          </b-tooltip>
        </div>
      </div>
    </div>
  </article>
</template>

<script>
import ErrorHandler from "@/components/ErrorHandler";
import ItemTypeTag from "@/components/ItemTypeTag.vue";
import {categories} from "@/categories";
import moment from "moment";
import axios from "axios";

export default {
  name: "ItemCardHorizontal",
  mixins: [ErrorHandler],
  components: {ItemTypeTag},
  props: {
    item: {
      type: Object,
      required: true
    },
    height: {
      type: Number,
      required: false,
      default: 100
    }
  },
  data() {
    return {
      geoLocation: null,
      address: null
    }
  },
  created() {
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

    this.fetchAddress();
  },
  watch: {
    item() {
      this.address = null;
      this.fetchAddress();
    }
  },
  computed: {
    itemCategories() {
      let itemCategories = [];
      if (categories[this.item.category1])
        itemCategories.push(categories[this.item.category1]);
      if (categories[this.item.category2])
        itemCategories.push(categories[this.item.category2]);
      if (categories[this.item.category3])
        itemCategories.push(categories[this.item.category3]);
      return itemCategories;
    },
    itemHasEnded() {
      return this.item.enddate && new Date(this.item.enddate) <= Date.now();
    },
    itemImage() {
      return (this.item.images.length > 0) ? this.item.images[0] : this.itemCategories[0]['image-placeholder'];
    },
    heightPx() {
      return this.height + "px";
    }
  },
  methods: {
    formattedDateFromNow(date) {
      return moment(date).locale(this.$i18n.locale).fromNow();
    },
    deg2rad(deg) {
      return deg * (Math.PI / 180)
    },
    getDistanceFromCoords() {
      let latLong = this.item['location'].slice(17, -1).split(' ');
      let lat2 = latLong[0];
      let lon2 = latLong[1];
      let R = 6371; // Radius of the earth in km
      let dLat = this.deg2rad(lat2 - this.geoLocation.coords.latitude);  // deg2rad below
      let dLon = this.deg2rad(lon2 - this.geoLocation.coords.longitude);
      let a =
          Math.sin(dLat / 2) * Math.sin(dLat / 2) +
          Math.cos(this.deg2rad(this.geoLocation.coords.latitude)) * Math.cos(this.deg2rad(lat2)) *
          Math.sin(dLon / 2) * Math.sin(dLon / 2);
      let c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
      return R * c; // Distance in km
    },
    async fetchAddress() {
      if (this.item.location !== null) {
        try {
          this.address = (await axios.post("/api/v1/address/", this.item.location)).data;
        } catch (error) {
          this.snackbarError(error);
        }
      }
    },
  }
}
</script>

<style lang="scss" scoped>
.media {
  height: v-bind(heightPx);

  .media-left {
    width: v-bind(heightPx);
    margin-right: 0.5rem;
  }

  .media-content {
    height: v-bind(heightPx);

    .columns {
      height: v-bind(heightPx);
      margin: 0;
    }

    .title span {
       margin-top: -0.3em;
    }
    .subtitle {
      font-style: italic;
      color: #767676;

      i {
        margin: 0 0.2em 0 0.1em;
      }
    }

    .address {
      overflow: hidden;
      display: -webkit-box;
      -webkit-line-clamp: 1;
      -webkit-box-orient: vertical;
    }
  }
}
</style>