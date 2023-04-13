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
        <div class="column is-6">
          <section id="carousel" class="mb-5-5">
            <b-carousel :autoplay="false" :arrow-hover="false" :arrow="item.images.length > 1" :indicator="item.images.length > 1">
              <template v-if="item.images.length > 0">
                <b-carousel-item v-for="image in item.images" :key="image.position">
                  <router-link :to="{name: 'item', params: {id: item.id}}">
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
                  <router-link :to="{name: 'item', params: {id: item.id}}">
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
          </section>
          <article id="user">
            <div class="title is-size-4 mb-2">
              <div class="icon-text">
                <span class="icon is-medium"><i class="fas fa-hand-holding-heart"></i></span>
                <span>{{ $t('shared-by') }}</span>
              </div>
            </div>
            <user-card :user="user" />
          </article>
        </div>
        <section id="item-info" class="column is-6">
          <h1 class="title is-size-3 mb-3">{{ item.name }}</h1>
          <h5 class="subtitle mt-3">
            <item-type-tag :type="item.type" />
            &middot;
            {{ $t("published") }}
            {{ formattedDateFromNow(item.creationdate) }}
            &middot;
            <i class="far fa-eye"></i>{{ item.hitcount }} {{ $t('views') }}
          </h5>
          <article id="categories" class="mb-5">
            <p v-for="category in itemCategories" :key="category.slug" class="category">
              <span class="icon"><i :class="category.icon"></i></span>
              <span class="slug">{{ $t(category.slug) }}</span>
            </p>
          </article>
          <template v-if="!isOwner">
            <div class="columns">
              <div class="column is-half">
                <b-button
                    :disabled="itemHasEnded"
                    type="is-primary"
                    style="width: 100%;"
                    @click="startConversation"
                >
                  <i class="far fa-envelope mr-1"></i>
                  {{ $t('start-conversation') }}
                </b-button>
              </div>
              <div class="column is-half">
                <b-button
                    type="is-primary"
                    outlined
                    style="width: 100%;"
                    @click="scrollToComments"
                >
                  <i class="fas fa-comments mr-1"></i>
                  {{ $t('leave-a-comment') }}
                </b-button>
              </div>
            </div>
          </template>
          <template v-else>
            <div v-if="!itemHasEnded" class="columns">
              <div class="column is-half">
                <router-link :to="{name: 'editItem', params: {id: item.id}}" class="button is-primary w-100">{{ $t('edit') }}</router-link>
              </div>
              <div class="column is-half">
                <b-button type="is-danger" class="w-100" @click="clickDeleteItem">{{ $t('delete') }}</b-button>
              </div>
            </div>
          </template>
          <article id="description" class="mb-5-5">
            <div class="title is-size-4 mb-2">
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
            <div class="title is-size-4 mb-2">
              <div class="icon-text">
                <span class="icon is-medium"><i class="fas fa-map-pin"></i></span>
                <span>{{ $t('location') }}</span>
              </div>
            </div>
            <div v-if="address">
              <router-link :to="{name: 'map', query: {id: item.id}}">
                {{ address }}
              </router-link>
            </div>
            <div v-else>
              <em>{{ $t('no-address') }}</em>
            </div>
          </article>
          <article id="availability" v-if="isOwner || notAvailableYet || item.enddate" class="mb-5-5">
            <div class="title is-size-4 mb-2">
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
          <section id="comments">
            <div class="title is-size-4 mb-2">
              <div class="icon-text">
                <span class="icon is-medium"><i class="fas fa-comments"></i></span>
                <span>{{ $tc('comment', 0) }} ({{ comments.length }})</span>
              </div>
            </div>
            <div id="write" class="mb-5">
              <div class="columns is-mobile">
                <div class="column">
                  <textarea
                      v-model="commentToSend"
                      class="textarea"
                      placeholder="Write your message"
                      :rows="textareaRows"
                      @input="checkRows"
                      @keydown.enter.exact.prevent="sendComment"
                      @keydown.enter.shift.exact.prevent="shiftEnterPressed"
                  />
                </div>
                <div class="column">
                  <b-button
                      type="is-primary"
                      @click="sendComment"
                      :loading="waitingFormResponse"
                  >
                    <i class="fas fa-paper-plane"></i>
                  </b-button>
                </div>
              </div>
            </div>
            <div v-if="comments.length > 0" id="comments-list">
              <item-comment
                  v-for="(comment, index) in comments"
                  :key="index"
                  :comment="comment"
                  @deleted="removeComment(index)"
              />
            </div>
            <div v-else class="box has-background-white-ter">
              No comments yet.
            </div>
          </section>
        </section>
      </div>
    </template>
  </div>
</template>

<script>
import axios from "axios";
import moment from "moment";
import {categories} from "@/categories";
import ItemTypeTag from "@/components/ItemTypeTag.vue";
import UserCard from "@/components/UserCard.vue";
import ErrorHandler from "@/mixins/ErrorHandler";
import ItemComment from "@/components/ItemComment.vue";
import {GeolocationCoords, scrollParentToChild} from "@/functions";

export default {
  name: 'TheItemView',
  mixins: [ErrorHandler],
  components: {ItemComment, UserCard, ItemTypeTag},
  data() {
    return {
      item: {},
      user: {},
      address: null,

      comments: [],
      commentToSend: "",
      textareaRows: 1,
      waitingFormResponse: false,

      redirection: false,
      loading: true
    }
  },
  computed: {
    userId() {
      return Number(this.item.user.id);
    },
    itemId() {
      return (this.$route.params.id) ? Number(this.$route.params.id) : null;
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
          const params = {
            'view_date': new Date()
          };
          this.item = (await axios.get(`/api/v1/${this.apiURI}/${this.itemId}/`, {params: params})).data;
        }
        catch (error) {
          this.snackbarError(error);
          this.redirection = true;
          await this.$router.push("/items");
        }
      }
    },
    async fetchAddress(location) {
      if (!this.redirection) {
        if (location instanceof GeolocationCoords) {
          try {
            return (await axios.post("/api/v1/address/reverse", location)).data;
          }
          catch (error) {
            this.snackbarError(error);
          }
        }
      }
      return null;
    },
    async fetchUser() {
      if (!this.redirection) {
        try {
          this.user = (await axios.get(`/api/v1/webusers/${this.userId}/`)).data;
        }
        catch (error) {
          this.snackbarError(error);
        }
      }
    },
    async fetchComments() {
      if (!this.redirection) {
        try {
          this.comments = (await axios.get(`/api/v1/items/${this.itemId}/comments/`)).data;
        }
        catch (error) {
          this.snackbarError(error);
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
          'item_id': this.item.id
        }
        const id = (await axios.post("/api/v1/conversations/", data)).data;
        await this.$router.push(`/conversations/${id}`);
      }
      catch (error) {
        this.snackbarError(error);
      }
    },
    clickDeleteItem() {
      this.$buefy.dialog.confirm({
        title: this.$t('delete-item'),
        message: this.$t('delete-item-confirmation'),
        confirmText: this.$t('delete'),
        cancelText: this.$t('cancel'),
        type: 'is-danger',
        hasIcon: true,
        onConfirm: () => this.deleteItem()
      });
    },
    async deleteItem() {
      try {
        await axios.delete(`/api/v1/items/${this.item.id}/`);
        this.$buefy.snackbar.open({
          duration: 5000,
          type: 'is-success',
          message: this.$t('item-deleted'),
          pauseOnHover: true,
        });
        await this.$router.push("/items");
      }
      catch (error) {
        this.snackbarError(this.$t('notif-error-item-delete'));
      }
    },
    shiftEnterPressed() {
      this.commentToSend += "\n";
      this.checkRows();
    },
    checkRows() {
      let commentRows = 1;
      for (let i in this.commentToSend) {
        if (this.commentToSend[i] === '\n')
          commentRows++;
        if (commentRows === 4)
          break;
      }
      this.textareaRows = commentRows;
    },
    async sendComment() {
      if (this.commentToSend !== "") {
        this.waitingFormResponse = true;
        try {
          const data = {
            'content': this.commentToSend,
            'creationdate': new Date()
          };
          const comment = (await axios.post(`/api/v1/items/${this.itemId}/comments/`, data)).data;
          this.comments.unshift(comment);

          setTimeout(() => {
            this.waitingFormResponse = false;
          }, 500);

          this.commentToSend = "";

          this.checkRows();
        }
        catch (error) {
          this.snackbarError(this.$t('notif-error-post-comment'));
        }
      }
    },
    removeComment(index) {
      this.comments.splice(index, 1);
      this.$buefy.snackbar.open({
        duration: 5000,
        type: 'is-success',
        message: this.$t('comment-deleted'),
        pauseOnHover: true,
        position: 'is-bottom-right'
      });
    },
    scrollToComments() {
      this.$el.querySelector("#comments").scrollIntoView({behavior: "smooth", block: "start"});
    }
  },
  async mounted() {
    this.loading = true;
    await this.fetchItem();
    if (this.item.location !== null) {
      const testtemp = new GeolocationCoords(this.item.location);
      console.log(testtemp);
      this.address = await this.fetchAddress(testtemp);
    }
    await this.fetchUser();
    await this.fetchComments();
    document.title = `Shareish | ${this.item.name}`;
    this.loading = false;
  }
};
</script>

<style lang="scss" scoped>
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
  font-size: 0.875em;
  font-style: italic;
  color: #767676;
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

#write {
  padding: 0;

  .column:last-child {
    flex: 0 0 calc(60px + 0.75rem);
    padding-left: 0;
  }

  textarea {
    resize: none;
  }

  button {
    width: 60px;
    height: 48px;
  }
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
</style>
