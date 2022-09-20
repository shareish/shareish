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

</style>