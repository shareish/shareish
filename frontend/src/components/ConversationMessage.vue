<template>
  <article class="media">
    <div class="media-left">
      <figure class="image">
        <b-image v-if="sender.images.length > 0" :src="sender.images[0].url" ratio="1by1" />
        <b-image v-else ratio="1by1" src="https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg"></b-image>
      </figure>
    </div>
    <div class="media-content">
      <div class="content">
        <p class="user">
          <router-link :to="{name: 'userDetails', params: {id: sender.id}}" class="has-text-weight-bold">
            {{ sender.first_name }} {{ sender.last_name }}
          </router-link>
          &middot;
          <small>
            <router-link :to="{name: 'userDetails', params: {id: sender.id}}" class="username">
              @{{ sender.username }}
            </router-link>
          </small>
        </p>
        <p class="message_content" style="white-space: pre-wrap;">{{ message.content }}</p>
        <p class="has-text-grey"><small>{{ formattedDate }}</small></p>
      </div>
    </div>
  </article>
</template>

<script>
import moment from "moment";

export default {
  name: 'ConversationMessage',
  props: {
    message: {
      type: Object,
      required: true
    }
  },
  computed: {
    sender() {
      return this.message.user;
    },
    formattedDate() {
      return moment(this.message.date, "YYYY-MM-DD[T]HH:mm:ss").fromNow();
    }
  }
};
</script>

<style scoped>
.image {
  width: 64px;
}

.media-content .content p {
  margin: 0.25em 0;
  word-break: break-word;
}
</style>
