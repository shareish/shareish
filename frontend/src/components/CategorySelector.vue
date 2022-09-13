<template>
  <b-field :label="label">

    <b-select>
      <option
        v-for="category in categories"
        :value="category.id"
        :key="category.id"
      >
        {{$t(category.slug)}}
      </option>
    </b-select>
  </b-field>

</template>

<script>
import {categories} from '@/categories';
export default {
  name: 'CategorySelector',
  props: ['number'],
  computed: {
    label() {
      let label = this.$t('item-category');
      if (this.number !== null) {
        label += ` ${this.number}`;
      }
      return label;
    },
    categories() {
      return Object.values(categories);
    }
  }
};
</script>

<style scoped>

</style>