<template>
  <div id="page-conversations" class="max-width-is-max-container" :class="{'window-size-is-mobile': isMobile, 'conversation-opened': isConversationSelected}">
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
            <b-tooltip :position="isMobile ? 'is-left' : 'is-bottom'" label="All">
              <b-button
                  :loading="!canChangeCategory && selectedCategory === 'all'"
                  :disabled="!canChangeCategory && selectedCategory !== 'all'"
                  :outlined="selectedCategory !== 'all'"
                  :active="selectedCategory === 'all'"
                  @click="clickCategory('all')"
                  type="is-primary"
                  class="ml-0"
              >
                <i class="fas fa-list-ul"></i>
              </b-button>
            </b-tooltip>
            <b-tooltip :position="isMobile ? 'is-left' : 'is-bottom'" label="Items you asked">
              <b-button
                  :loading="!canChangeCategory && selectedCategory === 'asked'"
                  :disabled="!canChangeCategory && selectedCategory !== 'asked'"
                  :outlined="selectedCategory !== 'asked'"
                  :active="selectedCategory === 'asked'"
                  @click="clickCategory('asked')"
                  type="is-primary"
              >
                <i class="far fa-hand-paper"></i>
              </b-button>
            </b-tooltip>
            <b-tooltip :position="isMobile ? 'is-left' : 'is-bottom'" label="From your items">
              <b-button
                  :loading="!canChangeCategory && selectedCategory === 'yours'"
                  :disabled="!canChangeCategory && selectedCategory !== 'yours'"
                  :outlined="selectedCategory !== 'yours'"
                  :active="selectedCategory === 'yours'"
                  @click="clickCategory('yours')"
                  type="is-primary"
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
              class="conversation columns is-mobile"
              :class="{'is-active': conversation.id === conversationId}"
          >
            <div class="column">
              <b-image :src="conversation.image" ratio="1by1" class="conversation-image" />
              <div v-if="conversation.unread_messages > 0" class="unread-messages">
                {{ conversation.unread_messages }}
              </div>
            </div>
            <div class="column">
              <p class="conversation-name">
                <template v-if="conversation.item !== null">
                  <strong>{{ conversation.item.name }}</strong>
                </template>
                <template v-else>
                  <small class="has-text-grey is-italic">{{ $t('item-unavailable') }}</small>
                </template>
              </p>
              <p class="conversation-receiver mb-1">
                {{ $t('with') }}
                <span v-if="conversation.receivers.length > 0" class="has-text-primary">
                  @{{ conversation.receivers.map(receiver => receiver.user.username).join(', @')  }}
                </span>
                <span v-else class="has-text-primary">{{ $t('unknown-user') }}</span>
              </p>
              <p class="conversation-last_message mt-1">{{ conversation.last_message }}</p>
            </div>
          </router-link>
        </div>
      </div>
      <div id="conversation" class="column">
        <template v-if="isConversationSelected">
          <div id="conversation-with">
            <div class="level is-mobile">
              <div class="level-left">
                <b-button
                    tag="router-link"
                    :to="{name: 'conversations'}"
                    type="is-primary"
                    outlined
                >
                  <i class="fas fa-chevron-left"></i>
                </b-button>
              </div>
              <div class="level-item">
                <p v-if="activeConversation.receivers.length === 1">
                  <template v-if="windowWidth > 768">Chatting with </template>
                  <strong>
                    <router-link :to="{name: 'profile', params: {id: activeConversation.receivers[0].user.id}}">
                      {{ activeConversation.receivers[0].user.first_name }} {{ activeConversation.receivers[0].user.last_name }}
                    </router-link>
                  </strong>
                </p>
                <p v-else-if="activeConversation.receivers.length === 0">
                  <template v-if="windowWidth > 768">Chatting with </template>
                  <strong>{{ $t('unknown-user') }}</strong>
                </p>
                <p v-else><strong>Group chat</strong></p>
              </div>
              <div class="level-right">
                <!--<b-tooltip position="is-left" :label="activeConversation.is_closed ? (activeConversation.closed_by.id === userId ? 'Unlock conversation' : 'This user locked the conversation') : 'Lock conversation'">//-->
		  <b-tooltip position="is-left" :label="activeConversation.is_closed ? (activeConversation.closed_by.id === userId ? $t('unlock-conversation') : $t('locked-conversation')) : $t('lock-conversation')"> 
		  
                  <b-button
                      type="is-primary"
                      outlined
                      @click="toggleConversationClose()"
                      :disabled="activeConversation.is_closed && activeConversation.closed_by.id !== userId"
                  >
                    <i class="fas" :class="activeConversation.is_closed ? 'fa-lock-open' : 'fa-lock'"></i>
                  </b-button>
                </b-tooltip>
              </div>
            </div>
          </div>
          <div id="item">
            <item-card-horizontal
                v-if="activeConversation.item !== null"
                :item="activeConversation.item"
                :height="itemCardHorizontalHeight" />
            <div v-else class="v-align-center" style="height: 100%;">
              <p class="has-text-centered" style="left: 0; right: 0;">{{ $t('item-linked-to-conv-unavailable-deleted') }}</p>
            </div>
          </div>
          <div id="messages" ref="messages" class="pt-4">
            <div class="messages-header has-text-centered mb-4">
              <template v-if="allMessagesLoaded">
                <p class="has-text-grey has-text-centered" style="height: 40px; line-height: 40px;">{{ $t('start-of-the-conversation') }}</p>
              </template>
              <template v-else>
                <b-button v-if="!allMessagesLoaded" :loading="messagesLoading" @click="loadMessages">
                  {{ $t('button-load-more') }}
                </b-button>
              </template>
            </div>
            <conversation-message
                v-for="(message, index) in messages"
                :key="index"
                :message="message"
                :receiver="userId"
                :show-side="messageShowSide(index)"
                @deleted="deletedEmitted(index)"
            />
          </div>
          <div id="write">
            <div class="columns is-mobile">
              <div class="column">
                <textarea
                    v-model="messageToSend"
                    class="textarea"
                    :placeholder="$t(!activeConversation.is_closed ? 'write-your-message' : 'this-conv-is-closed-textarea')"
                    :rows="textareaRows"
                    :disabled="activeConversation.is_closed"
                    @input="checkRows"
                    @keydown.enter.exact.prevent="sendMessage"
                    @keydown.enter.shift.exact.prevent="shiftEnterPressed"
                />
              </div>
              <div class="column">
                <b-button
                    type="is-primary"
                    @click="sendMessage"
                    :disabled="activeConversation.is_closed"
                    :loading="waitingFormResponse"
                >
                  <i class="fas fa-paper-plane"></i>
                </b-button>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ErrorHandler from "@/mixins/ErrorHandler";
import {categories} from "@/categories";
import {scrollParentToChild, rem, isEmptyArray, isNotEmptyString} from "@/functions";
import ConversationMessage from "@/components/ConversationMessage.vue";
import ItemCardHorizontal from "@/components/ItemCardHorizontal.vue";
import WindowSize from "@/mixins/WindowSize";
import _ from "lodash";

const CONVERSATIONS_REFRESH_INTERVAL = 15000;

export default {
  name: 'TheConversationsView',
  components: {ItemCardHorizontal, ConversationMessage},
  mixins: [ErrorHandler, WindowSize],
  data() {
    return {
      loading: true,
      conversations: [],
      conversationsTextarea: {},
      selected: -1,
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
      itemCardHorizontalHeight: 70,
      isMobile: false,
      allMessagesLoaded: false,
      messagesSection: 1,
      messagesLoading: false
    }
  },
  watch: {
    $route() {
      this.closeConversation();
      this.selected = (this.conversationId) ? this.getIConversation(this.conversationId) : -1;
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
        this.closeConversation();
        this.fetchConversations().then(() => {
          this.selected = this.getIConversation(this.conversationId);
          this.openConversation();
          setTimeout(() => {
            this.canChangeCategory = true;
          }, 500);
        });
      }
    },
    messageToSend() {
      this.conversationsTextarea[this.activeConversation.id] = this.messageToSend;
    }
  },
  computed: {
    conversationId() {
      return (this.$route.params.id) ? Number(this.$route.params.id) : null;
    },
    isConversationSelected() {
      return this.selected >= 0 && this.selected < this.conversations.length;
    },
    activeConversation() {
      return (this.isConversationSelected) ? this.conversations[this.selected] : null;
    },
    userId() {
      return Number(this.$store.state.user.id);
    },
    webSocketHost() {
      let host = axios.defaults.baseURL;
      host = host.replace("http://", "ws://");
      host = host.replace("https://", "wss://");
      return host;
    }
  },
  methods: {
    windowWidthChanged() {
      this.isMobile = (this.windowWidth < 900);
    },
    async openConversation() {
      if (this.isConversationSelected) {
        try {
          if (this.activeConversation.item !== null)
            document.title = `Shareish | ${this.activeConversation.item.name}`;
          else
            document.title = `Shareish | Conversation`;

          await this.loadMessages(false);

          if (this.conversationsTextarea[this.activeConversation.id] === undefined) {
            if (this.messages.length === 0 && this.activeConversation.item !== null)
               this.conversationsTextarea[this.activeConversation.id] = this.$t('intro-' + this.activeConversation.item.type + '-first-message');
            else
              this.conversationsTextarea[this.activeConversation.id] = "";
          }
          this.messageToSend = this.conversationsTextarea[this.activeConversation.id];
          await this.setMessagesAsSeen();

          this.connectToConversation();

          this.$nextTick(function () {
            document.getElementById('messages').addEventListener('scroll', this.scrollHandler);
          });
        }
        catch (error) {
          this.snackbarError(error);
          this.$router.push("/conversations");
        }
      }
    },
    closeConversation() {
      if (this.messages.length > 0) {
        const messages = document.getElementById('messages');
        if (messages)
          messages.removeEventListener('scroll', this.scrollHandler);
        this.messages = [];
      }
      if (this.ws)
        this.ws.close();
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

      const conversationWithHeight = 40 + 2 * rem(0.75) + 1;
      const itemHeight = this.itemCardHorizontalHeight + 2 * rem(0.75) + 1;
      const textareaHeight = ((messageRows * 24) + 24);
      const writeHeight = textareaHeight + (2 * rem(0.75));
      const messagesHeight = 750 - conversationWithHeight - itemHeight - writeHeight
      this.$el.querySelector("#messages").style.height = messagesHeight + "px";

      this.textareaRows = messageRows;
    },
    shiftEnterPressed() {
      this.messageToSend += "\n";
      this.checkRows();
    },
    async fetchConversations() {
      clearTimeout(this.timeouts['conversations']);
      try {
        const filters = {
          search: this.search,
          selectedCategory: this.selectedCategory
        };
        const conversations = (await axios.get("/api/v1/conversations/", {params: filters})).data;

        this.$store.state.notifications = Number((await axios.get("/api/v1/notifications/")).data);

        this.conversations = conversations.map(conversation => {
          let image = "https://placehold.co/96x96";
          if (conversation.item !== null) {
            image = categories[conversation.item.category1]['image-placeholder'];

            if (conversation.item.images.length > 0)
              image = conversation.item.images[0];
          }

          let conversation_users = [...conversation.users];
          for (const [i, conversation_user] of conversation_users.entries()) {
            if (conversation_user.user.id === this.userId) {
              conversation_users.splice(i, 1);
              break;
            }
          }

          return {
            ...conversation,
            image: image,
            receivers: conversation_users
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
      this.timeouts['conversations'] = setTimeout(this.fetchConversations, CONVERSATIONS_REFRESH_INTERVAL);
    },
    async setMessagesAsSeen(force = false) {
      if (this.isConversationSelected && (this.activeConversation.unread_messages > 0 || force) && this.messages.length > 0) {
        try {
          const data = {
            'conversation_id': this.activeConversation.id,
            'last_message_date': this.messages[this.messages.length - 1].date
          }
          const newUnreadMessages = Number((await axios.post("/api/v1/notifications/", data)).data);
          this.$store.state.notifications = newUnreadMessages;

          this.conversations[this.selected].unread_messages = newUnreadMessages;

          // If new message was sent but not yet retrieved/displayed, the this.messages[this.messages.length - 1]
          // could not be the real last message and this.conversation.unread_messages could be greater than 0
          const unreadMessagesBadge = this.$el.querySelector("#conversations .columns:nth-child(" + (this.selected + 1) + ") > .column:first-child .unread-messages");
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
    getIConversation(conversationId) {
      if (!isEmptyArray(this.conversations)) {
        for (let i in this.conversations) {
          if (this.conversations[i].id === conversationId)
            return Number(i);
        }
      }
      return -1;
    },
    scrollLastMessageIntoView(messageIndex = "last", position = "bottom", offset = rem(0.75)) {
      if (this.messages.length > 0) {
        this.$nextTick(() => {
          const parent = this.$el.querySelector("#messages");
          const childSelector = (messageIndex === "last") ? "last-child" : "nth-child(" + (messageIndex + 1) + ")";
          const child = this.$el.querySelector("#messages article:" + childSelector);
          scrollParentToChild(parent, child, position, offset);
        });
      }
    },
    async connectToConversation() {
      if (this.isConversationSelected) {
        try {
          this.ws = new WebSocket(`${this.webSocketHost}/ws/${this.activeConversation.id}/`);
          this.ws.addEventListener('message', (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'new_message') {
              const newMessage = JSON.parse(data['content']);
              this.messages.push(newMessage);
              this.scrollLastMessageIntoView("last", "bottom", rem(0.75));
              this.updateCurrentConversation(newMessage.content);
              this.setMessagesAsSeen(true);
            } else if (data.type === 'message_deleted') {
              const id = Number(data['content']);
              let messageIndex = -1;
              for (let i in this.messages) {
                if (this.messages[i].id === id) {
                  messageIndex = Number(i);
                  break;
                }
              }
              if (messageIndex >= 0) {
                if (this.messages[messageIndex].user_id === this.userId) {
                  this.$buefy.snackbar.open({
                    duration: 5000,
                    type: 'is-success',
                    message: this.$t('message-deleted'),
                    pauseOnHover: true,
                    position: 'is-bottom-right'
                  });
                }
                this.messages.splice(messageIndex, 1);
                if (this.isConversationSelected && messageIndex === this.messages.length)
                  this.conversations[this.selected].last_message = (this.messages.length > 0) ? this.messages[this.messages.length - 1].content : "";
              }
            }
          });
        }
        catch (error) {
          this.snackbarError(error);
        }
      }
    },
    sendMessage() {
      if (this.isConversationSelected && isNotEmptyString(this.messageToSend)) {
        this.waitingFormResponse = true;
        try {
          const data = {
            'type': 'new_message',
            'content': {
              'content': this.messageToSend,
              'conversation_id': this.activeConversation.id,
              'user_id': this.$store.state.user.id
            }
          };
          this.ws.send(JSON.stringify(data));

          this.updateCurrentConversation(this.messageToSend);

          setTimeout(() => {
            this.waitingFormResponse = false;
          }, 500);

          this.conversationsTextarea[this.activeConversation.id] = "";
          this.messageToSend = this.conversationsTextarea[this.activeConversation.id]

          this.checkRows();
        }
        catch (error) {
          this.snackbarError(this.$t('notif-error-send-message'));
        }
      }
    },
    updateCurrentConversation(newMessage) {
      if (this.isConversationSelected) {
        // Move conversation to top
        const conversationToPoke = this.conversations.splice(this.selected, 1)[0];
        this.conversations.unshift(conversationToPoke);
        this.selected = 0;
        this.conversations[this.selected].last_message = newMessage;
      }
    },
    deletedEmitted(index) {
      const data = {
        'type': 'message_deleted',
        'content': {
          'id': this.messages[index].id
        }
      };
      this.ws.send(JSON.stringify(data));
    },
    messageShowSide(index) {
      if (index === this.messages.length - 1) {
        // Message is the last one
        return true;
      } else if (index < this.messages.length - 1) {
        if (this.messages[index].user_id !== this.messages[index + 1].user_id) {
          // Next message is from different user
          return true;
        } else {
          // Next message if from same user
          const messageTimestamp = new Date(this.messages[index].date).getTime();
          const nextMessageTimestamp = new Date(this.messages[index + 1].date).getTime();
          if (nextMessageTimestamp - messageTimestamp >= 10 * 60 * 1000)
            return true;
        }
      }
      return false;
    },
    scrollHandler: _.debounce(async function () {
      const scrollBlock = document.getElementById('messages');
      if (scrollBlock.scrollTop <= 80 && !this.allMessagesLoaded)
        await this.loadMessages();
    }, 100),
    async loadMessages(append = true) {
      this.messagesLoading = true;

      if (!append) {
        this.messagesSection = 1;
        this.allMessagesLoaded = false;
        this.messages = [];
      }

      try {
        const data = (await axios.get(`/api/v1/conversations/${this.activeConversation.id}/messages/`, {params: {page: this.messagesSection}})).data;
        for (let i in data.results)
          this.messages.unshift(data.results[i]);
        this.messagesSection += 1;

        if (data.next === null)
          this.allMessagesLoaded = true;

        if (!append)
          this.scrollLastMessageIntoView("last", "bottom", rem(0.75));
        else
          // length +1 because there is always 1 element at the top of the messages list (loader/start of conv msg)
          this.scrollLastMessageIntoView(data.results.length + 1, "top", 0);
      }
      catch (error) {
        this.snackbarError(error);
      }

      setTimeout(() => {
        this.messagesLoading = false;
      }, 400);
    },
    async toggleConversationClose() {
      this.waitingFormResponse = true;

      if (!this.activeConversation.is_closed) {
        try {
          await axios.get(`/api/v1/conversations/${this.activeConversation.id}/close`);

          this.conversations[this.selected].closed_by = {'id': this.userId};
          this.conversations[this.selected].is_closed = true;

          this.$buefy.snackbar.open({
            duration: 5000,
            type: 'is-success',
            message: this.$t('notif-success-close-conversation'),
            pauseOnHover: true
          });
        }
        catch (error) {
          this.snackbarError(error, {'showErrorCode': false});
        }
      } else {
        if (this.activeConversation.closed_by.id === this.userId) {
          try {
            await axios.get(`/api/v1/conversations/${this.activeConversation.id}/open`);

            this.conversations[this.selected].closed_by.id = null;
            this.conversations[this.selected].is_closed = false;

            this.$buefy.snackbar.open({
              duration: 5000,
              type: 'is-success',
              message: this.$t('notif-success-open-conversation'),
              pauseOnHover: true
            });
          }
          catch (error) {
            this.snackbarError(error, {'showErrorCode': false});
          }
        } else {
          this.snackbarErrorFromKey('CONVERSATION_CLOSED_BY_OTHER_USER_CANNOT_OPEN');
        }
      }

      this.waitingFormResponse = false;
    }
  },
  async mounted() {
    document.title = `Shareish | ${this.$t('my-conversations')}`;
    await this.fetchConversations();
    if (this.conversationId) {
      this.selected = this.getIConversation(this.conversationId);
      await this.openConversation();
    }
    this.loading = false;
  },
  destroyed() {
    for (let i in this.timeouts)
      clearTimeout(this.timeouts[i]);
    this.closeConversation();
  }
};
</script>

<style lang="scss" scoped>
@function rem($size) {
  @return $size * 16px;
}

$boxHeight: 750px;
$conversationsWidth: 424px + 1px;
$conversationImageSize: 100px;
$searchNFiltersHeight: 40px + 2 * rem(0.75) + 1px;
$conversationWithHeight: 40px + 2 * rem(0.75) + 1px;
$itemHeight: 70px + 2 * rem(0.75) + 1px;

.max-width-is-max-container {
  margin: 0 auto;
  max-width: 1344px;
}

#page-conversations > .columns {
  padding: 0;
  height: $boxHeight;
  overflow: hidden;

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
    // $conversationsWidth - input margin right - 3 * icons width - 2 * icons margin left - 2 * outer padding - border width
    width: $conversationsWidth - rem(0.75) - 3 * 40px - 2 * 5px - 2 * rem(0.75) - 1px;
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
  width: $conversationsWidth - 1px;
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
      margin-top: 2px;
      width: calc(100% - 100px);

      p {
        text-overflow: ellipsis;
        white-space: nowrap;
        overflow: hidden;
        color: black;
      }
      p.conversation-name {
        font-size: 1.25rem !important;
      }
      p.conversation-receiver {
        font-size: 0.75rem !important;
        font-style: italic;
      }
      p.conversation-last_message {
        font-size: 0.875rem !important;
      }
    }
  }
}

#conversation {
  #conversation-with {
    height: $conversationWithHeight;
    padding: 0.75rem;
    border-bottom: 1px solid #e9e9e9;

    .level-left, .level-right {
      a {
        width: 40px;
      }
    }

    .level-item {
      line-height: 40px;
      white-space: nowrap;
      overflow: hidden;
    }
  }

  #item {
    height: $itemHeight;
    padding: 0.75rem;
    border-bottom: 1px solid #e9e9e9;
  }

  #messages {
    // $boxHeight - $itemHeight - base textarea height - 2 * outer padding
    height: $boxHeight - $conversationWithHeight - $itemHeight - 48px - (2 * rem(0.75));
    overflow-y: scroll;
    display: flex;
    flex-direction: column;

    *:first-child {
      margin-top: auto !important;
    }
  }

  #write {
    padding: 0.75rem;
    border-top: 1px solid #e9e9e9;

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
}

@media screen and (max-width: 1215px) {
  #conversations {
    .conversation {
      & > .column:first-child {
        flex: 0 0 80px;
      }
      & > .column:last-child {
        margin-top: 0;
        padding-left: 0;

        .title {
          font-size: 0.9em !important;
        }

        .subtitle {
          font-size: 0.8em !important;
        }
      }
    }
  }
}

@media screen and (max-width: 1215px) and (min-width: 901px) {
  #conversations {
    width: 324px;
  }

  #page-conversations > .columns > .column:first-child {
    flex: 0 0 325px;
  }
  #search-n-filters #search-input {
    width: 325px - 1px - 3 * 40px - 2 * 5px - 2 * rem(0.75) - rem(0.75);
  }
}

@media screen and (max-width: 900px) {
  #conversations {
    width: 100%;
  }

  #page-conversations.conversation-opened > .columns > .column:first-child {
    border-right: 0;
  }

  #page-conversations.conversation-opened > .columns > .column {
    &:first-child {
      display: none;
    }
    &:last-child {
      flex: 1 1 auto;
      border-right: 0;
    }
  }
  #page-conversations:not(.conversation-opened) > .columns > .column {
    &:first-child {
      flex: 1 1 auto;
      max-width: 100%;
    }
    &:last-child {
      display: none;
    }
  }

  #search-n-filters .is-clearfix {
    width: calc(100% - 3 * 40px - 2 * 5px - #{rem(0.75)});
  }
  #search-n-filters #search-input {
    width: 100%;
  }
}
</style>
