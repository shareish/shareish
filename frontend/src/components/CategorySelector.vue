<template>
  <b-field>
    <template #label>
      {{ label }}
      <b-tooltip v-if="usesTooltip" :label="$t('help_item_category')" multilined position="is-right">
        <i class="icon far fa-question-circle"></i>
      </b-tooltip>
    </template>
    <b-dropdown
      position="is-top-right"
      v-model="selectedCategory"
      aria-role="list"
      scrollable
      expanded
      :class="{'ml-2': windowWidth > 768}"
      @input="$emit('input', $event)">
      <template #trigger>
          <b-button
          icon-right="fas fa-angle-down"
          :icon-left="selectedCategory ? categories[selectedCategory].icon : (value ? categories[value].icon : '')"
          type="is-white"
          >
            <span>
            {{selectedCategory ? $t(categories[selectedCategory].slug) : (value ? $t(categories[value].slug) : $t('select_category'))}}
            </span>
          </b-button>
      </template>
    <b-dropdown-item v-if="number > 1 || !number" value="" style=" height: 30px;">
    </b-dropdown-item>
      <b-dropdown-item
        v-for="(category, key) in categories"
        :key="key"
        :value="key"
        aria-role="listitem"
      > 
        <div class="media">
          <b-icon class="media-left" :icon="category.icon"></b-icon>
          <div class="media-content">
            {{$t(category.slug)}}
          </div>
        </div>
      </b-dropdown-item>
    </b-dropdown>
  </b-field>
</template>

<script>
import { categories } from "@/categories";

export default {
  name: 'CategorySelector',
  data() {
    return {
      selectedCategory: this.value || null,
    }
  },
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
      return this.$tc('category', 1) + category_number;
    },
    categories() {
      return categories;
    }
  },
};
</script>
