<template>
<div class="page-account">
  <h1 class="title">{{$t('my-account')}}</h1>
  <user-card  v-if="user" :user="user" editable @logout="logout" @edit="startEdition"/>
  <h1 class="title">{{$t('my-recent-items')}}</h1>
  <div class="columns" v-if="items && items.length">
    <div class="column is-one-quarter" v-for="item in items" :key="`${item.id}-item-card`">
      <item-card :item="item" />
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
export default {
  name: 'Account',
  components: {UserCard},
  data() {
    return {
      user: null,
      items: []
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
    startEdition() {
      //TODO
    }
  },
  async created() {
    await Promise.all([
      this.fetchUser(),
      this.fetchItems()
    ]);
  }
};
</script>

<style scoped>

</style>