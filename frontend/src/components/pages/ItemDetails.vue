<template>
<div class="page-item-details">
  <b-loading :active="loading" v-if="loading" :is-full-page="false"/>
  <template v-else>
    <h1 class="title">{{item.name}} <item-type-tag :type="item.item_type" /></h1>
    <div class="block level">
      <div class="level-left">
        <div v-for="category in categories" class="icon-text level-item" :key="category.slug">
        <span class="icon is-large">
          <i class="fa-2x" :class="category.icon"></i>
        </span>
          <span class="is-size-5">{{$t(category.slug)}}</span>
        </div>
      </div>
      <div class="level-right">
        <div class="level-item" v-if="!isOwner">
          <button class="button is-primary" @click="startConversation">
            {{$t('start-conversation')}}
          </button>
        </div>
        <div class="level-item buttons" v-else>
          <button class="button is-primary" @click="startEdition">
            {{$t('edit')}}
          </button>
          <button class="button is-danger" @click="deleteItem">
            {{$t('delete')}}
          </button>
        </div>
      </div>
    </div>
    <div class="tile is-ancestor">
      <div class="tile is-vertical">
        <div class="tile is-parent">
          <article class="tile is-child box has-background-white-ter">
            <div class="content is-size-4">
              {{ item.description }}
            </div>
          </article>
        </div>
        <div class="tile">
          <div class="tile is-parent is-vertical">
            <article class="tile is-child box has-background-primary-light">
              <div class="title is-size-4">
                <div class="icon-text">
                  <span class="icon is-medium">
                    <i class="fas fa-calendar-day"></i>
                  </span>
                  <span>{{$t('availability')}}</span>
                </div>
              </div>
              <p class="content is-size-6">
                <span v-if="item.enddate">{{$t('from')}} {{formattedDate(item.startdate)}} ({{formattedDateFromNow(item.startdate)}}) </span>
                <span v-else>{{$t('since')}} {{formattedDate(item.startdate)}} ({{formattedDateFromNow(item.startdate)}}) </span><br>
                <span v-if="item.enddate">{{$t('to')}} {{formattedDate(item.enddate)}} ({{formattedDateFromNow(item.enddate)}}) </span>
              </p>
            </article>
            <article class="tile is-child box has-background-white-ter">
              <div class="title is-size-4">
                <div class="icon-text">
                  <span class="icon is-medium">
                    <i class="fas fa-hand-holding-heart"></i>
                  </span>
                  <span>{{$t('shared-by')}}</span>
                </div>
              </div>
              <user-card :user="user"/>
            </article>
          </div>
          <div class="tile is-parent">
            <article class="tile is-child box is-primary">
              <div class="title is-size-4">
                <div class="icon-text">
                <span class="icon is-medium">
                  <i class="fas fa-map-pin"></i>
                </span>
                  <span>{{$t('location')}}</span>
                </div>
              </div>
              <div class="content" v-if="address">
                <router-link :to="`/map?id=${item.id}`">
                  {{address}}
                </router-link>
              </div>
              <div class="content" v-else>
                <em>{{$t('no-address')}}</em>
              </div>
            </article>
          </div>
        </div>

      </div>
      <div class="tile is-parent is-4" v-if="item.images.length > 0">
        <article class="tile is-child box is-vcentered">
          <figure class="image is-256x256 " v-if="item.images[0]">
            <img :src="item.images[0]" />
          </figure>
        </article>
      </div>
    </div>
  </template>
</div>
</template>

<script>
import axios from 'axios';
import moment from 'moment';
import {categories} from '@/categories';
import ItemTypeTag from '@/components/ItemTypeTag';
import UserCard from '@/components/UserCard';
import EditItemModal from "@/components/EditItemModal";

export default {
  name: 'ItemDetails',
  components: {UserCard, ItemTypeTag},
  data() {
    return {
      item: {},
      users: [],
      address: null,

      loading: true,
      error: false,
    }
  },
  computed: {
    itemId() {
      return this.$route.params.id;
    },
    currentUserId() {
      return this.$store.state.user.id;
    },
    user() {
      return this.users.find(user => user.id === this.item.user) || {};
    },
    isOwner() {
      return this.currentUserId === this.user.id;
    },
    category1() {
      return this.category(this.item.category1);
    },
    category2() {
      return this.category(this.item.category2);
    },
    category3() {
      return this.category(this.item.category3);
    },
    categories() {
      let cat = [];
      if (this.category1) {
        cat.push(this.category1);
      }
      if (this.category2) {
        cat.push(this.category2);
      }
      if (this.category3) {
        cat.push(this.category3);
      }
      return cat;
    },
  },
  methods: {
    async fetchItem() {
      try {
        this.item = (await axios.get(`/api/v1/items/${this.itemId}/`)).data;
      }
      catch (error) {
        console.log(error);
        this.error = true;
      }
    },
    async fetchUsers() {
      try {
        let uri = `/api/v1/webusers/`;
        this.users = (await axios.get(uri)).data;
      }
      catch (error) {
        console.log(error);
        this.error = true;
      }
    },
    async fetchAddress() {
      if (this.item.location === null) {
        return;
      }

      try {
        this.address = (await axios.post(
          `/api/v1/address/`,
          this.item.location
        )).data;
      }
      catch (error) {
        console.log(JSON.stringify(error));
      }
    },
    formattedDate(date) {
      return moment(date, "YYYY-MM-DD[T]HH:mm:ss");
    },
    formattedDateFromNow(date) {
      return this.formattedDate(date).fromNow();
    },
    category(category) {
      return categories[category];
    },
    async startConversation() {
      try {
        const data = {
          'name': "" + this.item['id'] + "-" + this.item['user'] + "-" + this.currentUserId,
          'owner': this.item['user'],
          'buyer': this.currentUserId,
          'item': this.item['id'],
          'messages': [],
        }
        const response = await axios.post('api/v1/conversations/', data);
        await this.$router.push(`/conversations/${response.data['id']}`);
      }
      catch (error) {
        console.log(error);
      }
    },
    async deleteItem() {
      try {
        await axios.delete(`/api/v1/items/${this.item['id']}/`);
        this.$buefy.snackbar.open({
          duration: 5000,
          type: 'is-success',
          message: this.$t('notif-success-item-delete'),
          pauseOnHover: true,
        });
        await this.$router.push('/items');
      }
      catch (error) {
        console.log(error);
        this.$buefy.snackbar.open({
          duration: 5000,
          type: 'is-danger',
          message: this.$t('notif-error-item-delete'),
          pauseOnHover: true,
        })
      }
    },
    async updateItem(item) {
      this.loading = true;
      this.item = item;
      await this.fetchAddress();
      this.loading = false;
    },
    startEdition() {
      this.$buefy.modal.open({
        parent: this,
        props: {item: this.item, address: this.address},
        events: {updateItem: this.updateItem},
        component: EditItemModal,
        hasModalCard: true,
        trapFocus: true,
      })
    }
  },
  async mounted() {
    this.loading = true;
    await Promise.all([
      this.fetchUsers(),
      this.fetchItem()
    ])
    await this.fetchAddress();
    document.title = `Shareish | ${this.item.name}`;
    this.loading = false;
  }
};
</script>

<style scoped>
div.icon-text {
  align-items: center;
  justify-content: flex-start;
}

.is-vcentered {
  display: flex;
  flex-wrap: wrap;
  align-content: center;
  align-items: center;
  justify-content: center;
}

.is-vcentered .image {
  flex-grow: 2;
}
</style>