<template>
  <div id="page-profile">
    <b-loading v-if="loading" :active="true" :is-full-page="false" />
    <template v-else>
      <h1 class="title">@{{ user.username }}</h1>
      <user-card v-if="user" :user="user" />
      <h1 class="title">{{ $t('user-items') }}</h1>
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
import UserCard from "@/components/UserCard";
import axios from "axios";
import ItemCard from "@/components/ItemCard";
import ErrorHandler from "@/components/ErrorHandler";
import WindowSize from "@/components/WindowSize";

export default {
  name: 'TheProfileView',
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
  computed: {
    userId() {
      return Number(this.$route.params.id);
    }
  },
  methods: {
    async fetchUser() {
      try {
        this.user = (await axios.get(`/api/v1/webusers/${this.userId}`)).data;
      }
      catch (error) {
        this.snackbarError(error);
      }
    },
    async fetchItems() {
      try {
        const params = {id: this.userId}
        this.items = (await axios.get("/api/v1/user_items/", {params: params})).data;
      }
      catch (error) {
        this.snackbarError(error);
      }
    },
    windowWidthChanged() {
      // Below or equal 520
      let columnsWidthClass = 'is-full';
      if (this.windowWidth > 550) { // Arbitrary
        columnsWidthClass = 'is-half';
        if (this.windowWidth > 768) { // Over PAL* (768x576)
          columnsWidthClass = 'is-one-third';
          if (this.windowWidth > 1152) { // Over XGA+ (1152x864)
            columnsWidthClass = 'is-one-quarter';
            if (this.windowWidth > 1600) { // Over UXGA (1600x1200)
              columnsWidthClass = 'is-one-fifth';
              if (this.windowWidth > 2560) { // Over WQHD (2560x1440)
                columnsWidthClass = 'is-2';
                if (this.windowWidth > 3840) { // Over UHD-1 (3840x2160)
                  columnsWidthClass = 'is-1';
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

    if (this.$store.state.user.id !== this.userId) {
      await Promise.all([
        this.fetchUser(),
        this.fetchItems()
      ]);
      document.title = `Shareish | ${this.user.username}`;
    } else {
      await this.$router.push("/profile");
    }

    this.loading = false;
  }
};
</script>
