<template>
  <b-field :label="label">

    <b-select :value="value" @input="$emit('input', $event)">
      <option :value="null">{{$t('all')}}</option>
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
  props: ['number', 'value'],
  computed: {
    label() {
      let label = this.$t('item-category');
      if (this.number) {
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