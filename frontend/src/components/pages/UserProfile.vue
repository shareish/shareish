<template>
  <div class="page-account">
    <b-loading :active="loading" :is-full-page="false" v-if="loading" />
    <template v-else>
      <h1 class="title">@{{user.username}}</h1>
      <user-card  v-if="user" :user="user"/>
      <h1 class="title">{{$t('user-items')}}</h1>
      <div class="columns" v-if="items && items.length">
        <div class="column is-one-quarter" v-for="item in items" :key="`${item.id}-item-card`">
          <item-card :item="item" :users="itemUsers"/>
        </div>
      </div>
      <div v-else>
        {{$t('no-items')}}
      </div>
    </template>
  </div>
</template>

<script>
import UserCard from '@/components/UserCard';
import axios from 'axios';
import ItemCard from '@/components/ItemCard';
import EditAccountModal from '@/components/EditAccountModal';
export default {
  name: 'UserProfile',
  components: {UserCard, ItemCard},
  data() {
    return {
      user: null,
      items: [],
      itemUsers: [],

      loading: true
    }
  },
  computed: {
    currentUserId() {
      return this.$store.state.user.id;
    },
    currentUser() {
      return this.users.find(user => user.id === this.currentUserId) || {};
    },
    userId() {
      return Number(this.$route.params.id);
    },
  },
  methods: {
    async fetchUser() {
      try {
        const uri = `/api/v1/webusers/${this.userId}/`
        this.user = (await axios.get(uri)).data;
      }
      catch (error) {
        console.log(error);
      }
    },
    async fetchItems() {
      try {
        const uri = `/api/v1/user_items/`;
        this.items = (await axios.get(uri, {params: {id: this.userId}})).data;
      }
      catch (error) {
        console.log(error);
      }
    },
    async fetchItemUsers() {
      try {
        let uri = `/api/v1/webusers/`;
        this.itemUsers = (await axios.get(uri)).data;
      }
      catch (error) {
        console.log(error);
      }
    },
  },
  async created() {
    this.loading = true;

    if (this.currentUserId === this.userId) {
      await this.$router.push('/profile');
      return;
    }

    await Promise.all([
      this.fetchUser(),
      this.fetchItems(),
      this.fetchItemUsers()
    ]);
    document.title = `Shareish | ${this.user.username}`;
    this.loading = false;
  }
};
</script>

<style scoped>
.columns {
  flex-wrap: wrap;
  /*justify-content: space-between;*/
  align-content: flex-start;
}
</style>