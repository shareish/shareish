<template>
  <b-field>
    <template #label>{{ label }}
      <b-tooltip v-if="usesTooltip" :label="$t('help_item_category')" multilined position="is-right">
        <i class="icon far fa-question-circle"></i>
      </b-tooltip>
    </template>
    <b-select :expanded="expanded" :value="value" @input="$emit('input', $event)">
      <option v-if="number > 1 || !number" value=""></option>
      <option v-for="{id, slug} in categories" :key="id" :value="id">
        {{ $t(slug) }}
      </option>
    </b-select>
  </b-field>
</template>

<script>
import {categories} from "@/categories";

export default {
  name: 'CategorySelector',
  props: {
    number: Number,
    value: String,
    expanded: {
      type: Boolean,
      default: false
    },
    usesTooltip: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    label() {
      let category_number = (this.number) ? " " + this.number : "";
      return this.$t('category') + category_number;
    },
    categories() {
      return Object.values(categories);
    }
  }
};
</script>
