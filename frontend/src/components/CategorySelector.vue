<template>
  <b-field :label="label">
    <b-select :expanded="expanded" :value="value" @input="$emit('input', $event)">
      <option v-if="nullable" :value="null">{{ $t('all') }}</option>
      <option v-for="category in categories" :key="category.id" :value="category.id">
        {{ $t(category.slug) }}
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
      if (this.number)
        label += ` ${this.number}`;
      return label;
    },
    categories() {
      return Object.values(categories);
    }
  }
};
</script>
