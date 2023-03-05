<template>
  <div id="page-items">
    <items-filters
        @update:selectedType="selectedType = $event"
        @update:selectedCategory="selectedCategory = $event"
        @update:searchString="searchString = $event"
    />
    <b-loading v-if="loading" :active="loading" :is-full-page="false" />
    <div v-else ref="listItems" class="scrollable">
      <div v-if="items && items.length" class="columns is-mobile is-flex-wrap-wrap">
        <div v-for="item in items" :key="item.id" class="column" :class="columnsWidthClass">
          <item-card :item="item" />
        </div>
        <div v-if="!loadedAllItems" class="column is-narrow vertical-center">
          <button v-if="!loadedAllItems" :class="{'is-loading': itemsLoading}" class="button is-primary" @click="loadItems()">
            {{ $t('button-load-more') }}
          </button>
        </div>
      </div>
      <div v-else>{{ $t('no-items') }}</div>
    </div>
  </div>
</template>

<script>
import _ from 'lodash';
import ItemsFilters from '@/components/ItemsFilters';
import axios from 'axios';
import ItemCard from '@/components/ItemCard';
import ErrorHandler from "@/components/ErrorHandler";
import WindowSize from "@/components/WindowSize";

export default {
  name: 'TheItemsView',
  mixins: [ErrorHandler, WindowSize],
  components: {ItemsFilters, ItemCard},
  data() {
    return {
      searchString: null,
      selectedType: null,
      selectedCategory: null,

      loading: false,
      itemsLoading: false,
      page: 1,
      nbItemsPerPage: 20,
      loadedAllItems: false,
      columnsWidthClass: null,

      items: []
    }
  },
  computed: {
    params() {
      return {
        search: this.searchString,
        item_type: this.selectedType,
        category: this.selectedCategory
      };
    }
  },
  watch: {
    params() {
      this.loadItems(false);
    }
  },
  methods: {
    scrollHandler: _.debounce(function () {
      let scrollBlock = document.getElementById("wrapper");
      let bottom = (scrollBlock.scrollTop + scrollBlock.clientHeight >= scrollBlock.scrollHeight);
      if (bottom && !this.loadedAllItems) {
        this.loadItems();
      }
    }, 100),
    async loadItems(append = true) {
      this.itemsLoading = true;
      if (!append) {
        this.page = 1;
        this.loadedAllItems = false;
        this.items = [];
      }

      try {
        const uri = '/api/v1/actives/';
        const data = (await axios.get(uri, {params: {page: this.page, ...this.params}})).data;

        this.items.push(...data.results);
        this.page += 1;

        if (data.next === null) {
          this.loadedAllItems = true;
        }
      }
      catch (error) {
        this.snackbarError(error);
      }

      this.itemsLoading = false;
    },
    windowWidthChanged() {
      // Below or equal 520
      let columnsWidthClass = "is-full";
      if (this.windowWidth > 550) { // Arbitrary
        columnsWidthClass = "is-half";
        if (this.windowWidth > 768) { // Over PAL* (768x576)
          columnsWidthClass = "is-one-third";
          if (this.windowWidth > 1152) { // Over XGA+ (1152x864)
            columnsWidthClass = "is-one-quarter";
            if (this.windowWidth > 1600) { // Over UXGA (1600x1200)
              columnsWidthClass = "is-one-fifth";
              if (this.windowWidth > 2560) { // Over WQHD (2560x1440)
                columnsWidthClass = "is-2";
                if (this.windowWidth > 3840) { // Over UHD-1 (3840x2160)
                  columnsWidthClass = "is-1";
                }
              }
            }
          }
        }
      }
      this.columnsWidthClass = columnsWidthClass;
    }
  },
  async mounted() {
    this.loading = true;
    document.title = `Shareish | ${this.$t('items')}`;
    await Promise.all([
        this.loadItems()
    ]);
    this.loading = false;
  },
  created: function () {
    window.addEventListener('scroll', this.scrollHandler);
  },
  destroyed: function () {
    window.removeEventListener('scroll', this.scrollHandler);
  }
};
</script>

<style scoped>
.vertical-center {
  display: flex;
  flex-direction: row;
  align-items: center;
}
</style>
