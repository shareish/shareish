<template>
  <div class="box">
    <article class="media">
      <div class="media-left">
        <figure class="image">
          <img v-if="item.images.length > 0" :src="item.images[0]" alt="Image">
          <img v-else :src="category1['image-placeholder']" alt="Image">
        </figure>
      </div>
      <div class="media-content">
        <div class="content">
          <p>
            <strong class="is-size-4">{{ item.name }}</strong>
            <br>
            <item-type-tag :type="item.item_type" /> <small v-if="user">{{$t('by')}} @{{user.username}}</small>
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
            {{truncate(item.description)}}
          </p>
        </div>
        <nav class="level is-mobile">
        <div class="level-left">
          <router-link
            :to="{ name: 'itemDetail', params: { id: item.id}}"
          >
            <button class="button is-small is-primary level-item">
              <i class="fas fa-info-circle"></i> {{$t('i-am-interested')}}
            </button>
          </router-link>
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
  props: ['item', 'users'],
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
  },
  methods: {
      formattedDate(date) {
	  return moment(date, "YYYY-MM-DD[T]HH:mm:ss").fromNow();
      },
      truncate(description){
	  return (description.length > 150) ? description.slice(0, 150) + '[...]' : description;
      },
      category(category) {
	  return categories[category];
      }
  },
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

.image {
  width: 128px;
}
</style>
