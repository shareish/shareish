<template>
  <div class="page-add-item">
    <h1 class="title">{{ $t('my-conversations') }}</h1>
    <b-loading :active="loading" :is-full-page="false" />
    <template v-if="conversations.length">
      <div v-for="conversation in conversations" :key="conversation.id" class="box">
        <div class="level">
          <div class="level-left">
            {{ conversation.slug }}
            <div v-if="conversation.lastUpdate" class="is-size-7 has-text-grey ml-2">{{ $t('last-message') }}
              {{ formattedDate(conversation.lastUpdate) }}
            </div>
            <span v-if="conversation.unread_messages > 0" class="tag is-danger ml-2">
              {{ $tc('unread-messages', conversation.unread_messages, {count: conversation.unread_messages}) }}
            </span>
          </div>
          <div class="level-right">
            <router-link :to="{name: 'conversationDetail', params: {id: conversation.id}}">
              <button class="button is-primary">{{ $t('open-conversation') }}</button>
            </router-link>
          </div>
        </div>
      </div>
    </template>
    <div v-else>
      <em>{{ $t('no-conversation') }}</em>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import moment from 'moment';

const CONVERSATION_LIST_REFRESH_INTERVAL = 15000;

export default {
  name: 'Conversations',
  data() {
    return {
      loading: true,
      conversations: [],
      timeout: null
    }
  },
  methods: {
    async fetchConversations() {
      try {
        const conv = (await axios.get('/api/v1/conversations/')).data;
        this.conversations = conv.map(conversation => {
          let lastUpdate = null;
          if (conversation.last_message) {
            lastUpdate = conversation.last_message.date;
          }
          return {
            ...conversation,
            lastUpdate
          }
        })
      } catch (error) {
        console.log(error);
      }
      clearTimeout(this.timeout);
      this.timeout = setTimeout(this.fetchConversations, CONVERSATION_LIST_REFRESH_INTERVAL);
    },
    formattedDate(date) {
      return moment(date, "YYYY-MM-DD[T]HH:mm:ss").fromNow();
    },
  },
  mounted() {
    this.fetchConversations();
    this.loading = false;
    document.title = `Shareish | ${this.$t('my-conversations')}`;
  },
  destroyed() {
    clearTimeout(this.timeout);
  }
};
</script>
