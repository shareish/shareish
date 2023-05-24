<template>
  <div id="page-home">
    <div id="map-preview" class="box">
      <div class="container">
        <div class="choose-language is-inline-flex mb-3">
          <b-button class="is-small" type="is-info" :outlined="$i18n.locale !== 'fr'" @click="changeLanguage('fr')">FR</b-button>
          <b-button class="is-small" type="is-info ml-2" :outlined="$i18n.locale !== 'en'" @click="changeLanguage('en')">EN</b-button>
        </div>
        <div id="description" class="box">
          <h1 class="title is-size-1">Shareish</h1>
          <p class="subtitle">{{ $t('slogan') }}</p>
          <h2 class="title is-size-4 mb-4">{{ $t('what-is-shareish') }}</h2>
          <p class="text">{{ $t('shareish_description') }}</p>
          <div class="is-flex is-flex-wrap-wrap mt-3">
            <template v-if="!$store.state.isAuthenticated">
              <router-link :to="{name: 'signup'}" class="button is-primary">{{ $t('sign-up') }}</router-link>
              <router-link :to="{name: 'login'}" class="button is-primary ml-2">{{ $t('log-in') }}</router-link>
            </template>
            <template v-else>
              <router-link :to="{name: 'map'}" class="button is-primary">{{ $t('enter-shareish') }}</router-link>
            </template>
          </div>
        </div>
      </div>
    </div>
    <div id="faq" class="container pt-3">
      <h2 class="subtitle"><b>{{ $t('how-does-it-work') }}</b></h2>
      <p>
        <router-link :to="{name: 'signup'}">{{ $t('after_registration') }}</router-link> {{ $t('andet') }}
        <router-link :to="{name: 'login'}">{{ $t('logged_in') }}</router-link>, Shareish {{ $t('offers') }}
        <router-link :to="{name: 'map'}">{{ $t('interactive_map') }}</router-link> {{ $t('shareish_description2') }}.
      </p>
      <br />

      <br />
      <br />
      <h2 class="subtitle is-size-3 has-text-centered" style="margin-bottom: 2rem;"><b>{{ $t('faq') }}</b></h2>

      <p>
        <b>{{ $t('faq_nothing') }} </b><br />
        <i>{{ $t('faq_nothing_answer') }}. </i>
      </p>
      <br />

      <p>
        <b>{{ $t('faq_examples') }} </b><br />
        <i>{{ $t('faq_examples_answer') }}</i>
      </p>
      <br />

      <!-- can you give me exemples of services: promener chiens, faire courses, aller à la pharmacie, déposer qqun quelque part, citer exemple covid etc.... //-->

      <p>
        <b>{{ $t('faq_everything') }}</b><br />
        <i>{{ $t('faq_everything_answer') }}</i>
      </p>
      <br />

      <p>
        <b>{{ $t('faq_colors') }}</b><br />
        <i>{{ $t('faq_colors_answer') }}</i>
      </p>
      <br />

      <p>
        <b>{{ $t('faq_address') }}</b><br />
        <i>{{ $t('faq_address_answer') }}</i>
      </p>
      <br />

      <p>
        <b>{{ $t('faq_device') }}</b><br />
        <i>{{ $t('faq_device_answer') }}</i>
      </p>
      <br />

      <p ref="gdpr">
        <b>{{ $t('faq_data_collection') }}</b><br />
        <i>{{ $t('faq_data_collection_answer') }}.</i>
      </p>
      <br />

      <p>
        <b>{{ $t('faq_public_resources') }}</b><br />
        <i>
          {{ $t('faq_public_resources_answer') }}
          <a href="https://wiki.openstreetmap.org/wiki/Editors">editor tools</a>,
          <a href="https://mapcomplete.osm.be/">MapComplete</a> (web),
          <a href="https://wiki.openstreetmap.org/wiki/StreetComplete">StreetComplete</a> (Android),
          <a href="https://wiki.openstreetmap.org/wiki/OSM_Contributor">OSMand Contributor</a> (Android),
          <a href="https://wiki.openstreetmap.org/wiki/Go_Map!!">Go Map!!!</a> (macOS).
        </i>
      </p><br />

      <p>
        <b>{{ $t('faq_how_to_contribute') }}</b><br />
        <i>{{ $t('faq_how_to_contribute_answer') }}</i>
      </p>
      <br />

      <p>
        <b>{{ $t('faq_local_instance') }}</b><br />
        <i>{{ $t('faq_local_instance_answer') }}</i>
      </p>
      <br />

      <p>
        <b>{{ $t('faq_who') }}</b><br />
        <i>{{ $t('faq_who_answer') }}</i>
      </p>
      <br />

      <p>
        <b>{{ $t('faq_further') }}</b><br />
        <i>{{ $t('faq_further_answer') }} <a href="mailto:info@shareish.org">info@shareish.org</a>.</i>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TheHomeView',
  components: {},
  mounted() {
      document.title = "Shareish"
      
      if (this.$route.hash === '#gdpr') this.$refs['gdpr'].scrollIntoView();

  },
  methods: {
    changeLanguage(lang) {
      localStorage.setItem('language', lang);
      this.$i18n.locale = lang;
    }
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/styles/colors.scss";

#map-preview {
  background-image: url(../assets/mapview_2200_gradient_light.jpg);
  background-position: center -50px;
  background-repeat: no-repeat;
  padding-top: 200px;
  image-rendering: pixelated;

  #description {
    width: 500px;
    background-color: white;
    padding: 1.5rem;
    border-radius: 5px;

    h1 {
      font-size: 3rem;
      margin-top: -5px;
    }
    .subtitle {
      font-size: 1.4rem;
      margin-bottom: 2rem !important;
    }
    h2 {
      margin-top: 2rem !important;
    }
  }
}

#faq {
  margin-bottom: 3rem;
}

@media screen and (max-width: 1024px) {
  #map-preview {
    padding-top: 350px;

    #description {
      width: 100%;
    }
  }

  #faq {
    padding: 0 3rem;
  }
}

@media screen and (max-width: 1024px) {

}
</style>
