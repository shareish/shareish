<template>
  <div>
    <b-loading v-if="loading" :active="loading" :is-full-page="false" />
    <template v-else>
      <h1 class="title">{{ $t('my-recurrent-items') }}</h1>
      <div v-if="items && items.length" class="columns is-mobile is-flex-wrap-wrap">
        <div v-for="item in items" :key="item.id" class="column" :class="columnsWidthClass">
          <item-card :item="item" :recurrent-list="true" @submitAgain="$emit('submitAgain', $event)" />
        </div>
      </div>
      <div v-else>{{ $t('no-items') }}</div>
    </template>
  </div>
</template>

<script>
import ItemCard from '@/components/ItemCard';
import axios from 'axios';
import ErrorHandler from "@/components/ErrorHandler";
import WindowSize from "@/components/WindowSize";

export default {
  name: 'RecurrentItemsList',
  mixins: [ErrorHandler, WindowSize],
  components: {ItemCard},
  data() {
    return {
      items: [],
      loading: true,
      columnsWidthClass: null,
    }
  },
  methods: {
    async fetchItems() {
      try {
        this.items = (await axios.get('/api/v1/recurrents/')).data;
      }
      catch (error) {
        this.snackbarError(error);
      }
    },
    windowWidthChanged() {
      // Below or equal 520
      let columnsWidthClass = "is-full";
      if (this.windowWidth > 550) { // Arbitrary
        columnsWidthClass = "is-half";
        if (this.windowWidth > 768) { // Over PAL* (768x576)
          columnsWidthClass = "is-one-third";
          if (this.windowWidth > 1152) { // Over XGA+ (1152x864)
            columnsWidthClass = "is-one-quarter";
            if (this.windowWidth > 1600) { // Over UXGA (1600x1200)
              columnsWidthClass = "is-one-fifth";
              if (this.windowWidth > 2560) { // Over WQHD (2560x1440)
                columnsWidthClass = "is-2";
                if (this.windowWidth > 3840) { // Over UHD-1 (3840x2160)
                  columnsWidthClass = "is-1";
                }
              }
            }
          }
        }
      }
      this.columnsWidthClass = columnsWidthClass;
    }
  },
  async mounted() {
    this.loading = true;
    await Promise.all([
      this.fetchItems()
    ]);
    this.loading = false;
  }
};
</script>
