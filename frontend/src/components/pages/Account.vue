<template>
  <div class="page-account">
    <h1 class="title">{{ $t('my-account') }}</h1>
    <b-loading v-if="loading" :active="loading" :is-full-page="false" />
    <user-card v-else-if="user" :user="user" editable @edit="startEdition" />
    <h1 class="title">{{ $t('my-items') }}</h1>
    <b-loading v-if="loading" :active="loading" :is-full-page="false" />
    <div v-else-if="items && items.length" class="columns">
      <div v-for="item in items" :key="`${item.id}-item-card`" class="column is-one-quarter">
        <item-card :item="item" :user-list="true" :users="itemUsers" />
      </div>
    </div>
    <div v-else>
      {{ $t('no-items') }}
    </div>
  </div>
</template>

<script>
import UserCard from '@/components/UserCard';
import axios from 'axios';
import ItemCard from '@/components/ItemCard';
import EditAccountModal from '@/components/EditAccountModal';

export default {
  name: 'Account',
  components: {UserCard, ItemCard},
  data() {
    return {
      user: null,
      items: [],
      itemUsers: [],

      loading: true
    }
  },
  methods: {
    async fetchUser() {
      try {
        this.user = (await axios.get('/api/v1/users/me/')).data;
      } catch (error) {
        console.log(error);
      }
    },
    async fetchItems() {
      try {
        const uri = `/api/v1/user_items/`;
        this.items = (await axios.get(uri)).data;
      } catch (error) {
        console.log(error);
      }
    },
    async fetchItemUsers() {
      try {
        let uri = `/api/v1/webusers/`;
        this.itemUsers = (await axios.get(uri)).data;
      } catch (error) {
        console.log(error);
      }
    },
    updateUser(user) {
      this.user = user;
    },
    startEdition() {
      this.$buefy.modal.open({
        parent: this,
        props: {user: this.user},
        events: {updateUser: this.updateUser},
        component: EditAccountModal,
        hasModalCard: true,
        trapFocus: true,
      })
    }
  },
  async created() {
    this.loading = true;
    await Promise.all([
      this.fetchUser(),
      this.fetchItems(),
      this.fetchItemUsers()
    ]);
    this.loading = false;
  },
  mounted() {
    document.title = `Shareish | ${this.$t('my-account')}`;
  }
};
</script>

<style scoped>
.columns {
  flex-wrap: wrap;
  align-content: flex-start;
}
</style>
