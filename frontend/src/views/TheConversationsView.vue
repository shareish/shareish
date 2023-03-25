<template>
  <div id="page-conversations" class="max-width-is-max-container">
    <b-loading v-if="loading" :active="true" :is-full-page="false" />
    <div class="columns is-mobile box mt-3">
      <div class="column">
        <div id="search-n-filters">
          <b-field grouped>
            <b-input
                v-model="search"
                :placeholder="$t('search')"
                id="search-input"
                :icon-right="search ? 'close-circle' : ''"
                icon-right-clickable
                @icon-right-click="search = ''"
            ></b-input>
            <b-tooltip position="is-bottom" label="All">
              <b-button
                  :loading="!canChangeCategory && selectedCategory === 'all'"
                  :disabled="!canChangeCategory && selectedCategory !== 'all'"
                  :outlined="selectedCategory !== 'all'"
                  :active="selectedCategory === 'all'"
                  @click="clickCategory('all')"
                  class="button is-primary ml-0"
              >
                <i class="fas fa-list-ul"></i>
              </b-button>
            </b-tooltip>
            <b-tooltip position="is-bottom" label="Items you asked">
              <b-button
                  :loading="!canChangeCategory && selectedCategory === 'asked'"
                  :disabled="!canChangeCategory && selectedCategory !== 'asked'"
                  :outlined="selectedCategory !== 'asked'"
                  :active="selectedCategory === 'asked'"
                  @click="clickCategory('asked')"
                  class="button is-primary"
              >
                <i class="far fa-hand-paper"></i>
              </b-button>
            </b-tooltip>
            <b-tooltip position="is-bottom" label="From your items">
              <b-button
                  :loading="!canChangeCategory && selectedCategory === 'yours'"
                  :disabled="!canChangeCategory && selectedCategory !== 'yours'"
                  :outlined="selectedCategory !== 'yours'"
                  :active="selectedCategory === 'yours'"
                  @click="clickCategory('yours')"
                  class="button is-primary"
              >
                <i class="fas fa-user"></i>
              </b-button>
            </b-tooltip>
          </b-field>
        </div>
        <div id="conversations">
          <router-link
              v-for="(conversation, index) in conversations"
              :key="index"
              :to="{name: 'conversation', params: {id: conversation.id}}"
              class="conversation columns"
          >
            <div class="column">
              <b-image :src="conversation.image" ratio="1by1" class="conversation-image" />
              <div v-if="conversation.unread_messages > 0" class="unread-messages">
                {{ conversation.unread_messages }}
              </div>
            </div>
            <div class="column">
              <p class="title mb-1">{{ conversation.item.name }}</p>
              <p class="subtitle mt-1">{{ conversation.last_message }}</p>
            </div>
          </router-link>
        </div>
      </div>
      <div v-if="conversation" id="conversation" class="column">
        <div id="item">
          <item-card-horizontal :item="conversation.item" :height="itemCardHorizontalHeight" />
        </div>
        <div id="messages" ref="messages">
          <conversation-message v-for="(message, index) in messages" :key="index" :message="message" :receiver="userId" />
        </div>
        <div id="write">
          <textarea
              v-model="messageToSend"
              class="textarea mb-2"
              placeholder="Write your message"
              :rows="textareaRows"
              @input="checkRows"
              @keydown.enter.exact.prevent="sendMessage"
              @keydown.enter.shift.exact.prevent="shiftEnterPressed"
          />
          <div class="level">
            <div class="level-left">
              Chatting with
              <b-tooltip label="View user profile" position="is-top">
                <router-link :to="{name: 'profile', params: {id: receiver.id}}" class="ml-1">
                  @{{ receiver.username }}
                </router-link>
              </b-tooltip>
            </div>
            <div class="level-right">
              <b-button class="button is-primary" @click="sendMessage" :disabled="!conversationId" :loading="waitingFormResponse">Send</b-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ErrorHandler from "@/components/ErrorHandler";
import {categories} from "@/categories";
import {scrollParentToChild, rem, isArrEmpty, isDictEmpty} from "@/functions";
import ConversationMessage from "@/components/ConversationMessage.vue";
import ItemCardHorizontal from "@/components/ItemCardHorizontal.vue";

const CONVERSATION_LIST_REFRESH_INTERVAL = 15000;

export default {
  name: 'TheConversationsView',
  components: {ItemCardHorizontal, ConversationMessage},
  mixins: [ErrorHandler],
  data() {
    return {
      loading: true,
      conversations: [],
      conversation: null,
      messages: [],
      messageToSend: "",
      unableToFetchConversations: false,
      textareaRows: 1,
      ws: null,
      waitingFormResponse: false,
      search: "",
      selectedCategory: 'all',
      canChangeCategory: true,
      timeouts: {},
      itemCardHorizontalHeight: 80
    }
  },
  watch: {
    $route() {
      this.openConversation();
    },
    search() {
      clearTimeout(this.timeouts['searchInput']);
      this.timeouts['searchInput'] = setTimeout(() => {
        this.fetchConversations();
      }, 400);
    },
    selectedCategory() {
      if (this.canChangeCategory) {
        this.canChangeCategory = false;
        this.fetchConversations();
        setTimeout(() => {
          this.canChangeCategory = true;
        }, 500);
      }
    }
  },
  computed: {
    conversationId() {
      return (this.$route.params.id) ? Number(this.$route.params.id) : null;
    },
    userId() {
      return Number(this.$store.state.user.id);
    },
    receiver() {
      if (this.conversation)
        return (this.conversation.starter === this.userId) ? this.conversation.item.user : this.conversation.starter;
      return {};
    },
    webSocketHost() {
      let host = axios.defaults.baseURL;
      host = host.replace("http://", "ws://");
      host = host.replace("https://", "wss://");
      return host;
    }
  },
  methods: {
    async openConversation() {
      await this.fetchConversation();
      await this.setMessagesAsSeen();
      this.connectToConversation();
      if (this.messages.length === 0)
        this.messageToSend = this.$t('intro-' + this.conversation.item.type + '-first-message');
    },
    clickCategory(category) {
      if (this.canChangeCategory)
        this.selectedCategory = category;
    },
    checkRows() {
      let messageRows = 1;
      for (let i in this.messageToSend) {
        if (this.messageToSend[i] === '\n')
          messageRows++;
        if (messageRows === 4)
          break;
      }
      const textareaHeight = ((messageRows * 24) + 24);
      const writeHeight = textareaHeight + (2 * rem(0.75));
      const optionsHeight = (40 + rem(0.5))
      const itemHeight = this.itemCardHorizontalHeight + 2 * rem(0.75);
      this.$el.querySelector("#messages").style.height = (750 - itemHeight - writeHeight - optionsHeight) + "px";
      this.textareaRows = messageRows;
    },
    shiftEnterPressed() {
      this.messageToSend += "\n";
      this.checkRows();
    },
    async fetchConversations() {
      try {
        const filters = {
          search: this.search,
          selectedCategory: this.selectedCategory
        };
        const conversations = (await axios.get("/api/v1/conversations/", {params: filters})).data;
        this.$store.state.notifications = Number((await axios.get("/api/v1/notifications/")).data);
        this.conversations = conversations.map(conversation => {
          let image = categories[conversation.item.category1]['image-placeholder'];
          if (conversation.item.images.length > 0)
            image = conversation.item.images[0];
          return {
            ...conversation,
            image: image
          };
        });
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
      clearTimeout(this.timeouts['conversations']);
      this.timeouts['conversations'] = setTimeout(this.fetchConversations, CONVERSATION_LIST_REFRESH_INTERVAL);
    },
    async fetchConversation() {
      if (this.conversationId) {
        try {
          this.conversation = (await axios.get(`/api/v1/conversations/${this.conversationId}/`)).data;
          this.messages = (await axios.get(`/api/v1/conversations/${this.conversationId}/messages/`)).data;
          this.goToLastMessage();
          document.title = `Shareish | ${this.conversation.item.name}`;
        }
        catch (error) {
          this.snackbarError(error);
          this.$router.push("/conversations");
        }
      }
    },
    async setMessagesAsSeen() {
      if (this.conversation && this.conversation.unread_messages > 0 && this.messages.length > 0) {
        try {
          const data = {
            'conversation_id': this.conversation.id,
            'last_message_date': this.messages[this.messages.length - 1].date
          }
          const newUnreadMessages = Number((await axios.post("/api/v1/notifications/", data)).data);
          this.$store.state.notifications = newUnreadMessages;
          this.conversation.unread_messages = newUnreadMessages;

          // If new message was sent but not yet retrieved/displayed, the this.messages[this.messages.length - 1]
          // could not be the real last message and this.conversation.unread_messages could be greater than 0
          const nthChild = this.getIConversation() + 1;
          const unreadMessagesBadge = this.$el.querySelector("#conversations .columns:nth-child(" + nthChild + ") > .column:first-child .unread-messages");
          if (unreadMessagesBadge) {
            if (newUnreadMessages === 0)
              unreadMessagesBadge.remove();
            else
              unreadMessagesBadge.innerHTML = newUnreadMessages;
          }
        }
        catch (error) {
          this.snackbarError(error);
        }
      }
    },
    getIConversation() {
      if (this.conversation && !isArrEmpty(this.conversations)) {
        for (let i in this.conversations) {
          if (this.conversations[i].id === this.conversation.id) {
            return Number(i);
          }
        }
      }
      return -1;
    },
    goToLastMessage() {
      if (this.messages.length > 0) {
        this.$nextTick(function () {
          const parent = this.$el.querySelector("#messages");
          const child = this.$el.querySelector("#messages article:last-child");
          scrollParentToChild(parent, child);
        });
      }
    },
    async connectToConversation() {
      if (this.conversation) {
        try {
          if (this.ws !== null)
            this.ws.close();
          this.ws = new WebSocket(`${this.webSocketHost}/ws/${this.conversation.id}/`);
          this.ws.onopen = () => {
            console.log("Websocket connected.");
          };
          this.ws.addEventListener('message', (event) => {
            const data = JSON.parse(event.data);
            if (data.content) {
              this.messages.push(data);
              this.goToLastMessage();
              this.updateCurrentConversation(data.content);
              this.conversation.unread_messages += 1;
              this.setMessagesAsSeen();
            }
            this.ws.addEventListener('close', () => {
              console.log("Websocket has been closed.");
            });
          });
        }
        catch (error) {
          this.snackbarError(error);
        }
      }
    },
    sendMessage() {
      if (this.conversation && this.messageToSend !== "") {
        this.waitingFormResponse = true;
        try {
          const data = {
            'content': this.messageToSend,
            'conversation_id': this.conversation.id,
            'user_id': this.$store.state.user.id,
            'date': new Date()
          };
          this.ws.send(JSON.stringify(data));

          this.updateCurrentConversation(this.messageToSend);

          setTimeout(() => {
            this.waitingFormResponse = false;
          }, 500);

          this.messageToSend = "";

          this.checkRows();
        }
        catch (error) {
          this.snackbarError(this.$t('notif-error-send-message'));
        }
      }
    },
    updateCurrentConversation(newMessage) {
      const iConversation = this.getIConversation();
      if (iConversation > 0) {
        // Move conversation to top
        const conversationToPoke = this.conversations.splice(iConversation, 1)[0];
        this.conversations.unshift(conversationToPoke);
      }

      // Replace last message showed in conversations list
      this.$nextTick(function () {
        this.$el.querySelector("#conversations > .columns > .column:last-child .subtitle").innerHTML = newMessage;
      });
    }
  },
  async mounted() {
    document.title = `Shareish | ${this.$t('my-conversations')}`;
    await this.fetchConversations();
    if (this.conversationId)
      await this.openConversation();
    this.loading = false;
  },
  destroyed() {
    clearTimeout(this.timeout);
  }
};
</script>

<style lang="scss">
@function rem($size) {
  @return $size * 16px;
}

$boxHeight: 750px;
$conversationsWidth: 400px;
$conversationImageSize: 100px;
$searchNFiltersHeight: 40px + 2 * rem(0.75) + 1px;
$itemHeight: 80px + 2 * rem(0.75);

.max-width-is-max-container {
  margin: 0 auto;
  max-width: 1344px;
}

#page-conversations > .columns {
  padding: 0;
  height: $boxHeight;
  overflow: hidden;
  min-width: 1200px;

  & > .column {
    padding: 0;
  }
}

#page-conversations > .columns > .column:first-child {
  flex: 0 0 $conversationsWidth;
  border-right: 1px solid #e9e9e9;
}

#search-n-filters {
  height: $searchNFiltersHeight;
  padding: 0.75rem;
  border-bottom: 1px solid #e9e9e9;

  #search-input {
    width: $conversationsWidth - 3 * 40px - 2 * 5px - 2 * rem(0.75) - rem(0.75);
  }

  button {
    width: 40px !important;
    height: 40px !important;
    margin-left: 5px;
    border-radius: 100%;
  }
}

#conversations {
  overflow-y: scroll;
  height: $boxHeight - $searchNFiltersHeight;
  padding: 0.75rem;

  .conversation {
    margin: 0;
    border-radius: 5px;

    &:hover {
      background-color: #f2f2f2;
    }

    &.is-active {
      background-color: #e8e8e8;
    }

    & > .column:first-child {
      flex: 0 0 $conversationImageSize;
      position: relative;

      .conversation-image {
        border-radius: 5px;
        overflow: hidden;
      }

      .unread-messages {
        font-size: 14px;
        position: absolute;
        top: 5px;
        right: 5px;
        height: calc(14px + 6px + 2 * 0.2em);
        min-width: calc(14px + 6px + 2 * 0.2em);
        padding: 0.2em 0.4em;
        background-color: red;
        border-radius: 5px;
        color: white;
        text-align: center;
      }
    }

    & > .column:last-child {
      padding-left: 0.5rem;
      margin-top: 5px;

      .title {
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 1;
        -webkit-box-orient: vertical;
        font-size: 1rem !important;
      }

      .subtitle {
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        font-size: 0.875rem !important;
      }
    }
  }
}

#conversation {
  #item {
    height: $itemHeight;
    padding: 0.75rem;
    border-bottom: 1px solid #e9e9e9;
  }

  #messages {
    height: $boxHeight - $itemHeight - 48px - (40px + rem(0.5)) - (2 * rem(0.75));
    overflow-y: scroll;
    overscroll-behavior: none;
    display: flex;
    flex-direction: column;

    article:first-child {
      margin-top: auto !important;
    }
  }

  #write {
    padding: 0.75rem;
    border-top: 1px solid #e9e9e9;

    textarea {
      resize: none;
    }
  }
}
</style>