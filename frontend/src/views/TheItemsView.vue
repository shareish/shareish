<template>
  <div id="page-items">
    <div class="columns">
      <div class="column">
        <item-filters
            @fieldsUpdated="itemFiltersUpdated"
            rewrite-url-page-name="items"
            :limited-vertical-space="windowWidth < 1024"
        />
      </div>
      <div class="column is-relative" id="items-list-container">
        <b-loading v-if="firstItemsLoaded === false" :active="true" :is-full-page="false" />
        <div v-else id="items-list" class="scrollable">
          <header class="columns is-mobile">
            <div class="column">
              <p id="items-match-count">
                <b>{{ items.length }} {{ $tc('item', items.length) }}</b>
                <template v-if="windowWidth > 1350">
                  {{ $tc('corresponding-to-search', items.length) }}
                </template>
                <template v-else>
                  {{ $tc('found', items.length) }}
                </template>
              </p>
            </div>
            <div class="column" style="flex: 0 0 auto; display: inline-flex;">
              <div class="order-by-label">
                <i class="fas fa-sort mr-1"></i>
                {{ $t('order-by') }}
              </div>
              <b-field class="wsnw is-small">
                <b-select expanded v-model="input_orderBy" class="order-by-select">
                  <option value="creationdate">{{ $t('creationdate') }}</option>
                  <option value="startdate">{{ $t('startdate') }}</option>
                  <option value="enddate">{{ $t('enddate') }}</option>
                  <option value="distance">{{ $t('distance') }}</option>
                </b-select>
              </b-field>
              <b-field class="wsnw ml-1 is-small">
                <b-select expanded v-model="input_orderByDirection" class="order-by-direction-select">
                  <option
                      v-for="orderByAddition in orderByData[input_orderBy]"
                      :key="orderByAddition['direction']"
                      :value="orderByAddition['direction']"
                  >
                    {{ $t(orderByAddition['label']) }}
                  </option>
                </b-select>
              </b-field>
            </div>
          </header>
          <div v-if="items && items.length" class="columns is-mobile is-flex-wrap-wrap">
            <div v-for="item in items" :key="item.id" class="column" :class="columnsWidthClass">
              <item-card :item="item" :user-location="userLocation" />
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
import {
  GeolocationCoords,
  isNotEmptyString,
  lcall,
  ucfirst
} from "@/functions";
import ItemFilters from "@/components/ItemFilters.vue";

export default {
  name: 'TheItemsView',
  mixins: [ErrorHandler, WindowSize],
  components: {ItemFilters, ItemCard},
  data() {
    return {
      userLocation: null,
      input_orderBy: null,
      input_orderByDirection: null,
      orderByData: {
        'creationdate': [
          {
            'direction': '-',
            'label': 'recent-first'
          },
          {
            'direction': '',
            'label': 'oldest-first'
          }
        ],
        'startdate': [
          {
            'direction': '',
            'label': 'starting-soon-first'
          },
          {
            'direction': '-',
            'label': 'starting-late-first'
          }
        ],
        'enddate': [
          {
            'direction': '',
            'label': 'ending-soon-first'
          },
          {
            'direction': '-',
            'label': 'ending-late-first'
          }
        ],
        'distance': [
          {
            'direction': '',
            'label': 'closest-first'
          },
          {
            'direction': '-',
            'label': 'furthest-first'
          }
        ]
      },
      filteredQueryValues: {},
      builtURLParams: {},
      skipActions: [],

      lastQueryDatetime: null,
      page: 1,
      firstItemsLoaded: false,
      loadedAllItems: false,
      columnsWidthClass: null,
      timeouts: {},
      user: {},
      items: []
    }
  },
  created() {
    // Has the user activated geolocation?
    if ('geolocation' in navigator) {
      // Get the position
      navigator.geolocation.getCurrentPosition(
        position => {
          this.geoLocation = new GeolocationCoords(position);
          this.input_locationType = (this.$route.query['lt']) ? this.$route.query['lt'] : 'geoLocation';
        },
        null,
        {
          maximumAge: 10000,
          timeout: 5000,
          enableHighAccuracy: true
        }
      );
    }

    let ordering = null;
    if ('ordering' in this.$route.query)
      ordering = this.$route.query['ordering'];
    else if ('ordering' in this.$store.state.itemsFilters)
      ordering = this.$store.state.itemsFilters['ordering'];

    if (ordering !== null) {
      const issetDash = ordering.substring(0, 1) === '-';
      this.input_orderBy = issetDash ? ordering.substring(1) : ordering;
      this.input_orderByDirection = issetDash ? '-' : '';
    } else {
      this.input_orderBy = 'creationdate';
      this.input_orderByDirection = '-';
    }

    this.builtURLParams['ordering'] = this.ordering;
    this.$store.commit('setItemsFilters', this.builtURLParams);

    window.addEventListener('scroll', this.scrollHandler);
  },
  async mounted() {
    document.title = `Shareish | ${this.$t('items')}`;

    this.$nextTick(() => {
      const itemsList = document.getElementById("items-list-container");
      if (itemsList !== null) {
        const resizeObserver = new ResizeObserver((entries) => {
          for (const entry of entries)
            this.itemListWidthChanged(entry.contentRect.width);
        });
        resizeObserver.observe(itemsList);
      }
    });
  },
  watch: {
    input_orderBy() {
      if (this.firstItemsLoaded)
        this.input_orderByDirection = this.orderByData[this.input_orderBy][0]['direction'];
    },
    ordering() {
      this.builtURLParams['ordering'] = this.ordering;
      this.$store.commit('setItemsFilters', this.builtURLParams);
      this.rewriteURL();
      if (this.firstItemsLoaded)
        this.fetchItems(false);
    }
  },
  computed: {
    ordering() {
      return this.input_orderByDirection + this.input_orderBy;
    }
  },
  methods: {
    ucfirst,
    lcall,
    rewriteURL() {
      clearTimeout(this.timeouts['rewriteURL']);
      this.timeouts['rewriteURL'] = setTimeout(async () => {
        try {
          await this.$router.push({name: 'items', query: this.builtURLParams});
        } catch (error) {
          console.log("Redirected on same URL.");
        }
      }, 100);
    },
    itemFiltersUpdated(filteredQueryValues, builtURLParams) {
      this.builtURLParams = {...builtURLParams, ordering: this.ordering};
      this.rewriteURL();

      this.$store.commit('setItemsFilters', this.builtURLParams);

      clearTimeout(this.timeouts['itemFiltersUpdated']);
      this.timeouts['itemFiltersUpdated'] = setTimeout(() => {
        // Adding/removing query params external of items filters component
        // Setting the user location that is used in the ItemCards
        filteredQueryValues['ordering'] = this.input_orderBy;
        if ('userLocation' in filteredQueryValues) {
          this.userLocation = filteredQueryValues['userLocation'];
        } else {
          this.userLocation = null;
        }
        this.filteredQueryValues = filteredQueryValues;

        this.fetchItems(false);
      }, 600);
    },
    scrollHandler: _.debounce(function () {
      let scrollBlock = document.getElementById('wrapper');
      let bottom = (scrollBlock.scrollTop + scrollBlock.clientHeight >= scrollBlock.scrollHeight);
      if (bottom && !this.loadedAllItems)
        this.fetchItems(true);
    }, 100),
    async fetchItems(append = false) {
      this.lastQueryDatetime = new Date();

      try {
        if (!append) {
          this.page = 1;
          this.loadedAllItems = false;
        } else {
          this.page += 1;
        }

        const params = {
          page: this.page,
          ...this.filteredQueryValues,
          ordering: this.ordering
        };

        const restrictDistance = 'distancesRadius' in params;
        if (!restrictDistance && this.input_orderBy !== 'distance')
          delete params['userLocation']

        const items = (await axios.get("/api/v1/actives/", {params: params})).data;

        if (!append)
          this.items = items.results;
        else
          this.items.push(...items.results);

        if (items.next === null)
          this.loadedAllItems = true;

        if (!this.firstItemsLoaded)
          this.firstItemsLoaded = true;
      }
      catch (error) {
        this.snackbarError(error);
      }
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
    },
    async fetchAddress(location) {
      if (location instanceof GeolocationCoords) {
        try {
          return (await axios.post("/api/v1/address/reverse", location)).data;
        }
        catch (error) {
          this.fullErrorHandling(error);
        }
      }
      return null;
    },
    async fetchGeolocation(address) {
      if (isNotEmptyString(address)) {
        try {
          const formData = new FormData();
          formData.append('address', address);
          return (await axios.post("/api/v1/address", formData)).data;
        }
        catch (error) {
          this.fullErrorHandling(error);
        }
      }
      return null;
    },
    async updateGeolocationFromAddress() {
      if (isNotEmptyString(this.input_address)) {
        const geolocation = await this.fetchGeolocation(this.input_address);
        if (geolocation !== null)
          this.input_location = new GeolocationCoords(geolocation)
        else
          this.input_location = null;
      } else {
        this.input_location = null;
      }
    }
  },
  destroyed: function () {
    window.removeEventListener('scroll', this.scrollHandler);
    for (let i in this.timeouts)
      clearTimeout(this.timeouts[i]);
  }
};
</script>

<style lang="scss" scoped>
$filtersWidth: 400px;

#page-items > .columns > .column:first-child {
  flex: 0 0 $filtersWidth;
  max-width: $filtersWidth;
}

#items-list header {
  .order-by-label {
    height: 40px;
    line-height: 40px;
    margin-right: 0.5rem;
    font-weight: bold;
  }
  .order-by-select {
    width: 140px;
  }
  .order-by-direction-select {
    width: 210px;
  }
}

#items-match-count {
  height: 40px;
  line-height: 40px;
  font-size: 1.3em;
}

#load-more-items {
  display: flex;
  align-items: center;
}

@media screen and (max-width: 1450px) {
  #items-match-count {
    font-size: 1.1em;
  }
}

@media screen and (max-width: 1215px) and (min-width: 1024px) {
  $filtersWidth: 360px;

  #page-items > .columns > .column:first-child {
      flex: 0 0 $filtersWidth;
      max-width: $filtersWidth;
  }
}

@media screen and (max-width: 1120px) and (min-width: 1024px) {
  #items-list header .order-by-label {
    display: none;
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
}

@media screen and (max-width: 700px) {
  #items-list header .order-by-label {
    display: none;
  }
}

@media screen and (max-width: 600px) {
  #items-list header {
    display: block;
  }
}

@media screen and (max-width: 499px) {
  #items-list header > .column {
    width: 100%;
    padding: 0 0.75rem;

    &:last-child {
      display: flex;
      margin-bottom: 0.75rem;

      .field:last-child {
        flex-basis: 100%;

        .order-by-direction-select {
          width: 100%;
        }
      }
    }
  }
  .order-by-label {
    flex: 0 0 auto;
    display: block;
  }

  .order-by-select {
    width: 100%;
  }
}
</style>