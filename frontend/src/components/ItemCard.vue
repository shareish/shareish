<template>
  <div class="card">
    <div class="card-image">
      <router-link :to="{name: 'itemDetail', params: {id: item.id}, query: itemDetailQueryParams}">
        <figure v-if="item.images.length > 0" :style="figureStyle" class="image is-5by3">
        </figure>
        <figure v-else class="image is-5by3">
          <img :src="category1['image-placeholder']" alt="Placeholder image">
        </figure>
      </router-link>
    </div>
    <div class="card-content">
      <div class="media">
        <div class="media-content">
          <p class="title is-4">
            <router-link :to="{name: 'itemDetail', params: {id: item.id}, query: itemDetailQueryParams}">
              {{ item.name }}
            </router-link>
          </p>
          <p class="subtitle is-6">
            <item-type-tag :type="item.item_type" />
            <span v-if="user">
              {{ $t('by') }}
              <router-link :to="{name: 'userDetails', params: {id: user.id}}">
                @{{ user.username }}
              </router-link>
            </span>
          </p>
        </div>
      </div>
      <div class="content">
        {{ truncate(item.description) }}
        <br />
        <template v-if="!recurrentList">
          <small>{{ formattedDate(item.startdate) }}</small><br />
          <small v-if="item.enddate"> {{ $t('ends') }} {{ formattedDate(item.enddate) }}</small><br />
          <small v-if="item.location && this.location">{{ $t('at') }} &#177; {{ getDistanceFromLatLonInKm() }} km</small><br />
          <small v-if="item.hitcount > 0">{{ item.hitcount }} {{ $t('views') }}</small><br />
        </template>
      </div>
      <span v-for="category in categories" :key="category.slug" class="icon-text">
        <span class="icon">
          <i :class="category.icon"></i>
        </span>
        <span>{{ $t(category.slug) }}</span>
      </span>
    </div>
    <div v-if="recurrentList" class="card-footer">
      <a class="card-footer-item" @click="$emit('submitAgain', item)">{{ $t('submit-again') }}</a>
    </div>
  </div>
</template>

<script>
import ItemTypeTag from '@/components/ItemTypeTag';
import moment from 'moment/moment';
import {categories} from '@/categories';

export default {
  name: 'ItemCard',
  components: {ItemTypeTag},
  props: {
    item: Object,
    recurrentList: {type: Boolean, default: false},
    userList: {type: Boolean, default: false},
    users: Array
  },
  data() {
    return {
      location: null,
      gettingLocation: false,
      errorStr: null,
    }
  },
  created() {
    // Do we support geolocation
    if (!("geolocation" in navigator)) {
      this.errorStr = 'Geolocation is not available.';
      return;
    }

    this.gettingLocation = true;
    // Get position
    navigator.geolocation.getCurrentPosition(pos => {
      this.gettingLocation = false;
      this.location = pos;
    }, err => {
      this.gettingLocation = false;
      this.errorStr = err.message;
    }, {
      maximumAge: 10000,
      timeout: 5000,
      enableHighAccuracy: true
    });
  },
  computed: {
    user() {
      return this.users.find(user => user.id === this.item.user) || {};
    },
    category1() {
      return this.category(this.item.category1);
    },
    category2() {
      return this.category(this.item.category2);
    },
    category3() {
      return this.category(this.item.category3);
    },
    categories() {
      let cat = [];
      if (this.category1) {
        cat.push(this.category1);
      }
      if (this.category2) {
        cat.push(this.category2);
      }
      if (this.category3) {
        cat.push(this.category3);
      }
      return cat;
    },
    figureStyle() {
      return (this.item.images.length === 0) ? {} : {backgroundImage: `url("${(this.item.images[0])}")`, 'border-radius': '0.25rem 0.25rem 0 0'};
    },
    itemKind() {
      if (this.recurrentList) {
        return 'recurrent';
      } else if (this.userList) {
        return 'user';
      }
      return null;
    },
    itemDetailQueryParams() {
      return (this.itemKind) ? {'kind': this.itemKind} : {};
    }
  },
  methods: {
    formattedDate(date) {
      return moment(date, "YYYY-MM-DD[T]HH:mm:ss").locale(this.$i18n.locale).fromNow();
    },
    truncate(description) {
      return (description.length > 150) ? description.slice(0, 150) + '[...]' : description;
    },
    category(category) {
      return categories[category];
    },
    deg2rad(deg) {
      return deg * (Math.PI / 180)
    },
    getDistanceFromLatLonInKm() {
      let latLong = this.item['location'].slice(17, -1).split(' ');
      var lat2 = latLong[0];
      var lon2 = latLong[1];
      var R = 6371; // Radius of the earth in km
      var dLat = this.deg2rad(lat2 - this.location.coords.latitude);  // deg2rad below
      var dLon = this.deg2rad(lon2 - this.location.coords.longitude);
      var a =
          Math.sin(dLat / 2) * Math.sin(dLat / 2) +
          Math.cos(this.deg2rad(this.location.coords.latitude)) * Math.cos(this.deg2rad(lat2)) *
          Math.sin(dLon / 2) * Math.sin(dLon / 2);
      var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
      var d = R * c; // Distance in km
      return d.toFixed(2);
    },

  },
};
</script>

<style scoped>
.image {
  background-repeat: no-repeat;
  background-position: center center;
  background-size: cover;
  position: relative;
  border-bottom: 1px solid #ddd;
}

.title a {
  color: #4a4a4a !important;
}

.icon-text span {
  margin-right: 0.5rem;
}
</style>
