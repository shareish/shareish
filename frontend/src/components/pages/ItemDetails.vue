<template>
  <div class="page-item-details">
    <b-loading v-if="loading" :active="loading" :is-full-page="false" />
    <template v-else>
      <h1 class="title">{{ item.name }} <item-type-tag :type="item.item_type" /></h1>
      <div class="block level">
        <div class="level-left">
          <div v-for="category in itemCategories" :key="category.slug" class="icon-text level-item">
            <span class="icon is-large"><i :class="category.icon" class="fa-2x"></i></span>
            <span class="is-size-5">{{ $t(category.slug) }}</span>
          </div>
        </div>
        <div class="level-right">
          <div v-if="!isOwner" class="level-item">
            <button class="button is-primary" @click="startConversation">{{ $t('start-conversation') }}</button>
          </div>
          <div v-else class="level-item buttons">
            <button class="button is-primary" @click="startEdition">{{ $t('edit') }}</button>
            <button class="button is-danger" @click="deleteItem">{{ $t('delete') }}</button>
          </div>
        </div>
      </div>
      <div class="tile is-ancestor">
        <div class="tile is-vertical">
          <div class="tile is-parent">
            <article class="tile is-child box has-background-white-ter">
              <div class="content is-size-4">{{ item.description }}</div>
            </article>
          </div>
          <div class="tile">
            <div class="tile is-parent is-vertical">
              <article class="tile is-child box has-background-primary-light">
                <div class="title is-size-4">
                  <div class="icon-text">
                    <span class="icon is-medium"><i class="fas fa-calendar-day"></i></span>
                    <span>{{ $t('availability') }}</span>
                  </div>
                </div>
                <p class="content is-size-6">
                  <span v-if="item.enddate">{{ $t('from') }} {{ formattedDate(item.startdate) }} ({{ formattedDateFromNow(item.startdate) }})</span>
                  <span v-else>{{ $t('since') }} {{ formattedDate(item.startdate) }} ({{ formattedDateFromNow(item.startdate) }})</span><br />
                  <span v-if="item.enddate">{{ $t('to') }} {{ formattedDate(item.enddate) }} ({{ formattedDateFromNow(item.enddate) }})</span>
                </p>
              </article>
              <article class="tile is-child box has-background-white-ter">
                <div class="title is-size-4">
                  <div class="icon-text">
                    <span class="icon is-medium"><i class="fas fa-hand-holding-heart"></i></span>
                    <span>{{ $t('shared-by') }}</span>
                  </div>
                </div>
                <user-card :user="user" />
              </article>
            </div>
            <div class="tile is-parent">
              <article class="tile is-child box is-primary">
                <div class="title is-size-4">
                  <div class="icon-text">
                    <span class="icon is-medium"><i class="fas fa-map-pin"></i></span>
                    <span>{{ $t('location') }}</span>
                  </div>
                </div>
                <div v-if="address" class="content">
                  <router-link :to="{name: 'itemsMap', query: {id: item.id}}">
                    {{ address }}
                  </router-link>
                </div>
                <div v-else class="content">
                  <em>{{ $t('no-address') }}</em>
                </div>
              </article>
            </div>
          </div>
        </div>
        <div v-if="item.images.length > 0" class="tile is-parent is-4">
          <article class="tile is-child box is-vcentered">
            <figure class="image is-256x256">
              <img :src="item.images[item.images.length - 1]" />
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
import ErrorHandler from "@/components/ErrorHandler";

export default {
  name: 'ItemDetails',
  mixins: [ErrorHandler],
  components: {UserCard, ItemTypeTag},
  data() {
    return {
      item: {},
      user: {},
      address: null,

      redirection: false,
      loading: true
    }
  },
  computed: {
    userId() {
      return Number(this.item.user.id);
    },
    apiURI() {
      let kind = this.$route.query.kind;
      return (kind === 'recurrent') ? 'recurrents' : 'items';
    },
    isOwner() {
      return this.$store.state.user.id === this.user.id;
    },
    category1() {
      return categories[this.item.category1];
    },
    category2() {
      return categories[this.item.category2];
    },
    category3() {
      return categories[this.item.category3];
    },
    itemCategories() {
      let itemCategories = [];
      if (this.category1)
        itemCategories.push(this.category1);
      if (this.category2)
        itemCategories.push(this.category2);
      if (this.category3)
        itemCategories.push(this.category3);
      return itemCategories;
    },
  },
  methods: {
    async fetchItem() {
      if (!this.redirection) {
        try {
          const item_id = this.$route.params.id;
          this.item = (await axios.get(`/api/v1/${this.apiURI}/${item_id}/`)).data;
          await axios.get(`/api/v1/items/${item_id}/increase_hitcount`);
        }
        catch (error) {
          this.snackbarError(error);
          this.redirection = true;
          await this.$router.push("/items");
        }
      }
    },
    async fetchAddress() {
      if (!this.redirection) {
        if (this.item.location !== null) {
          try {
            this.address = (await axios.post('/api/v1/address/', this.item.location)).data;
          }
          catch (error) {
            this.snackbarError(error);
          }
        }
      }
    },
    async fetchUser() {
      if (!this.redirection) {
        try {
          this.user = (await axios.get(`/api/v1/webusers/${this.userId}/`)).data;
        }
        catch (error) {
          this.snackbarError(error);
          this.redirection = true;
          await this.$router.push("/items");
        }
      }
    },
    formattedDate(date) {
      moment.locale(this.$i18n.locale);
      return (moment(date).format('LLLL'));
    },
    formattedDateFromNow(date) {
      return moment(date).fromNow();
    },
    async startConversation() {
      try {
        const data = {
          'owner_id': this.item['user'],
          'buyer_id': this.$store.state.user.id,
          'item_id': this.item['id']
        }
        const response = await axios.post('/api/v1/conversations/', data);
        await this.$router.push(`/conversations/${response.data['id']}`);
      }
      catch (error) {
        this.snackbarError(error);
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
        this.snackbarError(this.$t('notif-error-item-delete'));
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
    await this.fetchItem();
    await this.fetchAddress();
    await this.fetchUser();
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
