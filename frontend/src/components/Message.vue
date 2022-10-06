<template>
  <article class="media">
    <figure class="media-left">
      <p class="image">
        <img v-if="sender.image.length > 0" :src="sender.image[0]" />
        <img v-else src="https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg" />
      </p>
    </figure>
    <div class="media-content">
      <div class="content">
        <p>
          <strong>
            <router-link :to="{ name: 'userDetails', params: { id: sender.id}}">
             {{sender.first_name}} {{sender.last_name}}
            </router-link>
          </strong>
          ·
          <small>
            <router-link :to="{ name: 'userDetails', params: { id: sender.id}}">
              @{{sender.username}}
            </router-link>
          </small>
          <br>
          {{message.content}}
          <br>
          <small class="has-text-grey">{{formattedDate}}</small>
        </p>
      </div>
    </div>
  </article>
</template>

<script>
import moment from 'moment';

export default {
  name: 'Message',
  props: ['message', 'users'],
  computed: {
    sender() {
      return this.users.find(user => user.id === this.message.user) || {};
    },
    formattedDate() {
      return moment(this.message.date, "YYYY-MM-DD[T]HH:mm:ss").fromNow();
    },
  }
};
</script>

<style scoped>
.image {
  width: 64px;
}
</style>