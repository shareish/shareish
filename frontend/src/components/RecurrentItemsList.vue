<template>
  <div id="items-container" ref="items-container">
    <b-loading v-if="loading" :active="true" :is-full-page="false" />
    <div v-else-if="items && items.length" ref="items-container" class="columns is-mobile is-flex-wrap-wrap">
      <div v-for="item in items" :key="item.id" class="column" :class="columnsWidthClass">
        <item-card :item="item" :recurrent-list="true" />
      </div>
    </div>
    <div v-else>{{ $t('no-items') }}</div>
  </div>
</template>

<script>
import axios from "axios";
import ItemCard from "@/components/ItemCard";
import ErrorHandler from "@/components/ErrorHandler";
import WindowSize from "@/components/WindowSize";

export default {
  name: 'RecurrentItemsList',
  mixins: [ErrorHandler, WindowSize],
  components: {ItemCard},
  data() {
    return {
      windowResizeWatchedRefsProperties: {
        'items-container': {
          'clientWidth': 0
        }
      },
      items: [],
      loading: true,
      columnsWidthClass: null
    }
  },
  methods: {
    async fetchItems() {
      try {
        this.items = (await axios.get("/api/v1/recurrents/")).data;
      }
      catch (error) {
        this.snackbarError(error);
      }
    },
    windowWidthChanged() {
      // Below or equal 520
      const clientWidth = this.windowResizeWatchedRefsProperties['items-container']['clientWidth'];
      let columnsWidthClass = "is-full";
      if (clientWidth > 550) { // Arbitrary
        columnsWidthClass = "is-half";
        if (clientWidth > 768) { // Over PAL* (768x576)
          columnsWidthClass = "is-one-third";
          if (clientWidth > 1152) { // Over XGA+ (1152x864)
            columnsWidthClass = "is-one-quarter";
            if (clientWidth > 1600) { // Over UXGA (1600x1200)
              columnsWidthClass = "is-one-fifth";
              if (clientWidth > 2560) { // Over WQHD (2560x1440)
                columnsWidthClass = "is-2";
                if (clientWidth > 3840) { // Over UHD-1 (3840x2160)
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
