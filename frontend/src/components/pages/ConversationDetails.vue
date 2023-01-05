<template>
<div class="page-conversation-details">
  <h1 class="title">{{conversation.slug}}</h1>
  <b-loading :active="loading" :is-full-page="false" v-if="loading"/>
  <template v-else>
    <div class="columns">
      <div class="column is-two-thirds">
        <message
          v-for="message in messages"
          :users="users"
          :message="message"
          :key="message.id"
        />

        <article class="media">
          <figure class="media-left">
            <p class="image">
              <img v-if="currentUser.image.length > 0" :src="currentUser.image[0]" />
              <img v-else src="https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg" />

            </p>
          </figure>
          <div class="media-content">
            <div class="field">
              <p class="control">
                <textarea class="textarea" :placeholder="$t('add-message-dot')" v-model="messageToSend"></textarea>
              </p>
            </div>
            <div class="field">
              <p class="control">
    <button class="button" @click="sendMessage" :disabled="messageToSend===''">{{$t('post-message')}}</button>
              </p>
            </div>
          </div>
        </article>
      </div>
      <div class="column">
        <item-card :users="users" :item="item" />
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
      messageToSend: ''   //this.$t('intro-first-message'),
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
        const id = this.conversationId;
        this.conversation = (await axios.get(`/api/v1/conversations/${id}/`)).data;
      }
      catch (error) {
        console.log(error);
        this.error = true;
      }
    },
    async autofillMessage(){
	  //console.log(this.conversation)
	  console.log(this.messages.length)
	  if (this.messages.length > 0) {
	      this.messageToSend='';
	  }
	  else {
	      if (this.item.item_type === "DN") {
		  this.messageToSend=this.$t('intro-donation-first-message');
	      }
	      else if (this.item.item_type === "BR") {
		  this.messageToSend=this.$t('intro-request-first-message');
	      }
	      else if (this.item.item_type === "LN") {
		  this.messageToSend=this.$t('intro-loan-first-message');
	      }
	  }
      },
    async fetchItem() {
      try {
        const id = this.conversation.item;
        this.item = (await axios.get(`/api/v1/items/${id}/`)).data;
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
    async fetchExistingMessages() {
      try {
        const id = this.conversationId;
        this.messages = (await axios.get(`/api/v1/conversations/${id}/messages/`)).data;
      }
      catch (error) {
        console.log(error);
        this.error = true;
      }
    },
    async createWebSocket() {
      try {
        this.ws = new WebSocket(`${this.webSocketHost}/ws/${this.conversationId}/`);
        this.ws.onopen = () => { console.log("Websocket connected.")};
        this.ws.addEventListener('message', (event) => {
          const data = JSON.parse(event.data);
          if (data.content) {
            this.messages.push(data);
            this.updateNotifications();
          }
          this.ws.addEventListener('close', () => { console.log("Websocket has been closed.")});
        });
      }
      catch (error) {
        console.log(error);
        this.error = true;
      }
    },
    sendMessage() {
      try {
        this.ws.send(
          JSON.stringify({
            'content': this.messageToSend,
            'conversation_id': this.conversationId,
            'user_id': this.currentUserId,
            'date': new Date()
          })
        )
        this.messageToSend = '';
      }
      catch (error) {
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
            'last_message': this.messages.slice(-1)[0]['id']
          }
          this.$store.state.notifications = (await axios.post(`/api/v1/notifications/`, data)).data['unread_messages'];
        }
        catch (error) {
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
    await this.fetchItem(); // need conversation fetched to get id
    this.updateNotifications();
    this.autofillMessage(),
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
