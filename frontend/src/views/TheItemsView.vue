<template>
  <div id="page-items">
    <div class="columns">
      <div class="column">
        <div id="filters">
          <div class="title has-background-primary p-3 is-size-4 has-text-white">{{ $tc('filter', 0) }}</div>
          <div class="list">
            <div class="search">
              <template v-if="windowWidth >= 1024">
                <b-field :label="$t('search')">
                  <b-input
                      v-model="searchString"
                      :placeholder="$t('name') + ', ' + lcall($t('description')) + ' ' + lcall($t('or')) + ' ' + lcall($t('author'))" />
                </b-field>
              </template>
              <div v-else class="columns is-mobile">
                <div class="column pr-2">
                  <b-field :label="$t('search')">
                    <b-input
                        v-model="searchString"
                        :placeholder="$t('name') + ', ' + lcall($t('description')) + ' ' + lcall($t('or')) + ' ' + lcall($t('author'))" />
                  </b-field>
                </div>
                <div class="column pl-1" style="flex-grow: 0; padding-top: calc(24px + 0.5rem + 0.75rem);">
                  <b-button
                      type="is-primary"
                      :outlined="!isMoreFiltersOpened"
                      @click="isMoreFiltersOpened = !isMoreFiltersOpened">
                    <template v-if="!isMoreFiltersOpened">
                      <template v-if="windowWidth >= 400">
                        {{ $t('show-filters') }}<i class="fas fa-chevron-down ml-2" style="margin-top: -1px; vertical-align: middle;"></i>
                      </template>
                      <template v-else>
                        <i class="fas fa-plus"></i>
                      </template>
                    </template>
                    <template v-else>
                      <template v-if="windowWidth >= 400">
                        {{ $t('hide-filters') }}<i class="fas fa-chevron-up ml-2"></i>
                      </template>
                      <template v-else>
                        <i class="fas fa-times"></i>
                      </template>
                    </template>
                  </b-button>
                </div>
              </div>
            </div>
            <div class="other-filters mt-4" :class="{'is-opened': windowWidth >= 1024 || isMoreFiltersOpened}">
              <toggle-box :title="$tc('type', 0)" outlined :title-size="6" class="mt-3">
                <template v-if="windowWidth >= 768 && windowWidth < 1024">
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
                      @icon-right-click="searchAvailabilityFrom = null"
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
                      @icon-right-click="searchAvailabilityUntil = null"
                      icon-pack="fas"
                      :locale="$i18n.locale"
                  />
                </b-field>
              </toggle-box>
              <toggle-box :title="$t('location')" outlined :title-size="6" class="mt-3">
                <div class="columns is-mobile mb-2">
                  <div class="column is-one-third pr-1">
                    <b-tooltip :label="$t('dont-use-geolocation')" position="is-top" type="is-danger" class="w-100">
                      <b-button
                          expanded
                          @click="locationTypeChosen = 'none'"
                          :outlined="locationTypeChosen !== 'none'"
                          :disabled="locationTypeChosen !== 'none' && locationLoading"
                          :loading="locationTypeChosen === 'none' && locationLoading"
                          type="is-danger"
                      >
                        <i class="fas fa-times"></i>
                      </b-button>
                    </b-tooltip>
                  </div>
                  <div class="column is-one-third pr-1 pl-1">
                    <b-tooltip :label="$t('use-geolocation')" position="is-top" type="is-primary" class="w-100">
                      <b-button
                          expanded
                          @click="locationTypeChosen = 'geoLocation'"
                          :outlined="locationTypeChosen !== 'geoLocation'"
                          :disabled="locationTypeChosen !== 'geoLocation' && locationLoading"
                          :loading="locationTypeChosen === 'geoLocation' && locationLoading"
                          type="is-primary"
                      >
                        <i class="fas fa-street-view"></i>
                      </b-button>
                    </b-tooltip>
                  </div>
                  <div class="column is-one-third pl-1">
                    <b-tooltip :label="$t('use-reflocation')" position="is-top" type="is-info" class="w-100">
                      <b-button
                          expanded
                          @click="locationTypeChosen = 'refLocation'"
                          :outlined="locationTypeChosen !== 'refLocation'"
                          :disabled="locationTypeChosen !== 'refLocation' && locationLoading"
                          :loading="locationTypeChosen === 'refLocation' && locationLoading"
                          type="is-info"
                      >
                        <i class="fas fa-home"></i>
                      </b-button>
                    </b-tooltip>
                  </div>
                </div>
                <b-field :label="$t('or-enter-an-address') + ':'">
                  <b-input v-model="address" :placeholder="$t('address')" />
                </b-field>
                <b-field>
                  <b-switch v-model="restrictDistance" :disabled="searchLocation === null" type="is-primary">{{ $t('restrict-distance') }}</b-switch>
                </b-field>
                <b-field :label="$t('radius-from-location') + ':'" v-if="restrictDistance && searchLocation !== null">
                  <b-slider v-model="distancesRadiusInput" class="pr-5 pl-4" :min="distancesRadiusSlider[0]" :max="distancesRadiusSlider[1]" :step="1" indicator :tooltip="false" />
                </b-field>
              </toggle-box>
              <toggle-box :title="$t('publication')" outlined :title-size="6" class="mt-3">
                <b-field>
                  <b-switch v-model="onlyUnseen" type="is-primary">{{ $t('show-only-unseen') }}</b-switch>
                </b-field>
                <b-field>
                  <b-switch v-model="useMinCreactiondate" type="is-primary">{{ $t('filter-items-creationdate') }}</b-switch>
                </b-field>
                <template v-if="useMinCreactiondate">
                  <div class="columns is-mobile mb-0 mt-3">
                    <div class="column pr-1">
                      <b-slider v-model="sliderTimeUnit" class="pr-5 pl-4" :min="1" :max="sliderTimeUnitMax" :step="1" indicator :tooltip="false" />
                    </div>
                    <div class="column pl-1" style="flex: 0 0 auto;">
                      <b-select v-model="timeUnit" :placeholder="$t('unit')">
                          <option value="days">{{ $tc('day', 0) }}</option>
                          <option value="hours">{{ $tc('hour', 0) }}</option>
                          <option value="minutes">{{ $tc('minute', 0) }}</option>
                      </b-select>
                    </div>
                  </div>
                  <p v-if="timeUnit === 'days'">{{ $t('only-items-created-on') }} <b>{{ formattedDay(minCreationdate) }}</b> {{ $t('or-later-will-be-showed') }}.</p>
                  <p v-else>{{ $t('only-items-created-at') }} <b>{{ formattedHour(minCreationdate) }}</b> {{ $t('on-day') }} <b>{{ formattedDay(minCreationdate) }}</b> {{ $t('or-later-will-be-showed') }}.</p>
                </template>
              </toggle-box>
            </div>
          </div>
        </div>
      </div>
      <div class="column">
        <b-loading v-if="loading" :active="true" :is-full-page="false" />
        <div v-else id="items-list" class="scrollable">
          <header class="columns is-mobile">
            <div class="column">
              <p id="items-match-count">
                <b>{{ items.length }} {{ $tc('item', items.length) }}</b>
                <template v-if="windowWidth > 1180">
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
              <b-field class="wsnw">
                <b-select expanded v-model="orderBy" class="order-by-select">
                  <option value="-creationdate">{{ $t('recent-first') }}</option>
                  <option value="startdate">{{ $t('order-by-availability-startdate') }}</option>
                  <option value="enddate">{{ $t('order-by-availability-enddate') }}</option>
                  <option value="distance">{{ $t('closest-distance') }}</option>
                </b-select>
              </b-field>
            </div>
          </header>
          <div v-if="items && items.length" class="columns is-mobile is-flex-wrap-wrap">
            <div v-for="item in items" :key="item.id" class="column" :class="columnsWidthClass">
              <item-card :item="item" :user-location="searchLocation" />
            </div>
            <div v-if="!loadedAllItems" id="load-more-items" class="column is-narrow">
              <b-button :class="{'is-loading': itemsLoading}" type="is-primary" @click="fetchItems(true)">
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
import {GeolocationCoords, lcall, ucfirst} from "@/functions";
import ToggleBox from "@/components/ToggleBox.vue";
import CategorySelector from "@/components/CategorySelector.vue";
import {categories} from "@/categories";
import moment from "moment/moment";

export default {
  name: 'TheItemsView',
  mixins: [ErrorHandler, WindowSize],
  components: {CategorySelector, ToggleBox, ItemCard},
  data() {
    return {
      isMoreFiltersOpened: false,
      searchString: null,
      searchTypes: ['DN', 'LN', 'RQ', 'EV'],
      searchCategories: [],
      selectedCategory: null,
      searchAvailabilityFrom: null,
      searchAvailabilityUntil: null,
      searchDistancesRadius: null,
      searchLocation: null,
      restrictDistance: false,
      distancesRadiusSlider: [0, 100],
      distancesRadiusInput: [0, 100],
      address: "",
      checkAddress: true,
      geoLocation: null,
      refLocation: null,
      geoLocationAddress: "",
      refLocationAddress: "",
      locationTypeChosen: 'geoLocation',
      locationLoading: false,
      onlyUnseen: false,
      useMinCreactiondate: false,
      timeUnit: 'hours',
      sliderTimeUnitMemory: {
        'days': 1,
        'hours': 1,
        'minutes': 1
      },
      sliderTimeUnitMaximums: {
        'days': 31,
        'hours': 24,
        'minutes': 60
      },
      sliderTimeUnit: 1,
      minCreationdate: new Date(),
      searchMinCreationdate: null,

      orderBy: '-creationdate',
      loading: true,
      itemsLoading: false,
      initialItemsLoadDone: false,
      page: 1,
      nbItemsPerPage: 20,
      loadedAllItems: false,
      columnsWidthClass: null,
      timeouts: {},
      user: {},
      items: []
    }
  },
  computed: {
    params() {
      return {
        search: this.searchString,
        types: this.searchTypes,
        categories: this.searchCategories,
        ordering: this.orderBy,
        onlyNew: (this.onlyUnseen) ? this.onlyUnseen : null,
        availableFrom: this.searchAvailabilityFrom,
        availableUntil: this.searchAvailabilityUntil,
        userLocation: this.searchLocation,
        distancesRadius: (this.searchLocation instanceof GeolocationCoords) ? this.searchDistancesRadius : null,
        minCreationdate: this.searchMinCreationdate
      };
    },
    userId() {
      return Number(this.$store.state.user.id);
    },
    sliderTimeUnitMax() {
      return this.sliderTimeUnitMaximums[this.timeUnit];
    }
  },
  watch: {
    useMinCreactiondate() {
      if (this.useMinCreactiondate)
        this.updateSearchMinCreationdate();
      else
        this.searchMinCreationdate = null;
    },
    timeUnit() {
      this.sliderTimeUnit = this.sliderTimeUnitMemory[this.timeUnit];
      this.updateSearchMinCreationdate();
    },
    sliderTimeUnit() {
      this.sliderTimeUnitMemory[this.timeUnit] = this.sliderTimeUnit;
      this.updateSearchMinCreationdate();
    },
    selectedCategory() {
      if (this.searchCategories.indexOf(this.selectedCategory) === -1)
        this.searchCategories.push(this.selectedCategory);
    },
    locationTypeChosen() {
      clearTimeout(this.timeouts['locationTypeChosen']);
      this.locationLoading = true;
      this.timeouts['locationTypeChosen'] = setTimeout(() => {
        switch (this.locationTypeChosen) {
          case 'geoLocation':
            this.checkAddress = false;
            this.address = this.geoLocationAddress;
            this.searchLocation = this.geoLocation;
            break;
          case 'refLocation':
            this.checkAddress = false;
            this.address = this.refLocationAddress;
            this.searchLocation = this.refLocation;
            break;
          case 'none':
            this.checkAddress = false;
            this.address = "";
            this.searchLocation = null;
            break;
        }
        this.locationLoading = false;
      }, 600);
    },
    address() {
      if (this.checkAddress) {
        clearTimeout(this.timeouts['address']);
        this.timeouts['address'] = setTimeout(() => {
          this.updateGeolocationFromAddress();
        }, 1000);
      } else {
        this.checkAddress = true;
      }
    },
    restrictDistance() {
      this.locationLoading = true;
      clearTimeout(this.timeouts['restrictDistance']);
      this.timeouts['restrictDistance'] = setTimeout(() => {
        if (this.restrictDistance)
          this.searchDistancesRadius = this.distancesRadiusInput;
        else
          this.searchDistancesRadius = null;
        this.locationLoading = false;
      }, 600);
    },
    distancesRadiusInput() {
      if (this.restrictDistance) {
        clearTimeout(this.timeouts['distancesRadius']);
        this.timeouts['distancesRadius'] = setTimeout(() => {
          this.searchDistancesRadius = this.distancesRadiusInput;
        }, 600);
      }
    },
    params() {
      if (this.initialItemsLoadDone)
        this.fetchItems();
    }
  },
  methods: {
    ucfirst,
    lcall,
    updateSearchMinCreationdate() {
      this.minCreationdate = this.getMinCreationdate();

      clearTimeout(this.timeouts['searchMinCreationdate']);
      this.timeouts['searchMinCreationdate'] = setTimeout(() => {
        this.searchMinCreationdate = this.minCreationdate;
      }, 600);
    },
    getMinCreationdate() {
      let minCreationdate = new Date();

      switch (this.timeUnit) {
        case 'days':
          minCreationdate.setDate(minCreationdate.getDate() - this.sliderTimeUnit);
          minCreationdate.setHours(0);
          minCreationdate.setMinutes(0);
          break;
        case 'hours':
          minCreationdate.setHours(minCreationdate.getHours() - this.sliderTimeUnit);
          minCreationdate.setMinutes(0);
          break;
        case 'minutes':
          minCreationdate.setMinutes(minCreationdate.getMinutes() - this.sliderTimeUnit);
          break;
      }
      minCreationdate.setSeconds(0);
      minCreationdate.setMilliseconds(0);

      return minCreationdate;
    },
    formattedDay(date) {
      return (moment(date).locale(this.$i18n.locale).format("DD/MM/YYYY"));
    },
    formattedHour(date) {
      return (moment(date).locale(this.$i18n.locale).format("HH:mm"));
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
      if (bottom && !this.loadedAllItems)
        this.fetchItems(true);
    }, 100),
    async fetchItems(append = false) {
      this.itemsLoading = true;
      try {
        if (!append) {
          this.page = 1;
          this.loadedAllItems = false;
        } else {
          this.page += 1;
        }

        const items = (await axios.get("/api/v1/actives/", {params: {page: this.page, ...this.params}})).data;

        if (!append)
          this.items = items.results;
        else
          this.items.push(...items.results);

        if (items.next === null)
          this.loadedAllItems = true;
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
    },
    async fetchUser() {
      try {
        const params = {
          columns: ['ref_location']
        }
        this.user = (await axios.get(`api/v1/webusers/${this.userId}`, {params: params})).data;
        if (this.user.ref_location !== null)
          this.refLocation = new GeolocationCoords(this.user.ref_location);
      }
      catch (error) {
        this.snackbarError(error);
      }
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
      if (address !== null && address !== "") {
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
      if (this.address !== "") {
        const geolocation = await this.fetchGeolocation(this.address);
        if (geolocation !== null)
          this.searchLocation = new GeolocationCoords(geolocation)
        else
          this.searchLocation = null;
      } else {
        this.searchLocation = null;
      }
    }
  },
  async mounted() {
    document.title = `Shareish | ${this.$t('items')}`;

    await this.fetchUser();

    this.geoLocationAddress = await this.fetchAddress(this.geoLocation);
    this.refLocationAddress = await this.fetchAddress(this.refLocation);

    if (this.locationTypeChosen === 'geoLocation') {
      this.checkAddress = false;
      this.address = this.geoLocationAddress;
      this.searchLocation = this.geoLocation;
    } else if (this.locationTypeChosen === 'refLocation') {
      this.checkAddress = false;
      this.address = this.refLocationAddress;
      this.searchLocation = this.refLocation;
    }

    await this.fetchItems();

    this.initialItemsLoadDone = true;

    this.loading = false;

    this.$nextTick(() => {
      const itemsList = document.getElementById("items-list");
      if (itemsList !== null) {
        const resizeObserver = new ResizeObserver((entries) => {
          for (const entry of entries)
            this.itemListWidthChanged(entry.contentRect.width);
        });
        resizeObserver.observe(itemsList);
      }
    });
  },
  created() {
    // Has the user activated geolocation?
    if ('geolocation' in navigator) {
      // Get the position
      navigator.geolocation.getCurrentPosition(
        position => {
          this.geoLocation = new GeolocationCoords(position);
        },
        null,
        {
          maximumAge: 10000,
          timeout: 5000,
          enableHighAccuracy: true
        }
      );
    }

    window.addEventListener('scroll', this.scrollHandler);
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

#items-list header {
  .order-by-label {
    height: 40px;
    line-height: 40px;
    margin-right: 0.5rem;
    font-weight: bold;
  }
  .order-by-select {
    width: 200px;
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

@media screen and (max-width: 1350px) {
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

    .other-filters:not(.is-opened) {
      display: none;
    }
  }
}

@media screen and (max-width: 600px) {
  #items-list header .order-by-label {
    display: none;
  }
}

@media screen and (max-width: 499px) {
  #filters {
    margin-bottom: 0.25rem;
  }

  #items-list header {
    display: block;

    & > .column {
      width: 100%;
      padding: 0 0.75rem;

      &:last-child {
        display: flex;
        margin-bottom: 0.75rem;

        .field {
          flex-basis: 100%;
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
}
</style>
