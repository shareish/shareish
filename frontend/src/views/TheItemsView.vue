<template>
  <div id="page-items">
    <b-loading v-if="loading" :active="true" :is-full-page="false" />
    <div v-else class="columns">
      <div class="column">
        <div id="filters">
          <div class="title has-background-primary p-3 is-size-4 has-text-white">{{ $tc('filter', 0) }}</div>
          <div class="list">
            <div class="search">
              <b-field v-if="windowWidth >= 1024" :label="$t('search')">
                <b-input v-model="searchString" :placeholder="$t('name') + ', ' + lcall($t('description')) + ' ' + lcall($t('or')) + ' ' + lcall($t('author'))" />
              </b-field>
              <div v-else class="columns is-mobile">
                <div class="column pr-2">
                  <b-field :label="$t('search')">
                    <b-input v-model="searchString" :placeholder="$t('name') + ', ' + lcall($t('description')) + ' ' + lcall($t('or')) + ' ' + lcall($t('author'))" />
                  </b-field>
                </div>
                <div class="column pl-1" style="flex-grow: 0; padding-top: calc(24px + 0.5rem + 0.75rem);">
                  <b-button
                      type="is-primary"
                      :outlined="!isMoreFiltersOpened"
                      @click="isMoreFiltersOpened = !isMoreFiltersOpened">
                    <template v-if="!isMoreFiltersOpened">
                      <template v-if="windowWidth >= 400">
                        {{ $t('show-filters') }}
                      </template>
                      <template v-else>
                        <i class="fas fa-plus"></i>
                      </template>
                    </template>
                    <template v-else>
                      <template v-if="windowWidth >= 400">
                        {{ $t('show-filters') }}
                      </template>
                      <template v-else>
                        <i class="fas fa-times"></i>
                      </template>
                    </template>
                  </b-button>
                </div>
              </div>
            </div>
            <div class="more-filters mt-4" :class="{'is-opened': windowWidth >= 1024 || isMoreFiltersOpened}">
              <label class="label">{{ $t('more-filters') }}</label>
              <div class="columns is-mobile mt-2">
                <div class="column is-half pr-1 pb-0 pt-0">
                  <b-button type="is-primary" :outlined="onlyNew" @click="onlyNew = false" expanded>
                    {{ ucfirst($t('all')) }}
                  </b-button>
                </div>
                <div class="column is-half pl-1 pb-0 pt-0">
                  <b-button type="is-purple" :outlined="!onlyNew" @click="onlyNew = true" expanded>
                    <i class="far fa-star mr-1"></i>
                    <template v-if="windowWidth >= 360">
                      {{ $t('only-new') }}
                    </template>
                  </b-button>
                </div>
              </div>
              <toggle-box :title="$tc('type', 0)" outlined :title-size="6" class="mt-3">
                <template v-if="windowWidth >= 768">
                  <div class="columns is-mobile">
                    <div class="column pr-2">
                      <b-field class="mb-1">
                        <b-checkbox-button v-model="searchTypes" native-value="DN" type="is-success">
                          <span>{{ $t('donation') }}</span>
                        </b-checkbox-button>
                      </b-field>
                    </div>
                    <div class="column pr-2 pl-2">
                      <b-field class="mb-1">
                        <b-checkbox-button v-model="searchTypes" native-value="RQ" type="is-danger">
                          <span>{{ $t('request') }}</span>
                        </b-checkbox-button>
                      </b-field>
                    </div>
                    <div class="column pr-2 pl-2">
                      <b-field class="mb-1">
                        <b-checkbox-button v-model="searchTypes" native-value="LN" type="is-warning">
                          <span>{{ $t('loan') }}</span>
                        </b-checkbox-button>
                      </b-field>
                    </div>
                    <div class="column pl-2">
                      <b-field class="mb-1">
                        <b-checkbox-button v-model="searchTypes" native-value="EV" type="is-purple">
                          <span>{{ $t('event') }}</span>
                        </b-checkbox-button>
                      </b-field>
                    </div>
                  </div>
                </template>
                <template v-else>
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
                </template>
              </toggle-box>
              <toggle-box :title="$tc('category', 0)" outlined :title-size="6" class="mt-3">
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
                <category-selector v-model="selectedCategory" expanded />
              </toggle-box>
              <toggle-box :title="$t('availability')" outlined :title-size="6" class="mt-3">
                <b-field :label="$t('from')">
                  <b-datetimepicker
                      v-model="searchAvailabilityFrom"
                      icon="calendar"
                      :icon-right="searchAvailabilityFrom ? 'close-circle' : ''"
                      icon-right-clickable
                      @icon-right-click="clearDate('searchAvailabilityFrom')"
                      icon-pack="fas"
                      :locale="$i18n.locale"
                  />
                </b-field>
                <b-field :label="$t('until')">
                  <b-datetimepicker
                      v-model="searchAvailabilityUntil"
                      icon="calendar"
                      :icon-right="searchAvailabilityUntil ? 'close-circle' : ''"
                      icon-right-clickable
                      @icon-right-click="clearDate('searchAvailabilityUntil')"
                      icon-pack="fas"
                      :locale="$i18n.locale"
                  />
                </b-field>
              </toggle-box>
            </div>
          </div>
        </div>
      </div>
      <div class="column">
        <div id="items-list" class="scrollable">
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
      searchAvailabilityFrom: null,
      searchAvailabilityUntil: null,

      loading: false,
      itemsLoading: false,
      page: 1,
      nbItemsPerPage: 20,
      loadedAllItems: false,
      columnsWidthClass: null,
      isMoreFiltersOpened: false,

      items: []
    }
  },
  computed: {
    params() {
      return {
        search: this.searchString,
        types: this.searchTypes,
        categories: this.searchCategories,
        onlyNew: (this.onlyNew) ? this.onlyNew : null,
        availableFrom: this.searchAvailabilityFrom,
        availableUntil: this.searchAvailabilityUntil
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
    },
    searchStartdateFrom() {
      console.log("test 1");
    },
    searchStartdateUntil() {
      console.log("test 2");
    }
  },
  methods: {
    ucfirst,
    lcall,
    clearDate(name) {
      switch (name) {
        case "searchAvailabilityFrom":
          this.searchAvailabilityFrom = null;
          break;
        case "searchAvailabilityUntil":
          this.searchAvailabilityUntil = null;
          break;
      }
    },
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
    itemListWidthChanged(width) {
      // Below or equal 520
      let columnsWidthClass = "is-full";
      if (width > 550) { // Arbitrary
        columnsWidthClass = "is-half";
        if (width > 768) { // Over PAL* (768x576)
          columnsWidthClass = "is-one-third";
          if (width > 1152) { // Over XGA+ (1152x864)
            columnsWidthClass = "is-one-quarter";
            if (width > 1600) { // Over UXGA (1600x1200)
              columnsWidthClass = "is-one-fifth";
              if (width > 2560) { // Over WQHD (2560x1440)
                columnsWidthClass = "is-2";
                if (width > 3840) { // Over UHD-1 (3840x2160)
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
  mounted() {
    document.title = `Shareish | ${this.$t('items')}`;
    this.loadItems();

    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries)
        this.itemListWidthChanged(entry.contentRect.width);
    });
    const itemsList = document.getElementById("items-list");
    resizeObserver.observe(itemsList);
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
      flex: 0 0 $filtersWidth;
      max-width: $filtersWidth;

      #filters {
        border-radius: 5px;
        box-shadow: 0 0.5em 1em -0.125em rgba(10, 10, 10, 0.1), 0 0 0 1px rgba(10, 10, 10, 0.02);
        max-width: calc(#{$filtersWidth} - 2 * 0.75rem);

        .title {
          margin-bottom: 0;
          border-radius: 5px 5px 0 0;
        }

        .list {
          padding: 0.75rem;
          border-radius: 0 0 5px 5px;
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

@media screen and (max-width: 1215px) and (min-width: 1024px) {
  $filtersWidth: 360px;

  #page-items > .columns > .column:first-child {
      flex: 0 0 $filtersWidth;
      max-width: $filtersWidth;
  }
}

@media screen and (max-width: 1023px) {
  $filtersWidth: 100%;

  #page-items > .columns {
    display: block;

    & > .column:first-child {
      flex: 0 0 $filtersWidth;
      max-width: $filtersWidth;
    }
  }

  #filters {
    min-width: $filtersWidth;

    .more-filters:not(.is-opened) {
      display: none;
    }
  }
}
</style>
