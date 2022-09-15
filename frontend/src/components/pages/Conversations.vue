<template>
  <div class="page-add-item">
    <h1 class="title">{{$t('my-conversations')}}</h1>
    <b-loading :active="loading" :is-full-page="false" />
    <template v-if="conversations.length">
      <div class="box" v-for="conversation in conversations" :key="conversation.slug">
        <div class="level">
          <div class="level-left">
            {{conversation.slug}} <span class="tag is-danger" v-if="!conversation.isUpToDate">{{$t('new-messages')}}</span>
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

export default {
  name: 'Conversations',
  data() {
    return {
      loading: false,
      conversations: []
    }
  },
  methods: {
    async fetchConversations() {
      this.loading = true;
      try {
        const conv = (await axios.get('/api/v1/conversations/')).data;
        this.conversations = conv.map(conversation => {
          return {
            ...conversation,
            isUpToDate: this.isConversationUpToDate(conversation)
          }
        })
      }
      catch (error) {
        console.log(error);
      }
      this.loading = false;
    },
    isConversationUpToDate(conversation) {
      if (this.$store.state.user.id === conversation['owner']) {
        return conversation['up2date_owner'] === true;
      }
      else {
        return conversation['up2date_buyer'] === true;
      }
    }
  },
  mounted() {
    this.fetchConversations();
  }
};
</script>

<style scoped>

</style>