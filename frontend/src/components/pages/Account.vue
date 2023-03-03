<template>
  <div class="page-account">
    <b-loading v-if="loading" :active="loading" :is-full-page="false" />
    <template v-else>
      <h1 class="title">{{ $t('my-account') }}</h1>
      <user-card v-if="user" :user="user" editable />
      <h1 class="title">{{ $t('my-items') }}</h1>
      <div v-if="items && items.length" class="columns is-flex-wrap-wrap">
        <div v-for="item in items" :key="`${item.id}-item-card`" class="column is-one-quarter">
          <item-card :item="item" />
        </div>
      </div>
      <div v-else>{{ $t('no-items') }}</div>
    </template>
  </div>
</template>

<script>
import UserCard from '@/components/UserCard';
import axios from 'axios';
import ItemCard from '@/components/ItemCard';
import ErrorHandler from "@/components/ErrorHandler";

export default {
  name: 'Account',
  mixins: [ErrorHandler],
  components: {UserCard, ItemCard},
  data() {
    return {
      user: {},
      items: [],

      loading: true
    }
  },
  methods: {
    async fetchUser() {
      try {
        this.user = (await axios.get('/api/v1/users/me/')).data;
      }
      catch (error) {
        this.snackbarError(error);
      }
    },
    async fetchItems() {
      try {
        this.items = (await axios.get('/api/v1/user_items/')).data;
      }
      catch (error) {
        this.snackbarError(error);
      }
    },
    updateUser(user) {
      this.user = user;
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
