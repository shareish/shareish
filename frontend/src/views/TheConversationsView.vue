<template>
  <div id="page-conversations" class="max-width-is-max-container">
    <h1 class="title">{{ $t('my-conversations') }}</h1>
    <b-loading v-if="loading" :active="true" :is-full-page="false" />
    <template v-else-if="conversations.length">
      <div v-for="conversation in conversations" :key="conversation.id" class="box">
        <div class="level">
          <div class="level-left">
            {{ conversation.slug }}
            <div v-if="conversation.lastmessagedate" class="is-size-7 has-text-grey ml-2">{{ $t('last-message') }}
              {{ formattedDateFromNow(conversation.lastmessagedate) }}
            </div>
            <span v-if="conversation.unread_messages > 0" class="tag is-danger ml-2">
              {{ $tc('unread-messages', conversation.unread_messages, {count: conversation.unread_messages}) }}
            </span>
          </div>
          <div class="level-right">
            <router-link :to="{name: 'conversation', params: {id: conversation.id}}">
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
import axios from "axios";
import moment from "moment";
import ErrorHandler from "@/components/ErrorHandler";

const CONVERSATION_LIST_REFRESH_INTERVAL = 15000;

export default {
  name: 'TheConversationsView',
  mixins: [ErrorHandler],
  data() {
    return {
      loading: true,
      conversations: [],
      timeout: null,
      unableToFetchConversations: false
    }
  },
  methods: {
    async fetchConversations() {
      try {
        this.conversations = (await axios.get("/api/v1/conversations/")).data;
        if (this.unableToFetchConversations) {
          this.$buefy.snackbar.open({
            duration: 5000,
            type: 'is-success',
            message: this.$t('conversations-reloaded-successfully'),
            pauseOnHover: true,
            queue: false
          });
          this.unableToFetchConversations = false;
        }
      }
      catch (error) {
        if (!this.unableToFetchConversations) {
          this.unableToFetchConversations = true;
          this.snackbarError(error);
        }
      }
      clearTimeout(this.timeout);
      this.timeout = setTimeout(this.fetchConversations, CONVERSATION_LIST_REFRESH_INTERVAL);
    },
    formattedDateFromNow(date) {
      return moment(date).locale(this.$i18n.locale).fromNow();
    }
  },
  async mounted() {
    await this.fetchConversations();
    document.title = `Shareish | ${this.$t('my-conversations')}`;
    this.loading = false;
  },
  destroyed() {
    clearTimeout(this.timeout);
  }
};
</script>

<style scoped>
.max-width-is-max-container {
  margin: 0 auto;
  max-width: 1344px;
}
</style>