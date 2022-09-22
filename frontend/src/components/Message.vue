<template>
  <article class="media">
    <figure class="media-left">
      <p class="image is-64x64">
        <img src="https://bulma.io/images/placeholders/128x128.png">
      </p>
    </figure>
    <div class="media-content">
      <div class="content">
        <p>
          <strong>{{sender.first_name}} {{sender.last_name}}</strong> · <small>@{{sender.username}}</small>
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

</style>