<template>
  <div class="item-list">

    <items-filters
        @update:selectedType="selectedType = $event"
        @update:selectedCategory="selectedCategory = $event"
        @update:searchString="searchString = $event"
    />
    <b-loading v-if="pageLoading" :active="pageLoading" :is-full-page="false" />
    <div v-else ref="listItems" class="scrollable">
      <div v-if="items && items.length" class="columns">
        <div v-for="item in items" :key="`${item.id}-item-card`" class="column is-one-quarter">
          <item-card :item="item" :users="users" />
        </div>
        <div v-if="!loadedAllItems" class="column is-narrow vertical-center">
          <button v-if="!loadedAllItems" :class="{'is-loading': loading}" class="button is-primary" @click="loadItems()">
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

export default {
  name: 'ItemsList',
  components: {ItemsFilters, ItemCard},
  data() {
    return {
      searchString: null,
      selectedType: null,
      selectedCategory: null,

      pageLoading: false,
      loading: false,
      page: 1,
      nbItemsPerPage: 20,
      loadedAllItems: false,

      items: [],
      users: []
    }
  },
  computed: {
    params() {
      return {
        search: this.searchString,
        item_type: this.selectedType,
        category: this.selectedCategory
      }
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
      this.loading = true;
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
      } catch (error) {
        console.log(error);
      }

      this.loading = false;
    },
    async fetchUsers() {
      try {
        let uri = `/api/v1/webusers/`;
        this.users = (await axios.get(uri)).data;
      } catch (error) {
        console.log(error);
      }
    }
  },
  async mounted() {
    document.title = `Shareish | ${this.$t('items')}`;
    this.pageLoading = true;
    await Promise.all([this.loadItems(), this.fetchUsers()]);
    this.pageLoading = false;
    //console.log(this.items)  
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
.columns {
  flex-wrap: wrap;
  /*justify-content: space-between;*/
  align-content: flex-start;
}

.vertical-center {
  display: flex;
  flex-direction: row;
  align-items: center;
}
</style>
