<template>
  <div id="page-item" class="max-width-is-max-container">
    <b-loading v-if="loading" :active="true" :is-full-page="false" />
    <template v-else>
      <article v-if="itemHasEnded" class="message is-warning">
        <div class="message-header">{{ $t('warning') }}</div>
        <div class="message-body">
          <template v-if="isOwner">
            {{ $t('item-not-available-anymore-warning-owner') }}
          </template>
          <template v-else>
            {{ $t('item-not-available-anymore-warning') }}
          </template>
        </div>
      </article>
      <div class="columns">
        <section class="column is-5">
          <div v-if="!isOwner && itemHasNotEndedYet" id="start-conversation" class="level mb-3">
            <div class="level-left">
              <p class="level-item is-size-5 has-text-weight-bold level-left-description">
                {{ $t("are-you-interested") }}
              </p>
              <button class="level-item button is-primary" @click="startConversation">
                {{ $t('start-conversation') }}
              </button>
            </div>
          </div>
          <b-carousel :autoplay="false" :arrow-hover="false" :arrow="item.images.length > 1" :indicator="item.images.length > 1">
            <template v-if="item.images.length > 0">
              <b-carousel-item v-for="image in item.images" :key="image.position">
                <router-link :to="{name: 'itemDetail', params: {id: item.id}}">
                  <figure id="item-image">
                    <div class="item-image-background">
                      <img :src="image" />
                    </div>
                    <figure>
                      <img :src="image" />
                    </figure>
                  </figure>
                </router-link>
              </b-carousel-item>
            </template>
            <template v-else>
              <b-carousel-item>
                <router-link :to="{name: 'itemDetail', params: {id: item.id}}">
                  <figure id="item-image">
                    <div class="item-image-background">
                      <img :src="itemCategories[0]['image-placeholder']" />
                    </div>
                    <figure>
                      <img :src="itemCategories[0]['image-placeholder']" />
                    </figure>
                  </figure>
                </router-link>
              </b-carousel-item>
            </template>
          </b-carousel>
          <div v-if="isOwner && !itemHasEnded" id="item-management" class="level mt-3">
            <div class="level-left">
              <p class="level-item is-size-5 has-text-weight-bold level-left-description">
                {{ $t('management') }}
              </p>
              <router-link :to="{name: 'editItem', params: {id: item.id}}" class="level-item button is-primary">{{ $t('edit') }}</router-link>
              <button class="level-item button is-danger" @click="deleteItem">{{ $t('delete') }}</button>
            </div>
          </div>
        </section>
        <section id="item-info" class="column is-7">
          <h1 class="title is-size-2">{{ item.name }}
            <item-type-tag :type="item.type" />
          </h1>
          <h5 class="subtitle is-size-6">
            {{ $t("published") }}
            {{ formattedDateFromNow(item.creationdate) }}
            &middot;
            <i class="far fa-eye"></i>{{ item.hitcount }} {{ $t('views') }}
          </h5>
          <article id="categories" class="mb-5-5">
            <p v-for="category in itemCategories" :key="category.slug" class="category">
              <span class="icon"><i :class="category.icon"></i></span>
              <span class="slug">{{ $t(category.slug) }}</span>
            </p>
          </article>
          <article id="description" class="mb-5-5">
            <div class="title is-size-4 mb-1">
              <div class="icon-text">
                <span class="icon is-medium"><i class="fas fa-info-circle"></i></span>
                <span>{{ $t('description') }}</span>
              </div>
            </div>
            <div class="box has-background-white-ter">
              <p class="description wbbw wspw">{{ item.description }}</p>
            </div>
          </article>
          <article id="location" class="mb-5-5">
            <div class="title is-size-4">
              <div class="icon-text">
                <span class="icon is-medium"><i class="fas fa-map-pin"></i></span>
                <span>{{ $t('location') }}</span>
              </div>
            </div>
            <div v-if="address">
              <router-link :to="{name: 'itemsMap', query: {id: item.id}}">
                {{ address }}
              </router-link>
            </div>
            <div v-else>
              <em>{{ $t('no-address') }}</em>
            </div>
          </article>
          <article id="availability" v-if="isOwner || notAvailableYet || item.enddate" class="mb-5-5">
            <div class="title is-size-4">
              <div class="icon-text">
                <span class="icon is-medium"><i class="fas fa-calendar-day"></i></span>
                <span>{{ $t('availability') }}</span>
              </div>
            </div>
            <template v-if="isOwner || itemHasEnded || notAvailableYet">
              <span>
                {{ $t('item-availability-from') }}
                {{ formattedDate(item.startdate) }} ({{ formattedDateFromNow(item.startdate) }})
              </span><br />
            </template>
            <template v-if="item.enddate">
              <span>
                {{ $t('item-availability-until') }}
                {{ formattedDate(item.enddate) }} ({{ formattedDateFromNow(item.enddate) }})
              </span>
            </template>
          </article>
          <article id="user">
            <div class="title is-size-4 mb-1">
              <div class="icon-text">
                <span class="icon is-medium"><i class="fas fa-hand-holding-heart"></i></span>
                <span>{{ $t('shared-by') }}</span>
              </div>
            </div>
            <user-card :user="user" />
          </article>
        </section>
      </div>
    </template>
  </div>
</template>

<script>
import axios from "axios";
import moment from "moment";
import {categories} from "@/categories";
import ItemTypeTag from "@/components/ItemTypeTag";
import UserCard from "@/components/UserCard";
import ErrorHandler from "@/components/ErrorHandler";

export default {
  name: 'TheItemView',
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
      return (this.$route.query.kind === 'recurrent') ? 'recurrents' : 'items';
    },
    isOwner() {
      return this.$store.state.user.id === this.user.id;
    },
    itemCategories() {
      let itemCategories = [];
      if (categories[this.item.category1])
        itemCategories.push(categories[this.item.category1]);
      if (categories[this.item.category2])
        itemCategories.push(categories[this.item.category2]);
      if (categories[this.item.category3])
        itemCategories.push(categories[this.item.category3]);
      return itemCategories;
    },
    notAvailableYet() {
      return this.item.enddate && new Date(this.item.enddate) <= Date.now();
    },
    itemHasNotEndedYet() {
      return !this.item.enddate || new Date(this.item.enddate) > Date.now();
    },
    itemHasEnded() {
      return this.item.enddate && new Date(this.item.enddate) <= Date.now();
    }
  },
  methods: {
    async fetchItem() {
      if (!this.redirection) {
        try {
          const item_id = this.$route.params.id;
          this.item = (await axios.get(`/api/v1/${this.apiURI}/${item_id}/`)).data;
          await axios.get(`/api/v1/items/${item_id}/increase_hitcount`);
        } catch (error) {
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
            this.address = (await axios.post("/api/v1/address/", this.item.location)).data;
          } catch (error) {
            this.snackbarError(error);
          }
        }
      }
    },
    async fetchUser() {
      if (!this.redirection) {
        try {
          this.user = (await axios.get(`/api/v1/webusers/${this.userId}/`)).data;
        } catch (error) {
          this.snackbarError(error);
          this.redirection = true;
          await this.$router.push("/items");
        }
      }
    },
    formattedDate(date) {
      return (moment(date).locale(this.$i18n.locale).format("LLLL"));
    },
    formattedDateFromNow(date) {
      return moment(date).locale(this.$i18n.locale).fromNow();
    },
    async startConversation() {
      try {
        const data = {
          'owner_id': this.item['user_id'],
          'buyer_id': this.$store.state.user.id,
          'item_id': this.item['id']
        }
        const id = (await axios.post("/api/v1/conversations/", data)).data;
        await this.$router.push(`/conversations/${id}`);
      } catch (error) {
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
        await this.$router.push("/items");
      } catch (error) {
        this.snackbarError(this.$t('notif-error-item-delete'));
      }
    },
    async updateItem(item) {
      this.loading = true;
      this.item = item;
      await this.fetchAddress();
      this.loading = false;
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
.max-width-is-max-container {
  margin: 0 auto;
  max-width: 1344px;
}

.mb-5-5 {
  margin-bottom: 2.25rem !important;
}

#item-image {
  position: relative;
  height: 600px;
  padding: 0;
}

#item-image > div.item-image-background {
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  height: 100%;
}

#item-image > div.item-image-background img {
  flex-shrink: 0;
  min-width: 100%;
  min-height: 100%;
  filter: blur(8px);
  -webkit-filter: blur(8px);
  opacity: 0.75;
  max-width: inherit;
}

#item-image > figure img {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  max-width: 100%;
  max-height: 100%;
}

div.icon-text {
  align-items: center;
  justify-content: flex-start;
}

#item-info {
  padding-left: 30px;
}

#item-info .subtitle {
  font-style: italic;
  opacity: 0.9;
}

#item-info .subtitle i {
  margin: 0 0.2em 0 0.1em;
}

#item-info #categories .category {
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
  line-height: 24px;
  padding: 5px 0;
}

#item-info #categories .category .icon {
  float: left;
  height: 24px;
  width: 30px;
  margin-right: 5px;
}

#item-info #categories .category .icon i {
  font-size: 1.5em;
}

#item-info #categories .category .slug {
  font-size: 16px;
}

@media screen and (max-width: 1215px) and (min-width: 769px) {
  #item-info {
    padding-left: 20px;
  }
}

@media screen and (max-width: 768px) {
  #item-info {
    padding-left: 0.75rem;
  }
}

@media screen and (max-width: 1215px) {
  #page-item-details .columns:first-child .column:first-child .level-left .level-item:first-child {
    display: none;
  }

  .level-left-description {
    display: none;
  }
}
</style>
