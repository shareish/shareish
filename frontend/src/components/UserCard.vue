<template>
  <div class="box">
    <div class="media">
      <figure class="media-left">
        <p class="image is-128x128">
          <img src="https://bulma.io/images/placeholders/128x128.png" />
        </p>
      </figure>
      <div class="media-content">
        <h2 class="title is-3">{{ user.first_name }} {{ user.last_name}}</h2>
        <h2 class="subtitle is-4">@{{ user.username }}</h2>
        {{user.description}}

        <nav class="level is-mobile">
          <div class="level-left">
            <a class="level-item" v-if="user.homepage_url" :href="user.homepage_url">
              <span class="icon is-small"><i class="fas fa-globe"></i></span>
            </a>
            <a class="level-item" v-if="user.facebook_url" :href="user.facebook_url">
              <span class="icon is-small"><i class="fab fa-facebook"></i></span>
            </a>
            <a class="level-item" v-if="user.instagram_url" :href="user.instagram_url">
              <span class="icon is-small"><i class="fab fa-instagram"></i></span>
            </a>
          </div>
        </nav>
      </div>
      <div class="media-right" v-if="editable && canEdit">
        <div class="buttons">
          <button class="button is-primary" @click="$emit('edit')">{{$t('edit')}}</button>
          <button class="button is-danger" @click="$emit('logout')">{{$t('log-out')}}</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
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
</style>