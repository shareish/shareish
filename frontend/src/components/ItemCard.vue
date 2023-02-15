<template>
  <div class="card">
    <div class="card-image">
      <router-link :to="{name: 'itemDetail', params: {id: item.id}, query: itemDetailQueryParams}">
        <figure class="image">
          <b-image v-if="item.images.length > 0" :src="item.images[0]" ratio="5by3"></b-image>
          <b-image v-else :src="category1['image-placeholder']" ratio="5by3"></b-image>
          <div class="hitcount tag">
            {{ item.hitcount }}<i class="far fa-eye"></i>
          </div>
        </figure>
      </router-link>
    </div>
    <div class="card-content">
      <div class="media">
        <div class="media-content">
          <p class="title is-5 mb-2">
            <router-link :to="{name: 'itemDetail', params: {id: item.id}, query: itemDetailQueryParams}">
              {{ item.name }}
            </router-link>
          </p>
<!--          <p class="mb-2">{{ truncate(item.description) }}</p>-->
          <p class="subtitle is-6 mt-0">
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
        <template v-if="!recurrentList">
          <small class="is-block">{{ formattedDate(item.startdate) }}</small>
          <small class="is-block" v-if="item.enddate"> {{ $t('ends') }} {{ formattedDate(item.enddate) }}</small>
          <small class="is-block" v-if="item.location && this.location">{{ capitalize($t('at')) }} &#177; {{ getDistanceFromLatLonInKm() }} km</small>
<!--          <small class="is-block">{{ item.hitcount }} {{ $t('views') }}</small>-->
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
      let lat2 = latLong[0];
      let lon2 = latLong[1];
      let R = 6371; // Radius of the earth in km
      let dLat = this.deg2rad(lat2 - this.location.coords.latitude);  // deg2rad below
      let dLon = this.deg2rad(lon2 - this.location.coords.longitude);
      let a =
          Math.sin(dLat / 2) * Math.sin(dLat / 2) +
          Math.cos(this.deg2rad(this.location.coords.latitude)) * Math.cos(this.deg2rad(lat2)) *
          Math.sin(dLon / 2) * Math.sin(dLon / 2);
      let c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
      let d = R * c; // Distance in km
      return d.toFixed(2);
    },
    capitalize(s) {
      const capitalizedFirst = s[0].toUpperCase();
      const rest = s.slice(1);

      return capitalizedFirst + rest;
    }
  },
};
</script>

<style scoped>
.image {
  background-repeat: no-repeat;
  background-position: center center;
  background-size: cover;
  position: relative;
}

.image .hitcount {
  position: absolute;
  right: 10px;
  bottom: 10px;
  font-weight: bold;
}

.image .hitcount i {
  margin-left: 4px;
}

.image .item-type {
  position: absolute;
  bottom: 10px;
  left: 10px;
}

/* Adding ellipsis to second line of item name */
.media-content .title {
  height: 2.25em; /* line-height is set to 1.125 by default */
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.title a {
  color: #4a4a4a !important;
}

.icon-text span {
  margin-right: 0.5rem;
}
</style>
