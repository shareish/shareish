<template>
  <div class="box" ref="UserCard">
    <div class="media">
      <figure class="media-left">
        <router-link :to="{name: 'userDetails', params: {id: user.id}}" class="image">
          <b-image v-if="user.images.length > 0" :src="user.images[user.images.length - 1]" ratio="1by1"></b-image>
          <b-image v-else ratio="1by1" src="https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg"></b-image>
        </router-link>
      </figure>
      <div class="media-content">
        <h2 class="title" :class="titleSizeClass">{{ user.first_name }} {{ user.last_name }}</h2>
        <div class="subtitle mb-3" :class="subtitleSizeClass">
          <router-link :to="{name: 'userDetails', params: {id: user.id}}">@{{ user.username }}</router-link>
          <template v-if="hasOneSocial">
            &middot;
            <nav class="socials">
              <small>
                <a v-if="user.homepage_url" :href="user.homepage_url" class="social" target="_blank">
                  <span class="icon is-small"><i class="fas fa-globe"></i></span>
                </a>
                <a v-if="user.facebook_url" :href="user.facebook_url" class="social" target="_blank">
                  <span class="icon is-small"><i class="fab fa-facebook"></i></span>
                </a>
                <a v-if="user.instagram_url" :href="user.instagram_url" class="social" target="_blank">
                  <span class="icon is-small"><i class="fab fa-instagram"></i></span>
                </a>
              </small>
            </nav>
          </template>
          <p class="joined mt-2">({{ $t('joined') }} {{ formattedDateFromNow(user.sign_in_date) }})</p>
        </div>
        <p class="description">{{ user.description }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment/moment';
import WindowSize from "@/components/WindowSize";

export default {
  name: 'UserCard',
  mixins: [WindowSize],
  props: {
    user: Object
  },
  data() {
    return {
      windowResizeWatchedRefsProperties: {
        "UserCard": {
          "clientWidth": 0
        }
      },
      titleSizeClass: null,
      subtitleSizeClass: null,
      userImageSize: null
    }
  },
  computed: {
    hasOneSocial() {
      return (this.user.homepage_url || this.user.facebook_url || this.user.instagram_url);
    }
  },
  methods: {
    formattedDateFromNow(date) {
      return moment(date).locale(this.$i18n.locale).fromNow();
    },
    windowWidthChanged() {
      let userImageSize = 128;
      let titleSizeClass = "is-3";
      let subtitleSizeClass = "is-5";
      if (this.windowResizeWatchedRefsProperties["UserCard"]["clientWidth"] < 680) {
        userImageSize = 96;
      }
      if (this.windowResizeWatchedRefsProperties["UserCard"]["clientWidth"] < 590) {
        userImageSize = 72;
        titleSizeClass = "is-4";
        subtitleSizeClass = "is-6";
      }
      this.titleSizeClass = titleSizeClass;
      this.subtitleSizeClass = subtitleSizeClass;
      this.userImageSize = userImageSize + "px";
    }
  }
};
</script>

<style scoped>
.media-left .image {
  width: v-bind('userImageSize');
}

.joined {
  font-size: 0.8rem;
}

nav.socials {
  display: inline-block;
}

nav.socials a.social {
  margin-right: 5px;
}

nav.socials a.social:last-child {
  margin-right: 0;
}




.media-right button {
  margin-left: 8px;
}
.media-right button:first-child {
  margin-left: 0;
}
</style>
