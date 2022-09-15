<template>
  <div class="card">
    <div class="card-image">
<!--      <figure class="image is-fullwidth">-->
<!--        <img v-if="images.length > 0" :src="images[0]" alt="Image">-->
<!--        <img v-else src="https://bulma.io/images/placeholders/1280x960.png" alt="Placeholder image">-->
<!--      </figure>      -->
      <router-link
        :to="{ name: 'itemDetail', params: { id: item.id}}"
      >
        <figure class="image is-5by3" :style="figureStyle" v-if="images.length > 0">
        </figure>
        <figure v-else class="image is-5by3">
          <img :src="category1['image-placeholder']" alt="Placeholder image">
        </figure>
      </router-link>


    </div>
    <div class="card-content">
      <div class="media">
<!--        <div class="media-left">-->
<!--          <figure class="image is-48x48">-->
<!--            <img src="https://bulma.io/images/placeholders/96x96.png" alt="Placeholder image">-->
<!--          </figure>-->
<!--        </div>-->
        <div class="media-content">
          <p class="title is-4">
            <router-link
              :to="{ name: 'itemDetail', params: { id: item.id}}"
            >
            {{ item.name }}
            </router-link>
          </p>
          <p class="subtitle is-6"><item-type-tag :type="item.item_type" /> <span v-if="user">{{$t('by')}} @{{user.username}}</span></p>
        </div>
      </div>
      <div class="content">
        {{item.description}}
        <br>
        <template v-if="!recurrentList">
          <small>{{formattedDate(item.startdate)}} </small><br>
          <small v-if="item.enddate"> {{$t('ends')}} {{formattedDate(item.enddate)}}</small>
        </template>
      </div>
      <span v-for="category in categories" class="icon-text" :key="category.slug">
        <span class="icon">
          <i :class="category.icon"></i>
        </span>
        <span>{{$t(category.slug)}}</span>
      </span>
    </div>
    <div class="card-footer" v-if="recurrentList">
      <a class="card-footer-item" @click="$emit('submitAgain', item)">{{$t('submit-again')}}</a>
    </div>
  </div>
</template>

<script>
import ItemTypeTag from '@/components/ItemTypeTag';
import axios from 'axios';
import moment from 'moment/moment';
import {categories} from '@/categories';

export default {
  name: 'ItemCard',
  components: {ItemTypeTag},
  props: {
    item: Object,
    recurrentList: {type: Boolean, default: false}
  },
  data() {
    return {
      user: null,
      images: [],
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
    figureStyle() {
      if (this.images.length === 0) {
        return {};
      }
      return {
        backgroundImage: `url("${(this.images[0])}")`,
        'border-radius': '0.25rem 0.25rem 0 0'
      };
    }
  },
  methods: {
    async fetchUser() {
      try {
        let uri = `/api/v1/webusers/${this.item['user']}/`;
        this.user = (await axios.get(uri)).data;
      }
      catch (error) {
        console.log(error);
      }
    },
    async fetchImages() {
      try {
        if (this.item['images'][0]) {
          const url = `/api/v1/images/${this.item['images'][0]}`;
          const data =  (await axios.get(url)).data;
          this.images = [data['url']];
        }
      }
      catch (error) {
        console.log(error);
      }
    },
    formattedDate(date) {
      return moment(date, "YYYY-MM-DD").fromNow();
    },
    category(category) {
      return categories[category];
    }
  },
  async mounted() {
    await Promise.all([
      this.fetchUser(),
      this.fetchImages()
    ]);
  }
};
</script>

<style scoped>
/*.image img {*/
/*  width: auto;*/
/*  height: auto;*/
/*  max-width: 100%;*/
/*  max-height: 100%;*/
/*  margin: auto;*/
/*}*/

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