<template>
  <div class="box">
    <article class="media">
      <div class="media-left">
        <figure class="image is-128x128">
          <img v-if="images.length > 0" :src="images[0]" alt="Image">
          <img v-else src="https://bulma.io/images/placeholders/128x128.png" alt="Image">
        </figure>
      </div>
      <div class="media-content">
        <div class="content">
          <p>
            <strong class="is-size-4">{{ item.name }}</strong>
            <br>
            <item-type-tag :type="item.item_type" /> <small>{{$t('by')}} @{{user.username}}</small>
            <br>
            <small>{{formattedDate(item.startdate)}} </small>
            <template v-if="item.enddate"> {{$t('to')}} {{formattedDate(item.enddate)}}</template>
          </p>
          <div class="level is-mobile categories-icons">
            <div class="level-left">
              <i :class="category1.icon" v-if="category1" :title="$t(category1.slug)" class="level-item fa-2x" />
              <i :class="category2.icon" v-if="category2" :title="$t(category2.slug)" class="level-item fa-2x" />
              <i :class="category3.icon" v-if="category3" :title="$t(category3.slug)" class="level-item fa-2x" />
            </div>
          </div>
          <p>
            {{item.description}}
          </p>
        </div>
        <nav class="level is-mobile">
        <div class="level-left">
            <button class="button is-small is-primary level-item">
              <i class="fas fa-info-circle"></i> {{$t('i-am-interested')}}
            </button>
        </div>
      </nav>
      </div>

    </article>
  </div>
</template>

<script>
import ItemTypeTag from '@/components/ItemTypeTag';
import axios from 'axios';
import moment from 'moment';
import {categories} from '@/categories';

export default {
  name: 'ItemMapPopup',
  components: {ItemTypeTag},
  props: ['item'],
  data() {
    return {
      user: null,
      images: null,
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
.box {
  box-shadow: none;
}

.categories-icons {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem !important;
}

button i {
  margin-right: 0.5rem;
}
</style>