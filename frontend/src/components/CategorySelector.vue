<template>
  <b-field :label="label">
    <b-select :value="value" @input="$emit('input', $event)" :expanded="expanded">
      <option :value="null" v-if="nullable">{{$t('all')}}</option>
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
  props: {
    number: Number,
    value: String,
    nullable: {type: Boolean, default: true},
    expanded: {type: Boolean, default: false}
  },
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