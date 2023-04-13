<template>
  <article class="media" :class="[isFrom]">
    <div v-if="!isFromSelf" class="media-left">
      <router-link :to="{name: 'profile', params: {id: sender.id}}">
        <figure class="image">
          <b-image :src="senderImage" ratio="1by1" />
        </figure>
      </router-link>
    </div>
    <div class="media-content">
      <p class="content wbbw wspw">{{ message.content }}</p>
      <p class="options has-text-grey">
        <template v-if="isFromSelf">
          <span class="delete-message has-text-danger" @click="clickDeleteMessage">Delete</span> &middot;
        </template>
        {{ formattedDate }}
      </p>
    </div>
    <div v-if="isFromSelf" class="media-right">
      <router-link :to="{name: 'profile', params: {id: sender.id}}">
        <figure class="image">
          <b-image :src="senderImage" ratio="1by1" />
        </figure>
      </router-link>
    </div>
  </article>
</template>

<script>
import moment from "moment";
import axios from "axios";
import ErrorHandler from "@/mixins/ErrorHandler";

export default {
  name: 'ConversationMessage',
  mixins: [ErrorHandler],
  props: {
    message: {
      type: Object,
      required: true
    },
    receiver: {
      type: Number,
      required: false,
      default: null
    }
  },
  computed: {
    sender() {
      return this.message.user;
    },
    isFromSelf() {
      return this.receiver === this.message.user.id;
    },
    isFrom() {
      return (this.isFromSelf) ? 'from-self' : 'from-sender';
    },
    senderImage() {
      if (this.message.user.images.length > 0)
        return this.message.user.images[0].url;
      return "https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg";
    },
    formattedDate() {
      return moment(this.message.date, "YYYY-MM-DD[T]HH:mm:ss").fromNow();
    }
  },
  methods: {
    clickDeleteMessage() {
      this.$buefy.dialog.confirm({
        title: this.$t('delete-message'),
        message: this.$t('delete-message-confirmation'),
        confirmText: this.$t('delete'),
        cancelText: this.$t('cancel'),
        type: 'is-danger',
        hasIcon: true,
        onConfirm: () => this.deleteMessage()
      });
    },
    async deleteMessage() {
      try {
        await axios.delete(`/api/v1/conversations/messages/${this.message.id}`);
        this.$emit('deleted');
      }
      catch (error) {
        this.snackbarError(error);
      }
    }
  }
};
</script>

<style lang="scss" scoped>
$arrowWidth: 6px;
.image {
  width: 64px;
}

.media {
  padding: 8px !important;
  margin: 0 !important;
  border: 0 !important;
  width: 75%;

  .media-content {
    position: relative;

    &:before {
      content:"\A";
      width: $arrowWidth * 2;
      height: $arrowWidth * 2;
      transform: rotate(-45deg);
      position: absolute;
      top: 18px;
    }

    p {
      margin: 0;

      &.content {
        position: relative;
        padding: 12px 14px;
        border-radius: 5px;
        z-index: 1;
      }

      &.options {
        margin-top: 0.25rem;
        font-size: 0.75rem;

        .delete-message {
          cursor: pointer;

          &:hover {
            color: hsl(348, 86%, 43%) !important;
          }
        }
      }
    }
  }

  &.from-sender .media-content {
    margin-left: $arrowWidth;

    &:before {
      left: -$arrowWidth;
      background-color: #e7e7e7;
    }

    p.content {
      background-color: #e7e7e7;
    }
    p.options {
      text-align: left;
    }
  }

  &.from-self {
    margin-left: 25% !important;
  }
  &.from-self .media-content {
    margin-right: $arrowWidth;

    &:before {
      right: -$arrowWidth;
      background-color: #3eae7b;
    }

    p.content {
      background-color: #3eae7b;
      color: white;
    }
    p.options {
      text-align: right;
    }
  }
}

@media screen and (max-width: 768px) {
  .image {
    width: 48px;
  }

  .media .media-content {
    overflow-x: inherit !important;
  }
}

@media screen and (max-width: 500px) {
  .media {
    width: 90%;

    &.from-self {
      margin-left: 10% !important;
    }

    .media-left, .media-right {
      display: none;
    }
  }
}
</style>
