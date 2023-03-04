<template>
  <div id="page-conversation-details" class="max-width-is-max-container">
    <h1 class="title">{{ conversation.slug }}</h1>
    <b-loading v-if="loading" :active="loading" :is-full-page="false" />
    <template v-else>
      <div class="columns">
        <div class="column is-two-thirds">
          <article class="media">
            <figure class="media-left">
              <p class="image">
                <img v-if="user.images.length > 0" :src="user.images[user.images.length - 1]" />
                <img v-else src="https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg" />
              </p>
            </figure>
            <div class="media-content">
              <div class="field">
                <p class="control">
                  <textarea v-model="messageToSend" :placeholder="$t('add-message-dot')" class="textarea"></textarea>
                </p>
              </div>
              <div class="field">
                <p class="control">
                  <button :disabled="!messageToSend" class="button" @click="sendMessage">{{ $t('post-message') }}</button>
                </p>
              </div>
            </div>
          </article>
          <message v-for="message in messages" :key="message.id" :message="message" />
        </div>
        <div class="column">
          <item-card :item="item" />
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import ItemCard from '@/components/ItemCard';
import Message from '@/components/Message';
import axios from 'axios';
import ErrorHandler from "@/components/ErrorHandler";

export default {
  name: 'ConversationDetails',
  mixins: [ErrorHandler],
  components: {ItemCard, Message},
  data() {
    return {
      conversation: {},
      item: {},
      messages: [],
      user: {},

      ws: null,
      loading: true,
      messageToSend: ''
    }
  },
  computed: {
    userId() {
      return Number(this.$store.state.user.id);
    },
    conversationId() {
      return Number(this.$route.params.id);
    },
    webSocketHost() {
      let host = axios.defaults.baseURL;
      host = host.replace('http://', 'ws://');
      host = host.replace('https://', 'wss://');
      return host;
    }
  },
  methods: {
    async fetchConversation() {
      try {
        this.conversation = (await axios.get(`/api/v1/conversations/${this.conversationId}/`)).data;
      }
      catch (error) {
        this.snackbarError(error);
      }
    },
    async autofillMessage() {
      if (this.messages.length === 0) {
        let types = {
          "DN": "donation",
          "RQ": "request",
          "LN": "loan"
        }
        this.messageToSend = this.$t('intro-' + types[this.item.item_type] + '-first-message');
      }
    },
    async fetchItem() {
      try {
        this.item = (await axios.get(`/api/v1/items/${this.conversation.item}/`)).data;
      }
      catch (error) {
        this.snackbarError(error);
      }
    },
    async fetchUser() {
      try {
        this.user = (await axios.get(`/api/v1/webusers/${this.userId}`)).data;
      }
      catch (error) {
        this.snackbarError(error);
      }
    },
    async fetchMessages() {
      try {
        this.messages = (await axios.get(`/api/v1/conversations/${this.conversationId}/messages/`)).data;
      }
      catch (error) {
        this.snackbarError(error);
      }
    },
    async createWebSocket() {
      try {
        this.ws = new WebSocket(`${this.webSocketHost}/ws/${this.conversationId}/`);
        this.ws.onopen = () => {
          console.log("Websocket connected.");
        };
        this.ws.addEventListener('message', (event) => {
          const data = JSON.parse(event.data);
          if (data.content) {
            this.messages.unshift(data);
            this.updateNotifications();
          }
          this.ws.addEventListener('close', () => {
            console.log("Websocket has been closed.");
          });
        });
      }
      catch (error) {
        this.snackbarError(error);
      }
    },
    sendMessage() {
      try {
        this.ws.send(JSON.stringify({
          'content': this.messageToSend,
          'conversation_id': this.conversationId,
          'user_id': this.$store.state.user.id,
          'date': new Date()
        }))
        this.messageToSend = '';
      }
      catch (error) {
        this.snackbarError(this.$t('notif-error-send-message'));
      }
    },
    async updateNotifications() {
      if (this.messages.length > 0) {
        try {
          const data = {
            'conversation_id': this.conversationId,
            'last_message_id': this.messages[0]['id']
          }
          this.$store.state.notifications = (await axios.post(`/api/v1/notifications/`, data)).data['unread_messages'];
        }
        catch (error) {
          this.snackbarError(error);
        }
      }
    }
  },
  async mounted() {
    this.loading = true;
    await Promise.all([
      this.fetchConversation(),
      this.fetchUser(),
      this.fetchMessages(),
      this.createWebSocket()
    ]);
    await this.fetchItem();
    this.updateNotifications();
    this.autofillMessage();
    document.title = `Shareish | ${this.conversation.slug}`;

    this.loading = false;
  },
  beforeDestroy() {
    if (this.ws)
      this.ws.close();
  }
};
</script>

<style scoped>
.max-width-is-max-container {
  margin: 0 auto;
  max-width: 1344px;
}

.image {
  width: 64px;
}
</style>
