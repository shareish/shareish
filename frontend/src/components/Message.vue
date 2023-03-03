<template>
  <article class="media">
    <figure class="media-left">
      <p class="image">
        <img v-if="sender.images.length > 0" :src="sender.images[sender.images.length - 1]" />
        <img v-else src="https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg" />
      </p>
    </figure>
    <div class="media-content">
      <div class="content">
        <p class="user">
          <router-link :to="{name: 'userDetails', params: {id: sender.id}}" class="has-text-weight-bold">
            {{ sender.first_name }} {{ sender.last_name }}
          </router-link>
          ·
          <small>
            <router-link :to="{name: 'userDetails', params: {id: sender.id}}" class="username">
              @{{ sender.username }}
            </router-link>
          </small>
        </p>
        <p class="message_content">{{ message.content }}</p>
        <p class="has-text-grey"><small>{{ formattedDate }}</small></p>
      </div>
    </div>
  </article>
</template>

<script>
import moment from 'moment';

export default {
  name: 'Message',
  props: {
    message: Object
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
