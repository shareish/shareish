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
      <div class="columns is-mobile">
        <div class="column">
          <div class="v-align-center" style="height: 100%;">
            <div class="inner">
              <div class="title columns is-mobile">
                <div class="column pr-2">
                  <item-type-tag :type="item.type" />
                </div>
                <div class="column pl-0">
                  <router-link :to="{name: 'item', params: {id: item.id}}" class="item-name">
                    {{ item.name }}
                  </router-link>
                </div>
              </div>
              <p class="subtitle">
                {{ $t('published') }} {{ formattedDateFromNow(item.creationdate, $i18n.locale) }}
                <template v-if="showViewsCount">
                  &middot;
                  <i class="far fa-eye"></i>{{ item.views_count }} {{ $t('views') }}
                </template>
              </p>
            </div>
          </div>
        </div>
        <div class="column">
          <i v-for="category in itemCategories" :key="category.slug" :class="category.icon" class="category mr-2" :title="$t(category.slug)" />
          <router-link v-if="item.location" :to="{name: 'map', query: {id: item.id}}" class="button is-primary ml-2">
            <i class="fas fa-map-marker-alt"></i>
          </router-link>
        </div>
      </div>
    </div>
  </article>
</template>

<script>
import ErrorHandler from "@/mixins/ErrorHandler";
import ItemTypeTag from "@/components/ItemTypeTag.vue";
import {categories} from "@/categories";
import WindowSize from "@/mixins/WindowSize";
import {formattedDateFromNow} from "@/functions";

export default {
  name: "ItemCardHorizontal",
  mixins: [ErrorHandler, WindowSize],
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
    },
    showViewsCount: {
      type: Boolean,
      required: false,
      default: false
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
    formattedDateFromNow
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

    & > .columns {
      height: v-bind(heightPx);
      margin: 0;

      & > .column:first-child {
        height: v-bind(heightPx);

        .title {
          font-size: 1.25rem;
          margin-bottom: 0.75em;

          .column {
            flex-basis: auto;
          }

          span {
            margin-top: -0.3em;
          }

          .item-name {
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 1;
            -webkit-box-orient: vertical;
          }
        }
        .subtitle {
          font-size: 0.875rem;
          font-style: italic;
          color: #767676;

          i {
            margin: 0 0.2em 0 0.1em;
          }
        }
      }

      & > .column:last-child {
        flex: 0 0 200px;
        display: flex;
        justify-content: flex-end;

        .category {
          font-size: 1.5em;
          line-height: 40px;
        }
      }
    }
  }
}

@media screen and (max-width: 1023px) {
  .media {
    overflow: hidden;

    .media-content > .columns  {
      display: block;

      & > .column:last-child {
        display: none;
      }
    }
  }
}
</style>
