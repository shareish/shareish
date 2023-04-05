<template>
  <div id="page-items">
    <b-loading v-if="loading" :active="true" :is-full-page="false" />
    <div v-else class="columns">
      <div class="column">
        <div id="filters">
          <div class="title has-background-primary p-3 is-size-4 has-text-white">{{ $tc('filter', 0) }}</div>
          <div class="list">
            <div class="search mb-4">
              <b-field :label="$t('search')">
                <b-input v-model="searchString" :placeholder="$t('name') + ', ' + lcall($t('description')) + ' ' + lcall($t('or')) + ' ' + lcall($t('author'))" />
              </b-field>
            </div>
            <div class="columns mb-3">
              <div class="column is-half pr-2">
                <b-button type="is-primary" :outlined="onlyNew" @click="onlyNew = false" expanded>
                  {{ ucfirst($t('all')) }}
                </b-button>
              </div>
              <div class="column is-half pl-2">
                <b-button type="is-purple" :outlined="!onlyNew" @click="onlyNew = true" expanded>
                  <i class="far fa-star mr-1"></i>
                  {{ $t('only-new') }}
                </b-button>
              </div>
            </div>
            <label class="label mb-2">{{ $t('more-filters') }}</label>
            <toggle-box :title="$tc('type', 0)" outlined :title-size="6" class="mb-3">
              <b-field class="mb-1">
                <b-checkbox-button v-model="searchTypes" native-value="DN" type="is-success">
                  <span>{{ $t('donation') }}</span>
                </b-checkbox-button>
              </b-field>
              <b-field class="mb-1">
                <b-checkbox-button v-model="searchTypes" native-value="RQ" type="is-danger">
                  <span>{{ $t('request') }}</span>
                </b-checkbox-button>
              </b-field>
              <b-field class="mb-1">
                <b-checkbox-button v-model="searchTypes" native-value="LN" type="is-warning">
                  <span>{{ $t('loan') }}</span>
                </b-checkbox-button>
              </b-field>
              <b-field class="mb-1">
                <b-checkbox-button v-model="searchTypes" native-value="EV" type="is-purple">
                  <span>{{ $t('event') }}</span>
                </b-checkbox-button>
              </b-field>
            </toggle-box>
            <toggle-box :title="$tc('category', 0)" outlined :title-size="6">
              <div v-if="searchCategories.length > 0" id="selected-categories">
                <p class="has-text-weight-bold mb-2">{{ $t('searched-categories') }}:</p>
                <div v-for="category in searchCategories" :key="category" class="selected-category columns is-mobile">
                  <div class="column name">{{ getCategory(category) }}</div>
                  <div class="column close" @click="removeCategory(category)"><i class="fas fa-times-circle"></i></div>
                </div>
              </div>
              <template v-else>
                <p class="mb-2"><small>{{ $t('no-categories-selected-for-search') }}</small></p>
              </template>
              <category-selector v-model="selectedCategory" />
            </toggle-box>
          </div>
        </div>
      </div>
      <div class="column">
        <div ref="listItems" class="scrollable">
          <div v-if="items && items.length" class="columns is-mobile is-flex-wrap-wrap">
            <div v-for="item in items" :key="item.id" class="column" :class="columnsWidthClass">
              <item-card :item="item" />
            </div>
            <div v-if="!loadedAllItems" class="column is-narrow vertical-center">
              <b-button v-if="!loadedAllItems" :class="{'is-loading': itemsLoading}" type="is-primary" @click="loadItems()">
                {{ $t('button-load-more') }}
              </b-button>
            </div>
          </div>
          <div v-else>{{ $t('no-items') }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import _ from "lodash";
import axios from "axios";
import ItemCard from "@/components/ItemCard.vue";
import ErrorHandler from "@/mixins/ErrorHandler";
import WindowSize from "@/mixins/WindowSize";
import {lcall, ucfirst} from "@/functions";
import ToggleBox from "@/components/ToggleBox.vue";
import CategorySelector from "@/components/CategorySelector.vue";
import {categories} from "@/categories";

export default {
  name: 'TheItemsView',
  mixins: [ErrorHandler, WindowSize],
  components: {CategorySelector, ToggleBox, ItemCard},
  data() {
    return {
      searchString: null,
      searchTypes: [],
      searchCategories: [],
      selectedCategory: null,
      onlyNew: false,

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
        types: this.searchTypes,
        categories: this.searchCategories,
        onlyNew: this.onlyNew
      };
    }
  },
  watch: {
    params() {
      this.loadItems(false);
    },
    selectedCategory() {
      if (this.searchCategories.indexOf(this.selectedCategory) === -1) {
        this.searchCategories.push(this.selectedCategory);
      }
    }
  },
  methods: {
    ucfirst,
    lcall,
    getCategory(category) {
      if (category in categories) {
        return this.$t(categories[category]['slug']);
      }
      return "";
    },
    removeCategory(category) {
      const index = this.searchCategories.indexOf(category);
      if (index > -1)
        this.searchCategories.splice(index, 1);
    },
    scrollHandler: _.debounce(function () {
      let scrollBlock = document.getElementById('wrapper');
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
      }

      try {
        const data = (await axios.get("/api/v1/actives/", {params: {page: this.page, ...this.params}})).data;

        if (!append) {
          this.items = data.results;
        } else {
          this.items.push(...data.results);
        }
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

<style lang="scss" scoped>
$filtersWidth: 400px;

.vertical-center {
  display: flex;
  flex-direction: row;
  align-items: center;
}

#page-items {
  & > .columns {
    & > .column:first-child {
      flex: 0 0 400px;

      #filters {
        border-radius: 5px;
        overflow: hidden;
        box-shadow: 0 0.5em 1em -0.125em rgba(10, 10, 10, 0.1), 0 0 0 1px rgba(10, 10, 10, 0.02);
        max-width: calc(#{$filtersWidth} - 2 * 0.75rem);

        .title {
          margin-bottom: 0;
        }

        .list {
          padding: 0.75rem;
        }

        #selected-categories {
          .selected-category {
            padding: 0;
            margin: 0 0 5px 0;
            font-size: 0.75rem;
            background-color: white;
            border-radius: 5px;

            .column.name {
              flex: 0 0 calc(400px - 0.75rem * 6 - 40px - 2px);
              padding: 10px;
              white-space: nowrap;
              text-overflow: ellipsis;
              overflow: hidden;
            }

            .column.close {
              flex: 0 0 40px;
              padding: 10px;
              text-align: center;
              cursor: pointer;

              i {
                vertical-align: middle;
              }
            }

            &:last-child {
              margin-bottom: 0.75rem !important;
            }
          }
        }
      }
    }
  }
}
</style>
