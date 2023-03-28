<template>
  <article class="media" :class="[isFrom, {'spaced': showSide}]">
    <div v-if="!isFromSelf" class="media-left">
      <router-link v-if="showSide" :to="{name: 'profile', params: {id: sender.id}}">
        <figure class="image">
          <b-image :src="senderImage" ratio="1by1" />
        </figure>
      </router-link>
    </div>
    <div class="media-content">
      <p class="content wbbw wspw" :class="{'show-arrow': showSide}">{{ message.content }}</p>
      <p v-if="showSide" class="date has-text-grey">{{ formattedDateFromNow(message.date, $i18n.locale) }}</p>
    </div>
    <div v-if="isFromSelf" class="media-right">
      <router-link v-if="showSide" :to="{name: 'profile', params: {id: sender.id}}">
        <figure class="image">
          <b-image :src="senderImage" ratio="1by1" />
        </figure>
      </router-link>
    </div>
    <div v-if="isFromSelf" class="delete-message vh-align-center">
      <i class="fas fa-trash" @click="clickDeleteMessage"></i>
    </div>
  </article>
</template>

<script>
import axios from "axios";
import ErrorHandler from "@/mixins/ErrorHandler";
import {formattedDateFromNow} from "@/functions";

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
    },
    showSide: {
      type: Boolean,
      required: false,
      default: true
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
      } catch (error) {
        this.snackbarError(error);
      }
    },
    formattedDateFromNow
  }
};
</script>

<style lang="scss" scoped>
$arrowWidth: 6px;
$imageWidth: 48px;
$mediaWidth: 75%;

.image {
  width: $imageWidth;
}

.media {
  position: relative;
  padding: 2px !important;
  margin: 0 !important;
  border: 0 !important;
  width: 100%;

  &.spaced {
    margin-bottom: 0.75rem !important;
  }

  .media-left, .media-right {
    position: relative;
    width: $imageWidth;
    height: 100%;

    a {
      position: absolute;
      bottom: 22px;
    }
  }

  .media-content p {
    margin: 0;

    &.content {
      position: relative;
      padding: 12px 14px;
      border-radius: 5px;
      z-index: 1;
    }

    &.date {
      margin-top: 0.25rem;
      font-size: 0.75rem;
    }
  }

  .delete-message {
    position: absolute;
    top: 10px;
    display: none;
    background-color: #ffcdcd;
    border-radius: 100%;
    width: 32px;
    height: 32px;
    cursor: pointer;

    i {
      color: #ff4c4c;
    }

    &:hover i {
      color: hsl(348, 86%, 43%) !important;
    }
  }

  &.from-sender {
    padding-right: 100% - $mediaWidth !important;

    .media-left {
      margin-left: 5px;
    }

    .media-content {
      p.content {
        background-color: #e7e7e7;

        &.show-arrow {
          position: relative;

          &:before {
            position: absolute;
            top: 18px;
            left: -$arrowWidth;
            width: $arrowWidth * 2;
            height: $arrowWidth * 2;
            transform: rotate(-45deg);
            background-color: #e7e7e7;
            content: "\A";
          }
        }
      }

      p.date {
        text-align: left;
      }
    }
  }

  &.from-self {
    padding-left: 100% - $mediaWidth !important;

    .media-content {
      p.content {
        background-color: #3eae7b;
        color: white;

        &.show-arrow {
          position: relative;

          &:before {
            position: absolute;
            bottom: 18px;
            right: -$arrowWidth;
            width: $arrowWidth * 2;
            height: $arrowWidth * 2;
            transform: rotate(-45deg);
            background-color: #3eae7b;
            content: "\A";
          }
        }
      }

      p.date {
        text-align: right;
      }
    }

    .media-right {
      margin-right: 5px;
    }

    .delete-message {
      right: calc(#{$mediaWidth} + 10px);
    }
  }

  &:hover {
    .delete-message {
      display: block;
    }
  }
}

@media screen and (max-width: 768px) {
  .media .media-content {
    overflow-x: inherit !important;
  }
}
</style>
