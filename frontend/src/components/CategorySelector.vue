<template>
  <b-field :label="label">
    <b-select :expanded="expanded" :value="value" @input="$emit('input', $event)">
      <option v-if="number > 1" value=""></option>
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
    number: {
      type: Number,
      required: true,
      validator: function (value) {
        return value > 0;
      }
    },
    value: String,
    expanded: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    label() {
      return this.$t('category') + " " + this.number;
    },
    categories() {
      return Object.values(categories);
    }
  }
};
</script>
