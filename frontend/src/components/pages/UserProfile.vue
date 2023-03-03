<template>
  <div class="page-account">
    <b-loading v-if="loading" :active="loading" :is-full-page="false" />
    <template v-else>
      <h1 class="title">@{{ user.username }}</h1>
      <user-card v-if="user" :user="user" />
      <h1 class="title">{{ $t('user-items') }}</h1>
      <div v-if="items && items.length" class="columns">
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
  name: 'UserProfile',
  mixins: [ErrorHandler],
  components: {UserCard, ItemCard},
  data() {
    return {
      user: {},
      items: [],

      loading: true
    }
  },
  computed: {
    userId() {
      return Number(this.$route.params.id);
    },
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
        this.items = (await axios.get('/api/v1/user_items/', {params: params})).data;
      }
      catch (error) {
        this.snackbarError(error);
      }
    },
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
      await this.$router.push('/profile');
    }

    this.loading = false;
  }
};
</script>

<style scoped>
.columns {
  flex-wrap: wrap;
  align-content: flex-start;
}
</style>
