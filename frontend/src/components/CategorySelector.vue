<template>
  <b-field :message="this.errorCat" type="is-danger">
    <template #label>
      {{ label }}
      <b-tooltip v-if="usesTooltip" :label="$t('help_item_category')" multilined position="is-right">
        <i class="icon far fa-question-circle"></i>
      </b-tooltip>
    </template>
    <b-dropdown
      position="is-bottom-left"
      v-model="selectedCategory"
      aria-role="list"
      scrollable
      :expanded="true"
      @input="$emit('input', $event)">

      <template v-if="number===1" #trigger>
          <b-button v-if="errorCat"
          icon-right="fas fa-exclamation-circle"
          type="is-danger"
          :icon-left="selectedCategory ? categories[selectedCategory].icon : (value ? categories[value].icon : '')"
          >
            {{selectedCategory ? $t(categories[selectedCategory].slug) : (value ? $t(categories[value].slug) : $t('select_category'))}}
          </b-button>
          <b-button v-else
          icon-right="fas fa-angle-down"
          :icon-left="selectedCategory ? categories[selectedCategory].icon : (value ? categories[value].icon : '')"
          >
            {{selectedCategory ? $t(categories[selectedCategory].slug) : (value ? $t(categories[value].slug) : $t('select_category'))}}
          </b-button>
      </template>

      <template v-else #trigger>
        <b-button v-if="!number"
          icon-right="fas fa-angle-down"
          :icon-left="selectedCategory ? categories[selectedCategory].icon : (value ? categories[value].icon : '')"
          class="button-truncate"
          >
            <span class="text-truncate">
            {{selectedCategory ? $t(categories[selectedCategory].slug) : (value ? $t(categories[value].slug) : $t('select_category'))}}
            </span>
            
        </b-button>
        <b-button v-else
          icon-right="fas fa-angle-down"
          :icon-left="selectedCategory ? categories[selectedCategory].icon : (value ? categories[value].icon : '')"
          >
            <span>
              {{selectedCategory ? $t(categories[selectedCategory].slug) : (value ? $t(categories[value].slug) : $t('select_category'))}}
            </span>
            
        </b-button>
      </template>

      <b-dropdown-item v-if="number > 1" value="" style=" height: 30px;"></b-dropdown-item>
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
    usesTooltip: {
      type: Boolean,
      default: false
    },
    errorCat: String,
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

<style lang="scss" scoped>

@media screen and (min-width: 1024px) {

  .button-truncate{
    overflow: hidden;
  }

  .text-truncate{
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;
    display: inline-block;
    width: calc(230px - 24px);
  }
}

@media screen and (max-width: 425px) {

.button-truncate{
  overflow: hidden;
}

.text-truncate{
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
  display: inline-block;
  width: calc(230px - 24px);
}
}

</style>