<template>
  <div class="box" ref="UserCard">
    <div class="media">
      <div class="media-left">
        <b-carousel class="carousel" :autoplay="false" :arrow-hover="true" :arrow="user.images.length > 1" :indicator="user.images.length > 1">
          <template v-if="user.images.length > 0">
            <b-carousel-item v-for="(image, index) in user.images" :key="index">
              <router-link :to="{name: 'userDetails', params: {id: user.id}}" class="image">
                <b-image :src="image.url" ratio="1by1"></b-image>
              </router-link>
            </b-carousel-item>
          </template>
          <template v-else>
            <b-carousel-item>
              <router-link :to="{name: 'userDetails', params: {id: user.id}}" class="image">
                <b-image ratio="1by1" src="https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg"></b-image>
              </router-link>
            </b-carousel-item>
        </template>
        </b-carousel>
      </div>
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
          <p class="joined mt-2">({{ $t('joined') }} {{ formattedDateFromNow(user.sign_up_date) }})</p>
        </div>
        <p class="description">{{ user.description }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import moment from "moment/moment";
import WindowSize from "@/components/WindowSize";

export default {
  name: 'UserCard',
  mixins: [WindowSize],
  props: {
    user: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      windowResizeWatchedRefsProperties: {
        'UserCard': {
          'clientWidth': 0
        }
      },
      titleSizeClass: null,
      subtitleSizeClass: null,
      mediaLeftSquareSize: null
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
      let mediaLeftSquareSize = 150;
      let titleSizeClass = "is-3";
      let subtitleSizeClass = "is-5";
      if (this.windowResizeWatchedRefsProperties['UserCard']['clientWidth'] < 680) {
        mediaLeftSquareSize = 128;
      }
      if (this.windowResizeWatchedRefsProperties['UserCard']['clientWidth'] < 590) {
        mediaLeftSquareSize = 100;
        titleSizeClass = "is-4";
        subtitleSizeClass = "is-6";
      }
      this.titleSizeClass = titleSizeClass;
      this.subtitleSizeClass = subtitleSizeClass;
      this.mediaLeftSquareSize = mediaLeftSquareSize + "px";
    }
  }
};
</script>

<style scoped>
.media-left, .carousel {
  width: v-bind('mediaLeftSquareSize');
  height: v-bind('mediaLeftSquareSize');
  min-height: v-bind('mediaLeftSquareSize');
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
