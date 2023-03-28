<template>
  <div class="box">
    <article class="media">
      <div class="media-left">
        <router-link :to="{name: 'item', params: {id: item.id}}">
          <figure class="image">
            <img v-if="item.images.length > 0" :src="item.images[0]" alt="Image">
            <img v-else :src="itemCategories[0]['image-placeholder']" alt="Image">
          </figure>
        </router-link>
      </div>
      <div class="media-content">
        <div class="content">
          <p class="is-size-4 mb-1 wbbw has-text-weight-bold">{{ item.name }}</p>
          <div class="mb-1">
            <item-type-tag :type="item.type" />
            <span v-if="item.user">
              {{ $t('by') }}
              <router-link :to="{name: 'profile', params: {id: item.user.id}}">
                @{{ item.user.username }}
              </router-link>
            </span>
          </div>
          <small class="is-block">{{ $t('published') }} {{ formattedDateFromNow(item.creationdate, $i18n.locale) }}</small>
          <small v-if="notAvailableYet">
            {{ $t('available') }}
            {{ formattedDateFromNow(item.startdate, $i18n.locale) }}
          </small>
          <small class="is-block" v-if="item.enddate">
            <template v-if="!itemHasEnded">
              {{ $t('ends') }}
            </template>
            <template v-else>
              {{ $t('ended') }}
            </template>
            {{ formattedDateFromNow(item.enddate, $i18n.locale) }}
          </small>
          <div class="level is-mobile categories-icons">
            <div class="level-left">
              <i v-for="category in itemCategories" :key="category.slug" :class="category.icon" :title="$t(category.slug)" class="level-item fa-2x" />
            </div>
          </div>
          <p class="description wbbw wspw">{{ item.description }}</p>
        </div>
        <nav class="level is-mobile">
          <div class="level-left">
            <router-link :to="{name: 'item', params: {id: item.id}}">
              <button class="button is-small is-primary level-item">
                <i class="fas fa-info-circle"></i>
                {{ $t('i-am-interested') }}
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
import {categories} from '@/categories';
import {formattedDateFromNow} from "@/functions";

export default {
  name: 'ItemMapPopup',
  components: {ItemTypeTag},
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  computed: {
    itemHasEnded() {
      return this.item.enddate && new Date(this.item.enddate) <= Date.now();
    },
    notAvailableYet() {
      return this.item.startdate && new Date(this.item.startdate) > Date.now();
    },
    itemCategories() {
      let itemCategories = [];
      if (categories[this.item.category1])
        itemCategories.push(categories[this.item.category1]);
      if (categories[this.item.category2])
        itemCategories.push(categories[this.item.category2]);
      if (categories[this.item.category3])
        itemCategories.push(categories[this.item.category3]);
      return itemCategories;
    }
  },
  methods: {
    formattedDateFromNow,
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

.image {
  width: 128px;
}

.media-content .description {
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
}
</style>
