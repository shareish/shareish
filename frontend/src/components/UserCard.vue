<template>
  <div class="box">
    <div class="media">
      <figure class="media-left">
        <p class="image">
          <router-link :to="{name: 'userDetails', params: {id: user.id}}">
            <b-image v-if="user.images.length > 0" :src="user.images[user.images.length - 1]" ratio="1by1"></b-image>
            <b-image v-else ratio="1by1" src="https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg"></b-image>
          </router-link>
        </p>
      </figure>
      <div class="media-content">
        <h2 class="title is-3">
          <router-link :to="{name: 'userDetails', params: {id: user.id}}">
            {{ user.first_name }} {{ user.last_name }}
          </router-link>
        </h2>
        <h2 class="subtitle is-4">@{{ user.username }}</h2>
        ({{ $t('member_since') }} {{ formattedDate(user.sign_in_date) }})<br /><br />
        {{ user.description }}

        <nav class="level is-mobile">
          <div class="level-left">
            <a v-if="user.homepage_url" :href="user.homepage_url" class="level-item">
              <span class="icon is-small"><i class="fas fa-globe"></i></span>
            </a>
            <a v-if="user.facebook_url" :href="user.facebook_url" class="level-item">
              <span class="icon is-small"><i class="fab fa-facebook"></i></span>
            </a>
            <a v-if="user.instagram_url" :href="user.instagram_url" class="level-item">
              <span class="icon is-small"><i class="fab fa-instagram"></i></span>
            </a>
          </div>
        </nav>
      </div>
      <div v-if="editable && canEdit" class="media-right">
        <div class="buttons">
          <router-link to="/settings">
            <button class="button is-primary">{{ $t('edit') }}</button>
          </router-link>
          <button class="button is-danger" @click="logout()">{{ $t('log-out') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment/moment';
import { logout } from '@/App.vue';

export default {
  name: 'UserCard',
  props: {
    user: Object,
    editable: {type: Boolean, default: false}
  },
  computed: {
    canEdit() {
      return this.user.id === this.$store.state.user.id;
    }
  },
  methods: {
    formattedDate(date) {
      moment.locale(this.$i18n.locale);
      return (moment(date).format('LL'));
    },
    async logout() {
      logout(this)
    }
  }
};
</script>

<style scoped>
.media-left, .media-content {
  margin-bottom: 1rem;
}

.media-content {
  margin-right: 1rem;
}

.media-right {
  margin-left: 0 !important;
}

.media {
  flex-wrap: wrap;
}

.image {
  width: 128px;
}

.title a {
  color: #4a4a4a !important;
}

.media-right button {
  margin-left: 8px;
}
.media-right button:first-child {
  margin-left: 0;
}
</style>
