<template>
  <div class="page-conversation-details">
    <h1 class="title">{{ conversation.slug }}</h1>
    <b-loading v-if="loading" :active="loading" :is-full-page="false"/>
    <template v-else>
      <div class="columns">
        <div class="column is-two-thirds">
          <article class="media">
            <figure class="media-left">
              <p class="image">
                <img v-if="currentUser.images.length > 0" :src="currentUser.images[currentUser.images.length - 1]"/>
                <img v-else src="https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg"/>
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
                  <button :disabled="messageToSend===''" class="button" @click="sendMessage">{{
                      $t('post-message')
                    }}
                  </button>
                </p>
              </div>
            </div>
          </article>
          <message v-for="message in messages" :key="message.id" :message="message" :users="users"/>
        </div>
        <div class="column">
          <item-card :item="item" :users="users"/>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import ItemCard from '@/components/ItemCard';
import Message from '@/components/Message';
import axios from 'axios';

export default {
  name: 'ConversationDetails',
  components: {ItemCard, Message},
  data() {
    return {
      conversation: {},
      users: [],
      item: {},
      messages: [],

      ws: null,
      loading: true,
      error: false,
      messageToSend: ''
    }
  },
  computed: {
    currentUserId() {
      return this.$store.state.user.id;
    },
    currentUser() {
      return this.users.find(user => user.id === this.currentUserId) || {};
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
      } catch (error) {
        console.log(error);
        this.error = true;
      }
    },
    async autofillMessage() {
      if (this.messages.length === 0) {
        let types = {
          "DN": "donation",
          "BR": "request",
          "LN": "loan"
        }
        this.messageToSend = this.$t('intro-' + types[this.item.item_type] + '-first-message');
      }
    },
    async fetchItem() {
      try {
        this.item = (await axios.get(`/api/v1/items/${this.conversation.item}/`)).data;
      } catch (error) {
        console.log(error);
        this.error = true;
      }
    },
    async fetchUsers() {
      try {
        this.users = (await axios.get(`/api/v1/webusers/`)).data;
      } catch (error) {
        console.log(error);
        this.error = true;
      }
    },
    async fetchExistingMessages() {
      try {
        this.messages = (await axios.get(`/api/v1/conversations/${this.conversationId}/messages/`)).data;
      } catch (error) {
        console.log(error);
        this.error = true;
      }
    },
    async createWebSocket() {
      try {
        this.ws = new WebSocket(`${this.webSocketHost}/ws/${this.conversationId}/`);
        this.ws.onopen = () => {
          console.log("Websocket connected.")
        };
        this.ws.addEventListener('message', (event) => {
          const data = JSON.parse(event.data);
          if (data.content) {
            this.messages.unshift(data);
            this.updateNotifications();
          }
          this.ws.addEventListener('close', () => {
            console.log("Websocket has been closed.")
          });
        });
      } catch (error) {
        console.log(error);
        this.error = true;
      }
    },
    sendMessage() {
      try {
        this.ws.send(JSON.stringify({
          'content': this.messageToSend,
          'conversation_id': this.conversationId,
          'user_id': this.currentUserId,
          'date': new Date()
        }))
        this.messageToSend = '';
      } catch (error) {
        this.$buefy.snackbar.open({
          duration: 5000,
          type: 'is-danger',
          message: this.$t('notif-error-send-message'),
          pauseOnHover: true,
        })
      }
    },
    async updateNotifications() {
      if (this.messages.length > 0) {
        try {
          const data = {
            'conversation': this.conversationId,
            'last_message': this.messages[0]['id']
          }
          this.$store.state.notifications = (await axios.post(`/api/v1/notifications/`, data)).data['unread_messages'];
        } catch (error) {
          console.log(error);
        }
      }
    }
  },
  async mounted() {
    this.loading = true;
    await Promise.all([
      this.fetchConversation(),
      this.fetchUsers(),
      this.fetchExistingMessages(),
      this.createWebSocket()
    ]);
    await this.fetchItem();
    this.updateNotifications();
    this.autofillMessage();
    this.loading = false;

    document.title = `Shareish | ${this.conversation.slug}`;
  },
  beforeDestroy() {
    if (this.ws) {
      this.ws.close();
    }
  }
};
</script>

<style scoped>
.image {
  width: 64px;
}
</style>
