<template>
  <div class="card">
    <div class="card-image">
      <b-carousel :autoplay="false" :arrow-hover="false" :arrow="item.images.length > 1" :indicator="item.images.length > 1">
        <template v-if="item.images.length > 0">
          <b-carousel-item v-for="image in item.images" :key="image.position">
            <router-link :to="linkOnClick">
              <figure class="image">
                <b-image :src="image" ratio="5by3" />
              </figure>
            </router-link>
          </b-carousel-item>
        </template>
        <template v-else>
          <b-carousel-item>
            <router-link :to="linkOnClick">
              <figure class="image">
                <b-image :src="itemCategories[0]['image-placeholder']" ratio="5by3" />
              </figure>
            </router-link>
          </b-carousel-item>
        </template>
      </b-carousel>
      <div class="hitcount tag">{{ item.hitcount }}<i class="far fa-eye"></i></div>
    </div>
    <div class="card-content">
      <div class="media">
        <div class="media-content">
          <p class="title is-5 mb-2">
            <router-link :to="linkOnClick">
              {{ item.name }}
            </router-link>
          </p>
          <p class="mb-2 description wbbw wspw">{{ item.description }}</p>
          <p class="subtitle is-6 mt-0">
            <item-type-tag :type="item.type" />
            <span v-if="item.user">
              {{ $t('by') }}
              <router-link :to="{name: 'profile', params: {id: item.user.id}}">
                @{{ item.user.username }}
              </router-link>
            </span>
          </p>
        </div>
      </div>
      <div v-if="!recurrentList" class="content">
        <small class="is-block">{{ $t('published') }} {{ formattedDateFromNow(item.creationdate) }}</small>
        <small class="is-block" v-if="item.enddate">
          <template v-if="!itemHasEnded">
            {{ $t('ends') }}
          </template>
          <template v-else>
            {{ $t('ended') }}
          </template>
          {{ formattedDateFromNow(item.enddate) }}
        </small>
        <small class="is-block" v-if="item.location && this.geoLocation">{{ ucfirst($t('at')) }} &#177; {{ getDistanceFromCoords().toFixed(2) }} km</small>
      </div>
      <span v-for="category in itemCategories" :key="category.slug" class="icon-text">
        <span class="icon"><i :class="category.icon"></i></span>
        <span>{{ $t(category.slug) }}</span>
      </span>
    </div>
    <div v-if="recurrentList" class="card-footer">
      <router-link :to="{name: 'addItemFrom', params: {id: item.id}}" class="card-footer-item">{{ $t('submit-again') }}</router-link>
    </div>
  </div>
</template>

<script>
import ItemTypeTag from "@/components/ItemTypeTag";
import moment from "moment/moment";
import {categories} from '@/categories';
import ErrorHandler from "@/components/ErrorHandler";
import {ucfirst} from "@/functions";

export default {
  name: 'ItemCard',
  mixins: [ErrorHandler],
  components: {ItemTypeTag},
  props: {
    item: {
      type: Object,
      required: true
    },
    recurrentList: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      geoLocation: null,
      linkOnClick: ""
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
    const addItemFromLink = {name: 'addItemFrom', params: {id: this.item.id}};
    const itemLink = {name: 'item', params: {id: this.item.id}};
    this.linkOnClick = !this.recurrentList ? itemLink : addItemFromLink;
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
    }
  },
  methods: {
    ucfirst,
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
    }
  }
};
</script>

<style scoped>
.card-image {
  position: relative;
}

.card-image .hitcount {
  position: absolute;
  right: 10px;
  bottom: 10px;
  font-weight: bold;
}

.card-image .hitcount i {
  margin-left: 4px;
}

.media-content .title {
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.media-content .title a {
  color: #4a4a4a !important;
}

.media-content .description {
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
}

.icon-text span {
  margin-right: 0.5rem;
}
</style>
