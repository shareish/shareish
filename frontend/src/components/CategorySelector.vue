<template>
  <b-field :label="label">
    <b-select :expanded="expanded" :value="value" @input="$emit('input', $event)">
      <option v-if="number > 1 || !number" value=""></option>
      <option v-for="{id, slug} in categories" :key="id" :value="id">
        {{ $t(slug) }}
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
    expanded: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    label() {
      let addon = (this.number) ? " " + this.number : "";
      return this.$t('category') + addon;
    },
    categories() {
      return Object.values(categories);
    }
  }
};
</script>
