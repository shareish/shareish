<template>
  <div class="comment media">
    <div class="media-left">
      <router-link :to="{name: 'profile', params: {id: comment.user.id}}">
        <figure class="image">
          <b-image :src="userImage" ratio="1by1" />
        </figure>
      </router-link>
    </div>
    <div class="media-content">
      <p class="content wbbw wspw has-background-white-ter">{{ comment.content }}</p>
      <p class="options has-text-grey">
        {{ formattedDateFromNow(comment.creationdate) }} &middot;
        <template v-if="isFromSelf">
          <span class="delete-comment has-text-danger" @click="clickDeleteComment">Delete</span>
        </template>
      </p>
    </div>
  </div>
</template>

<script>
import moment from "moment/moment";
import axios from "axios";

export default {
  name: "ItemComment",
  props: {
    comment: {
      type: Object,
      required: true
    }
  },
  computed: {
    userImage() {
      if (this.comment.user.images.length > 0)
        return this.comment.user.images[0].url;
      return "https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg";
    },
    isFromSelf() {
      return this.$store.state.user.id === this.comment.user.id;
    }
  },
  methods: {
    formattedDateFromNow(date) {
      return moment(date).locale(this.$i18n.locale).fromNow();
    },
    clickDeleteComment() {
      this.$buefy.dialog.confirm({
        title: this.$t('delete-comment'),
        comment: this.$t('delete-comment-confirmation'),
        confirmText: this.$t('delete'),
        cancelText: this.$t('cancel'),
        type: 'is-danger',
        hasIcon: true,
        onConfirm: () => this.deleteComment()
      });
    },
    async deleteComment() {
      try {
        await axios.delete(`/api/v1/items/${this.comment.item.id}/comments/${this.comment.id}`);
        this.$emit('deleted');
      } catch (error) {
        this.snackbarError(error);
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.media.comment {
  .media-left {
    width: 64px;
    height: 100%;
    margin-right: 0.75rem;
  }

  .media-content {
    .content {
      padding: 10px 12px;
      border-radius: 5px;
      margin-bottom: 0;
    }

    .options {
      margin: 0.25rem 0 0 0.5rem;
      font-size: 0.75rem;

      .delete-comment {
        cursor: pointer;

        &:hover {
          color: hsl(348, 86%, 43%) !important;
        }
      }
    }
  }
}
</style>