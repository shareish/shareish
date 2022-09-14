<template>
  <div class="item-list">
    <items-filters
      @update:selectedType="selectedType = $event"
      @update:selectedCategory="selectedCategory = $event"
      @update:searchString="searchString = $event"
    />

    <div class="scrollable"  ref="listItems">
      <div class="columns" v-if="items && items.length">
        <div class="column" v-for="item in items" :key="`${item.id}-item-card`">
          {{item}}
        </div>
        <div class="column is-narrow vertical-center" v-if="!loadedAllItems">
          <button class="button is-primary" :class="{'is-loading': loading}" v-if="!loadedAllItems" @click="loadItems()">
            {{$t('button-load-more')}}
          </button>
        </div>
      </div>
      <div v-else>
        {{$t('no-items')}}
      </div>
    </div>

  </div>
</template>

<script>
import _ from 'lodash';
import ItemsFilters from '@/components/ItemsFilters';
import axios from 'axios';

export default {
  name: 'ItemsList',
  components: {ItemsFilters},
  data() {
    return {
      searchString: null,
      selectedType: null,
      selectedCategory: null,

      loading: false,
      page: 1,
      nbItemsPerPage: 20,
      loadedAllItems: false,

      items: []
    }
  },
  computed: {
    params() {
      return {
        name: this.searchString,
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
    scrollHandler: _.debounce(function() {
      let scrollBlock = document.getElementById("wrapper");
      let bottom = (scrollBlock.scrollTop + scrollBlock.clientHeight === scrollBlock.scrollHeight);
      if (bottom && !this.loadedAllItems) {
        this.loadItems();
      }
    }, 100),
    async loadItems(append=true) {
      this.loading = true;
      if (!append) {
        this.page = 1;
        this.loadedAllItems = false;
        this.items = [];
      }

      try {
        const uri = '/api/v1/actives/';
        // TODO: endpoint should use filters...
        const data = (await axios.get(uri, {params: {page: this.page}})).data;

        this.items.push(...data.results);
        this.page += 1;

        if (data.next === null) {
          this.loadedAllItems = true;
        }
      }
      catch (error) {
        console.log(error);
      }

      this.loading = false;
    }
  },
  async mounted() {
    document.title = "Shareish | Items";
    await this.loadItems();
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
}

.column:not(.is-narrow) {
  max-width: 12.5rem;
  min-width: 12.5rem;
}

.vertical-center {
  display: flex;
  flex-direction: row;
  align-items: center;
}
</style>