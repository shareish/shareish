<template>
  <div class="card">
    <div class="card-image">
      <router-link :to="{name: 'itemDetail', params: {id: item.id}, query: itemDetailQueryParams}">
        <figure class="image">
          <b-image v-if="item.images.length > 0" :src="item.images[item.images.length - 1]" ratio="5by3"></b-image>
          <b-image v-else :src="category1['image-placeholder']" ratio="5by3"></b-image>
          <div class="hitcount tag">{{ item.hitcount }}<i class="far fa-eye"></i></div>
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
          <p class="mb-2">{{ truncate(item.description) }}</p>
          <p class="subtitle is-6 mt-0">
            <item-type-tag :type="item.item_type" />
            <span v-if="item.user">
              {{ $t('by') }}
              <router-link :to="{name: 'userDetails', params: {id: item.user.id}}">
                @{{ item.user.username }}
              </router-link>
            </span>
          </p>
        </div>
      </div>
      <div class="content">
        <template v-if="!recurrentList">
          <small class="is-block">{{ $t('published') }} {{ formattedDateFromNow(item.creationdate) }}</small>
          <small class="is-block" v-if="item.enddate">{{ $t('ends') }} {{ formattedDateFromNow(item.enddate) }}</small>
          <small class="is-block" v-if="item.location && this.location">{{ capitalize($t('at')) }} &#177; {{ getDistanceFromCoords().toFixed(2) }} km</small>
        </template>
      </div>
      <span v-for="category in categories" :key="category.slug" class="icon-text">
        <span class="icon"><i :class="category.icon"></i></span>
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
import ErrorHandler from "@/components/ErrorHandler";

export default {
  name: 'ItemCard',
  mixins: [ErrorHandler],
  components: {ItemTypeTag},
  props: {
    item: Object,
    recurrentList: {type: Boolean, default: false}
  },
  data() {
    return {
      location: null
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
  },
  computed: {
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
      return (this.recurrentList) ? 'recurrent' : null;
    },
    itemDetailQueryParams() {
      return (this.itemKind) ? {'kind': this.itemKind} : {};
    }
  },
  methods: {
    formattedDateFromNow(date) {
      return moment(date).locale(this.$i18n.locale).fromNow();
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
    getDistanceFromCoords() {
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
      return R * c; // Distance in km
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
