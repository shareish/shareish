<template>
  <div id="filters-surrounding" :class="{'inputs-loaded': inputsLoaded}">
    <b-loading v-if="!inputsLoaded" :active="true" :is-full-page="false" />
    <div v-else id="filters" :class="{'boxed': boxed}">
      <template v-if="componentWidth !== null">
        <div v-if="boxed" class="title has-background-primary p-3 is-size-4 has-text-white">{{ $tc('filter', 0) }}</div>
        <div class="list">
          <div class="search">
            <template v-if="!limitedVerticalSpace">
              <b-field :label="$t('search')">
                <b-input
                    v-model="input_search"
                    :placeholder="$t('name') + ', ' + lcall($t('description')) + ' ' + lcall($t('or')) + ' ' + lcall($t('author'))" />
              </b-field>
            </template>
            <div v-else class="columns is-mobile">
              <div class="column pr-2">
                <b-field :label="$t('search')">
                  <b-input
                      v-model="input_search"
                      :placeholder="$t('name') + ', ' + lcall($t('description')) + ' ' + lcall($t('or')) + ' ' + lcall($t('author'))" />
                </b-field>
              </div>
              <div class="column pl-1" style="flex-grow: 0; padding-top: calc(24px + 0.5rem + 0.75rem);">
                <b-button
                    type="is-primary"
                    :outlined="!isMoreFiltersOpened"
                    @click="isMoreFiltersOpened = !isMoreFiltersOpened">
                  <template v-if="!isMoreFiltersOpened">
                    <template v-if="componentWidth >= 400">
                      {{ $t('show-filters') }}<i class="fas fa-chevron-down ml-2" style="margin-top: -1px; vertical-align: middle;"></i>
                    </template>
                    <template v-else>
                      <i class="fas fa-plus"></i>
                    </template>
                  </template>
                  <template v-else>
                    <template v-if="componentWidth >= 400">
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
          <div class="other-filters mt-4" :class="{'is-opened': componentWidth >= 1024 || isMoreFiltersOpened || !limitedVerticalSpace}">
            <toggle-box v-if="typesFilter" :title="$tc('type', 0)" outlined :title-size="6" class="mt-3">
              <template v-if="componentWidth >= 600">
                <div class="columns is-mobile">
                  <div class="column pr-2">
                    <b-field class="mb-1">
                      <b-checkbox-button v-model="input_types" native-value="DN" type="is-success">
                        <span>{{ $t('donation') }}</span>
                      </b-checkbox-button>
                    </b-field>
                  </div>
                  <div class="column pr-2 pl-2">
                    <b-field class="mb-1">
                      <b-checkbox-button v-model="input_types" native-value="RQ" type="is-danger">
                        <span>{{ $t('request') }}</span>
                      </b-checkbox-button>
                    </b-field>
                  </div>
                  <div class="column pr-2 pl-2">
                    <b-field class="mb-1">
                      <b-checkbox-button v-model="input_types" native-value="LN" type="is-warning">
                        <span>{{ $t('loan') }}</span>
                      </b-checkbox-button>
                    </b-field>
                  </div>
                  <div class="column pl-2">
                    <b-field class="mb-1">
                      <b-checkbox-button v-model="input_types" native-value="EV" type="is-purple">
                        <span>{{ $t('event') }}</span>
                      </b-checkbox-button>
                    </b-field>
                  </div>
                </div>
              </template>
              <template v-else>
                <b-field class="mb-1">
                  <b-checkbox-button v-model="input_types" native-value="DN" type="is-success">
                    <span>{{ $t('donation') }}</span>
                  </b-checkbox-button>
                </b-field>
                <b-field class="mb-1">
                  <b-checkbox-button v-model="input_types" native-value="RQ" type="is-danger">
                    <span>{{ $t('request') }}</span>
                  </b-checkbox-button>
                </b-field>
                <b-field class="mb-1">
                  <b-checkbox-button v-model="input_types" native-value="LN" type="is-warning">
                    <span>{{ $t('loan') }}</span>
                  </b-checkbox-button>
                </b-field>
                <b-field class="mb-1">
                  <b-checkbox-button v-model="input_types" native-value="EV" type="is-purple">
                    <span>{{ $t('event') }}</span>
                  </b-checkbox-button>
                </b-field>
              </template>
            </toggle-box>
            <toggle-box v-if="categoriesFilter" :title="$tc('category', 0)" outlined :title-size="6" class="mt-3">
              <div v-if="input_categories.length > 0" id="selected-categories">
                <p class="has-text-weight-bold mb-2">{{ $t('searched-categories') }}:</p>
                <div v-for="category in input_categories" :key="category" class="selected-category columns is-mobile">
                  <div class="column name">{{ getCategory(category) }}</div>
                  <div class="column close" @click="removeCategory(category)"><i class="fas fa-times-circle"></i></div>
                </div>
              </div>
              <template v-else>
                <p class="mb-2"><small>{{ $t('no-categories-selected-for-search') }}</small></p>
              </template>
              <category-selector v-model="selectedCategory" expanded />
            </toggle-box>
            <toggle-box v-if="availabilityFilter" :title="$t('availability')" outlined :title-size="6" class="mt-3">
              <b-field :label="$t('from')">
                <b-datetimepicker
                    v-model="input_availableFrom"
                    icon="calendar"
                    :icon-right="input_availableFrom ? 'close-circle' : ''"
                    icon-right-clickable
                    @icon-right-click="input_availableFrom = null"
                    icon-pack="fas"
                    :locale="$i18n.locale"
                />
              </b-field>
              <b-switch v-model="input_includeAfterAvailableFrom" :disabled="!(input_availableFrom instanceof Date)" class="mb-5">
                <small>Include items that starts after this date</small>
              </b-switch>
              <b-field :label="$t('until')">
                <b-datetimepicker
                    v-model="input_availableUntil"
                    icon="calendar"
                    :icon-right="input_availableUntil ? 'close-circle' : ''"
                    icon-right-clickable
                    @icon-right-click="input_availableUntil = null"
                    icon-pack="fas"
                    :locale="$i18n.locale"
                />
              </b-field>
              <b-switch v-model="input_includeBeforeAvailableUntil" :disabled="!(input_availableUntil instanceof Date)">
                <small>Include items that ends before this date</small>
              </b-switch>
            </toggle-box>
            <toggle-box v-if="locationFilter" :title="$t('location')" outlined :title-size="6" class="mt-3">
              <div class="columns is-mobile mb-2">
                <div class="column is-one-third pr-1">
                  <b-tooltip :label="$t('dont-use-geolocation')" position="is-top" type="is-danger" class="w-100">
                    <b-button
                        expanded
                        @click="input_locationType = 'none'"
                        :outlined="input_locationType !== 'none'"
                        :disabled="input_locationType !== 'none' && locationLoading"
                        :loading="input_locationType === 'none' && locationLoading"
                        type="is-danger"
                    >
                      <i class="fas fa-times"></i>
                    </b-button>
                  </b-tooltip>
                </div>
                <div class="column is-one-third pr-1 pl-1">
                  <b-tooltip :label="$t('use-geolocation')" position="is-top" type="is-info" class="w-100">
                    <b-button
                        expanded
                        @click="input_locationType = 'geoLocation'"
                        :outlined="input_locationType !== 'geoLocation'"
                        :disabled="input_locationType !== 'geoLocation' && locationLoading"
                        :loading="input_locationType === 'geoLocation' && locationLoading"
                        type="is-info"
                    >
                      <i class="fas fa-street-view"></i>
                    </b-button>
                  </b-tooltip>
                </div>
                <div class="column is-one-third pl-1">
                  <b-tooltip :label="$t('use-reflocation')" position="is-top" type="is-primary" class="w-100">
                    <b-button
                        expanded
                        @click="input_locationType = 'refLocation'"
                        :outlined="input_locationType !== 'refLocation'"
                        :disabled="input_locationType !== 'refLocation' && locationLoading"
                        :loading="input_locationType === 'refLocation' && locationLoading"
                        type="is-primary"
                    >
                      <i class="fas fa-home"></i>
                    </b-button>
                  </b-tooltip>
                </div>
              </div>
              <b-field :label="$t('or-enter-an-address') + ':'">
                <b-input v-model="input_address" :placeholder="$t('address')" />
              </b-field>
              <b-field>
                <b-switch v-model="input_restrictDistance" :disabled="input_location === null || input_locationType === 'none'" type="is-primary">{{ $t('restrict-distance') }}</b-switch>
              </b-field>
              <b-field :label="$t('radius-from-location') + ':'" v-if="input_restrictDistance && input_location !== null">
                <b-slider v-model="input_distancesRadius" class="pr-5 pl-4" :min="0" :max="100" :step="1" indicator :tooltip="false" />
              </b-field>
            </toggle-box>
            <toggle-box v-if="publicationFilter" :title="$t('publication')" outlined :title-size="6" class="mt-3">
              <b-field>
                <b-switch v-model="input_onlyUnseen" type="is-primary">{{ $t('show-only-unseen') }}</b-switch>
              </b-field>
              <b-field>
                <b-switch v-model="input_useMinCreationdate" type="is-primary">{{ $t('filter-items-creationdate') }}</b-switch>
              </b-field>
              <template v-if="input_useMinCreationdate">
                <div class="columns is-mobile mb-0 mt-3">
                  <div class="column pr-1">
                    <b-slider v-model="input_timeUnitValue" class="pr-5 pl-4" :min="1" :max="sliderTimeUnitMax" :step="1" indicator :tooltip="false" />
                  </div>
                  <div class="column pl-1" style="flex: 0 0 auto;">
                    <b-select v-model="input_timeUnit" :placeholder="$t('unit')">
                        <option value="days">{{ $tc('day', 0) }}</option>
                        <option value="hours">{{ $tc('hour', 0) }}</option>
                        <option value="minutes">{{ $tc('minute', 0) }}</option>
                    </b-select>
                  </div>
                </div>
                <p v-if="input_timeUnit === 'days'">{{ $t('only-items-created-on') }} <b>{{ formattedDay(minCreationdate) }}</b> {{ $t('or-later-will-be-showed') }}.</p>
                <p v-else>{{ $t('only-items-created-at') }} <b>{{ formattedHour(minCreationdate) }}</b> {{ $t('on-day') }} <b>{{ formattedDay(minCreationdate) }}</b> {{ $t('or-later-will-be-showed') }}.</p>
              </template>
            </toggle-box>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import ToggleBox from "@/components/ToggleBox.vue";
import CategorySelector from "@/components/CategorySelector.vue";
import moment from "moment";
import {categories} from "@/categories";
import axios from "axios";
import {GeolocationCoords, isArr, isDictEmpty, isNotEmptyArray, isNotEmptyString, lcall} from "@/functions";
import ErrorHandler from "@/mixins/ErrorHandler";

export default {
  name: "ItemFilters",
  mixins: [ErrorHandler],
  components: {CategorySelector, ToggleBox},
  props: {
    limitedVerticalSpace: {
      type: Boolean,
      required: false,
      default: false
    },
    boxed: {
      type: Boolean,
      required: false,
      default: true
    },
    typesFilter: {
      type: Boolean,
      required: false,
      default: true
    },
    categoriesFilter: {
      type: Boolean,
      required: false,
      default: true
    },
    availabilityFilter: {
      type: Boolean,
      required: false,
      default: true
    },
    locationFilter: {
      type: Boolean,
      required: false,
      default: true
    },
    publicationFilter: {
      type: Boolean,
      required: false,
      default: true
    },
  },
  data() {
    const data = {
      input_search: "",

      mapping: {
        'toUrl': {
          'search': 's',
          'types': 't',
          'categories': 'c',
          'onlyUnseen': 'us',
          'availableFrom': 'avf',
          'includeAfterAvailableFrom': 'iaavf',
          'availableUntil': 'avu',
          'includeBeforeAvailableUntil': 'ibavu',
          'useMinCreationdate': 'umcd',
          'timeUnit': 'tu',
          'timeUnitValue': 'tuv',
          'distancesRadius': 'dr',
          'locationType': 'lt'
        },
        'fromUrl': {
          's': 'search',
          't': 'types',
          'c': 'categories',
          'us': 'onlyUnseen',
          'avf': 'availableFrom',
          'iaavf': 'includeAfterAvailableFrom',
          'avu': 'availableUntil',
          'ibavu': 'includeBeforeAvailableUntil',
          'umcd': 'useMinCreationdate',
          'tu': 'timeUnit',
          'tuv': 'timeUnitValue',
          'dr': 'distancesRadius',
          'lt': 'locationType'
        }
      },

      filtersUsed: {
        'types': true,
        'categories': true,
        'availability': true,
        'location': true,
        'publication': true
      },
      inputsLoaded: false,
      componentWidth: null,
      isMoreFiltersOpened: false,
      selectedCategory: null,
      timeouts: {}
    }

    if (this.typesFilter)
      data['input_types'] = ['DN', 'LN', 'RQ', 'EV'];

    if (this.categoriesFilter)
      data['input_categories'] = [];

    if (this.availabilityFilter) {
      data['input_availableFrom'] = null;
      data['input_includeAfterAvailableFrom'] = true;
      data['input_availableUntil'] = null;
      data['input_includeBeforeAvailableUntil'] = true;
    }

    if (this.locationFilter) {
      data['input_location'] = null;
      data['input_locationType'] = 'none';
      data['locationTypeSetFromOutside'] = false;
      data['input_address'] = "";
      data['input_restrictDistance'] = false;
      data['input_distancesRadius'] = [0, 100];

      data['checkAddress'] = true;
      data['geoLocation'] = null;
      data['refLocation'] = null;
      data['geoLocationAddress'] = "";
      data['refLocationAddress'] = "";
      data['locationLoading'] = false;
    }

    if (this.publicationFilter) {
      data['input_onlyUnseen'] = false;
      data['input_useMinCreationdate'] = false;
      data['input_timeUnit'] = 'hours';
      data['input_timeUnitValue'] = 1;

      data['sliderTimeUnitMemory'] = {
        'days': 1,
        'hours': 1,
        'minutes': 1
      };
      data['sliderTimeUnitMaximums'] = {
        'days': 31,
        'hours': 24,
        'minutes': 60
      };
    }

    return data;
  },
  created() {
    if (this.locationFilter) {
      // Has the user activated geolocation?
      if ('geolocation' in navigator) {
        // Get the position
        navigator.geolocation.getCurrentPosition(
            position => {
              this.geoLocation = new GeolocationCoords(position);
              if (!this.locationTypeSetFromOutside)
                this.input_locationType = 'geoLocation';
            },
            null,
            {
              maximumAge: 10000,
              timeout: 5000,
              enableHighAccuracy: true
            }
        );
      }
    }
  },
  async mounted() {
    const existingParams = ['t', 'c', 'avf', 'iaavf', 'avu', 'ibavu', 'lt', 'dr', 'is', 'tu', 'tuv'];
    let oneParamFound = false;
    for (const i in existingParams) {
      if (existingParams[i] in this.$route.query)
        oneParamFound = true;
    }
    this.saveDataIntoInputs(!oneParamFound ? this.$store.state.itemsFilters : this.$route.query);

    if (this.locationFilter) {
      await this.fetchUser();

      this.geoLocationAddress = await this.fetchAddress(this.geoLocation);
      this.refLocationAddress = await this.fetchAddress(this.refLocation);

      if (this.input_locationType === 'geoLocation') {
        this.checkAddress = false;
        this.input_address = this.geoLocationAddress;
        this.input_location = this.geoLocation;
      } else if (this.input_locationType === 'refLocation') {
        this.checkAddress = false;
        this.input_address = this.refLocationAddress;
        this.input_location = this.refLocation;
      }
    }

    this.inputsLoaded = true;

    const filteredQueryValues = this.filterQueryValues(this.queryValues);
    this.$emit('fieldsUpdated', filteredQueryValues, this.buildURLParams(filteredQueryValues));

    this.$nextTick(() => {
      const filters = document.getElementById("filters");
      if (filters !== null) {
        const resizeObserver = new ResizeObserver((entries) => {
          this.componentWidth = entries[0].contentRect.width;
        });
        resizeObserver.observe(filters);
      }
    });
  },
  computed: {
    userId() {
      return Number(this.$store.state.user.id);
    },
    sliderTimeUnitMax() {
      return this.sliderTimeUnitMaximums[this.input_timeUnit];
    },
    minCreationdate() {
      let minCreationdate = new Date();

      switch (this.input_timeUnit) {
        case 'days':
          minCreationdate.setDate(minCreationdate.getDate() - this.input_timeUnitValue);
          minCreationdate.setHours(0);
          minCreationdate.setMinutes(0);
          break;
        case 'hours':
          minCreationdate.setHours(minCreationdate.getHours() - this.input_timeUnitValue);
          minCreationdate.setMinutes(0);
          break;
        case 'minutes':
          minCreationdate.setMinutes(minCreationdate.getMinutes() - this.input_timeUnitValue);
          break;
      }
      minCreationdate.setSeconds(0);
      minCreationdate.setMilliseconds(0);

      return minCreationdate;
    },
    queryValues() {
      return {
        'search': this.input_search,
        'types': this.input_types,
        'categories': this.input_categories,
        'availableFrom': this.input_availableFrom,
        'includeAfterAvailableFrom': this.input_includeAfterAvailableFrom,
        'availableUntil': this.input_availableUntil,
        'includeBeforeAvailableUntil': this.input_includeBeforeAvailableUntil,
        'location': this.input_location,
        'restrictDistance': this.input_restrictDistance,
        'distancesRadius': this.input_distancesRadius,
        'onlyUnseen': this.input_onlyUnseen,
        'useMinCreationdate': this.input_useMinCreationdate,
        'minCreationdate': this.minCreationdate
      }
    }
  },
  watch: {
    queryValues: {
      handler() {
        if (this.inputsLoaded) {
          const filteredQueryValues = this.filterQueryValues(this.queryValues);
          this.$emit('fieldsUpdated', filteredQueryValues, this.buildURLParams(filteredQueryValues));
        }
      },
      deep: true
    },
    selectedCategory() {
      if (this.input_categories.indexOf(this.selectedCategory) === -1)
        this.input_categories.push(this.selectedCategory);
    },
    input_timeUnit() {
      this.input_timeUnitValue = this.sliderTimeUnitMemory[this.input_timeUnit];
    },
    input_locationType() {
      this.locationLoading = true;
      this.timeouts['input_locationType'] = setTimeout(() => {
        switch (this.input_locationType) {
          case 'geoLocation':
            this.checkAddress = false;
            if (this.geoLocation === null)
              this.snackbarError(this.$t('enable-geolocation-to-use-feature'));
            this.input_address = this.geoLocationAddress;
            this.input_location = this.geoLocation;
            break;
          case 'refLocation':
            this.checkAddress = false;
            this.input_address = this.refLocationAddress;
            this.input_location = this.refLocation;
            break;
          case 'none':
            this.checkAddress = false;
            this.input_address = "";
            this.input_location = null;
            break;
        }
        this.locationLoading = false;
      }, 600);
    },
    input_address() {
      if (this.checkAddress) {
        clearTimeout(this.timeouts['input_address']);
        this.timeouts['input_address'] = setTimeout(() => {
          this.updateGeolocationFromAddress();
        }, 1000);
      } else {
        this.checkAddress = true;
      }
    },
    input_timeUnitValue() {
      this.sliderTimeUnitMemory[this.input_timeUnit] = this.input_timeUnitValue;
    }
  },
  methods: {
    lcall,
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
      const index = this.input_categories.indexOf(category);
      if (index > -1)
        this.input_categories.splice(index, 1);
    },
    async fetchUser() {
      try {
        const params = {
          columns: ['ref_location']
        }
        const refLocation = (await axios.get(`api/v1/webusers/${this.userId}`, {params: params})).data.ref_location;
        if (refLocation !== null) {
          this.refLocation = new GeolocationCoords(refLocation);
          if (this.input_locationType === 'none' && !this.locationTypeSetFromOutside)
            this.input_locationType = 'refLocation';
        }
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
    saveDataIntoInputs(data) {
      if (this.typesFilter) {
        if ('t' in data)
          this.input_types = (isArr(data['t'])) ? data['t'] : [data['t']];
      }

      if (this.categoriesFilter) {
        if ('c' in data)
          this.input_categories = (isArr(data['c'])) ? data['c'] : [data['c']];
      }

      if (this.availabilityFilter) {
        if ('avf' in data)
          this.input_availableFrom = new Date(parseInt(data['avf']) * 1000);
        if ('avu' in data)
          this.input_availableUntil = new Date(parseInt(data['avu']) * 1000);
        this.input_includeAfterAvailableFrom = ('iaavf' in data && data['iaavf'] === 'true');
        this.input_includeBeforeAvailableUntil = ('ibavu' in data && data['ibavu'] === 'true');
      }

      if (this.locationFilter) {
        if ('lt' in data) {
          this.input_locationType = data['lt'];
          this.locationTypeSetFromOutside = true;
        }
        if ('dr' in data) {
          if (isArr(data['dr']) && data['dr'].length === 2) {
            this.input_restrictDistance = true;
            this.input_distancesRadius[0] = parseInt(data['dr'][0]);
            this.input_distancesRadius[1] = parseInt(data['dr'][1]);
          }
        }
      }

      if (this.publicationFilter) {
        this.input_onlyUnseen = ('us' in data && data['us'] === 'true');
        if ('tu' in data && 'tuv' in data) {
          this.input_useMinCreationdate = true;
          this.input_timeUnit = data['tu'];
          this.sliderTimeUnitMemory[this.input_timeUnit] = parseInt(data['tuv']);
          this.input_timeUnitValue = parseInt(data['tuv']);
        } else {
          this.input_useMinCreationdate = false;
        }
        delete data['tu'];
        delete data['tuv'];
      }
    },
    filterQueryValues(queryValues) {
      const newQueryValues = {}

      if (isNotEmptyString(queryValues['search']))
        newQueryValues['search'] = queryValues['search'];

      if (isNotEmptyArray(queryValues['types']))
        newQueryValues['types'] = queryValues['types'];
      if (isNotEmptyArray(queryValues['categories']))
        newQueryValues['categories'] = queryValues['categories'];

      if (queryValues['availableFrom'] instanceof Date) {
        newQueryValues['availableFrom'] = queryValues['availableFrom'];
        if (queryValues['includeAfterAvailableFrom'])
          newQueryValues['includeAfterAvailableFrom'] = true;
      }

      if (queryValues['availableUntil'] instanceof Date) {
        newQueryValues['availableUntil'] = queryValues['availableUntil'];
        if (queryValues['includeBeforeAvailableUntil'])
          newQueryValues['includeBeforeAvailableUntil'] = true;
      }

      if (queryValues['useMinCreationdate'])
        newQueryValues['minCreationdate'] = this.minCreationdate;

      if (queryValues['location'] instanceof GeolocationCoords) {
        newQueryValues['userLocation'] = queryValues['location'];
        if (queryValues['restrictDistance'])
          newQueryValues['distancesRadius'] = queryValues['distancesRadius'];
      }

      if (queryValues['onlyUnseen'])
        newQueryValues['onlyUnseen'] = true;

      return newQueryValues;
    },
    buildURLParams(filteredQueryValues) {
      const params = {};

      if (this.typesFilter) {
        if ('types' in filteredQueryValues)
          params['t'] = filteredQueryValues['types'];
      }

      if (this.categoriesFilter) {
        if ('categories' in filteredQueryValues)
          params['c'] = filteredQueryValues['categories'];
      }

      if (this.availabilityFilter) {
        if ('availableFrom' in filteredQueryValues)
          params['avf'] = filteredQueryValues['availableFrom'].getTime() / 1000
        if ('availableUntil' in filteredQueryValues)
          params['avu'] = filteredQueryValues['availableUntil'].getTime() / 1000
        if ('includeAfterAvailableFrom' in filteredQueryValues)
          params['iaavf'] = (filteredQueryValues['includeAfterAvailableFrom'] === true)
        if ('includeBeforeAvailableUntil' in filteredQueryValues)
          params['ibavu'] = (filteredQueryValues['includeBeforeAvailableUntil'] === true)
      }

      if (this.locationFilter) {
        params['lt'] = this.input_locationType;

        if ('distancesRadius' in filteredQueryValues)
          params['dr'] = filteredQueryValues['distancesRadius'];
      }

      if (this.publicationFilter) {
        if ('onlyUnseen' in filteredQueryValues)
          params['us'] = (filteredQueryValues['onlyUnseen'] === true);

        if ('minCreationdate' in filteredQueryValues) {
          params['tu'] = this.input_timeUnit;
          params['tuv'] = this.input_timeUnitValue;
        }
      }

      return params;
    }
  },
  destroyed: function () {
    for (let i in this.timeouts)
      clearTimeout(this.timeouts[i]);
  }
}
</script>

<style lang="scss" scoped>
#filters-surrounding {
  position: relative;

  &:not(.inputs-loaded) {
    height: 200px;
  }
}

#filters.boxed {
  border-radius: 5px;
  box-shadow: 0 0.5em 1em -0.125em rgba(10, 10, 10, 0.1), 0 0 0 1px rgba(10, 10, 10, 0.02);

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
      flex: 0 0 calc(100% - 40px);
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

@media screen and (max-width: 1023px) {
  #filters {
    min-width: 100%;

    .other-filters:not(.is-opened) {
      display: none;
    }
  }
}

@media screen and (max-width: 499px) {
  #filters {
    margin-bottom: 0.25rem;
  }
}
</style>