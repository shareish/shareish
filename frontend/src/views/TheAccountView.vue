<template>
  <div id="page-account">
    <b-loading v-if="loading" :active="true" :is-full-page="false" />
    <template v-else>
      <h1 class="title is-inline-block mr-3">{{ $t('my-account') }}</h1>
      <user-card v-if="user" :user="user" />
      <h1 class="title">{{ $t('my-items') }}</h1>
      <div v-if="items && items.length" class="columns is-mobile is-flex-wrap-wrap">
        <div v-for="item in items" :key="item.id" class="column" :class="columnsWidthClass">
          <item-card :item="item" />
        </div>
      </div>
      <div v-else>{{ $t('no-items') }}</div>
    </template>
  </div>
</template>

<script>
import UserCard from "@/components/UserCard.vue";
import axios from "axios";
import ItemCard from "@/components/ItemCard.vue";
import ErrorHandler from "@/mixins/ErrorHandler";
import WindowSize from "@/mixins/WindowSize";

export default {
  name: 'TheAccountView',
  mixins: [ErrorHandler, WindowSize],
  components: {UserCard, ItemCard},
  data() {
    return {
      user: {},
      items: [],
      columnsWidthClass: null,

      loading: true
    }
  },
  methods: {
    async fetchUser() {
      try {
        this.user = (await axios.get("/api/v1/users/me/")).data;
      }
      catch (error) {
        this.snackbarError(error);
      }
    },
    async fetchItems() {
      try {
        this.items = (await axios.get("/api/v1/user_items/")).data;
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
  async created() {
    this.loading = true;
    await Promise.all([
      this.fetchUser(),
      this.fetchItems()
    ]);
    this.loading = false;
  },
  mounted() {
    document.title = `Shareish | ${this.$t('my-account')}`;
  }
};
</script>
