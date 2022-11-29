<template>
<div class="page-account">
  <h1 class="title">{{$t('my-account')}}</h1>
  <b-loading :active="loading" :is-full-page="false" v-if="loading" />
  <user-card  v-else-if="user" :user="user" editable @logout="logout" @edit="startEdition"/>
  <h1 class="title">{{$t('my-items')}}</h1>
  <b-loading :active="loading" :is-full-page="false" v-if="loading" />
  <div class="columns" v-else-if="items && items.length">
    <div class="column is-one-quarter" v-for="item in items" :key="`${item.id}-item-card`">
      <item-card :item="item" :users="itemUsers"/>
    </div>
  </div>
  <div v-else>
    {{$t('no-items')}}
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
        const uri = `/api/v1/users/me/`
        this.user = (await axios.get(uri)).data;
      }
      catch (error) {
        console.log(error);
      }
    },
    async fetchItems() {
      try {
        const uri = `/api/v1/user_items/`;
        this.items = (await axios.get(uri)).data;
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
    async logout() {
      try {
        await axios.post('/api/v1/token/logout/');
        axios.defaults.headers.common["Authorization"] = "";
        localStorage.removeItem("token");
        this.$store.commit('removeToken');
        this.$store.commit('removeUserID');
        await this.$router.push('/');
      }
      catch (error) {
        if (error.response) {
          error = error.response.data;
        }
        else if (error.message) {
          error = error.message;
        }
        console.log(JSON.stringify(error));
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
  /*justify-content: space-between;*/
  align-content: flex-start;
}
</style>