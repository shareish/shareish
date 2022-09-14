<template>
  <b-field grouped>
    <b-field expanded :label="$t('what-are-you-looking-for')">
      <b-input :placeholder="$t('search-dot')"
        :value="searchString"
        @input="debounceSearchString"
        type="search"
        icon-pack="fas"
        icon="search">
      </b-input>
    </b-field>
    <b-field :label="$t('item-type')">
      <b-select v-model="selectedType">
        <option :value="null">{{ $t('all') }}</option>
        <option value="BR">{{ $t('request') }}</option>
        <option value="DN">{{ $t('donation') }}</option>
        <option value="LN">{{ $t('loan') }}</option>
      </b-select>
    </b-field>
    <category-selector v-model="selectedCategory"></category-selector>
  </b-field>
</template>

<script>
import _ from 'lodash';
import CategorySelector from '@/components/CategorySelector';

export default {
  name: 'ItemsFilters',
  components: {CategorySelector},
  data() {
    return {
      selectedCategory: null,
      selectedType: null,
      searchString: '',
    }
  },
  computed: {

  },
  watch: {
    selectedCategory() {
      this.$emit('update:selectedCategory', this.selectedCategory);
    },
    selectedType() {
      this.$emit('update:selectedType', this.selectedType);
    },
    searchString() {
      this.$emit('update:searchString', this.searchString);
    }
  },
  methods: {
    debounceSearchString: _.debounce(async function (value) {
      this.searchString = value;
    }, 500),
  }
};
</script>

<style scoped>

</style>