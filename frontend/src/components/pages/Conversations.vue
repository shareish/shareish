<template>
  <div class="page-add-item">
    <h1 class="title">{{$t('my-conversations')}}</h1>
    <b-loading :active="loading" :is-full-page="false" />
    <template v-if="conversations.length">
      <div class="box" v-for="conversation in conversations" :key="conversation.slug">
        <div class="level">
          <div class="level-left">
            {{conversation.slug}}
            &nbsp;
            <span class="tag is-danger" v-if="conversation.unread_messages > 0">
              {{$tc('unread-messages', conversation.unread_messages, {count: conversation.unread_messages})}}
            </span>
          </div>
          <div class="level-right">
            <router-link :to="{ name: 'conversationDetail', params: { id: conversation.id }}">
              <button class="button is-primary">{{$t('open-conversation')}}</button>
            </router-link>
          </div>
        </div>
      </div>
    </template>
    <div v-else>
      <em>{{$t('no-conversation')}}</em>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

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
          return {
            ...conversation,
          }
        })
      }
      catch (error) {
        console.log(error);
      }
      clearTimeout(this.timeout);
      this.timeout = setTimeout(this.fetchConversations, CONVERSATION_LIST_REFRESH_INTERVAL);
    },
  },
  mounted() {
    this.fetchConversations();
    this.loading = false;
  },
  destroyed() {
    clearTimeout(this.timeout);
  }
};
</script>

<style scoped>

</style>