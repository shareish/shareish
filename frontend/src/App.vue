<template>
  <div class="wrapper" id="wrapper">
    <shareish-navbar />
<!--            <div class="navbar-item">-->
<!--              <div class="select is-rounded">-->
<!--                <select v-model="$i18n.locale" @change="changeLanguage">-->
<!--                  <option value="en">En</option>-->
<!--                  <option value="fr">Fr</option>-->
<!--                </select>-->
<!--              </div>-->
<!--            </div>-->
<!--          <template v-else>-->
<!--            <div class="navbar-item" @click="toggleDropdown()">-->
<!--              <router-link to="/">{{ $t('home') }}</router-link>-->
<!--            </div>-->

    <section class="section">
      <router-view />
    </section>

    <footer class="footer">
        <div class="columns">
                <div class="column">
                    <!-- Content -->
                    <h6 class="title is-4 mb-4">Shareish</h6>
                    <!-- <img src="./assets/anonymous_institute.svg" alt="the anonymous Institute">//-->
                    <address>
                        XXX Anonymous
                        <br>XXX Anonymous
                        <br>XXX Anonymous
                        <br>XXX Anonymous (for Review)
                    </address>
                </div>
                <div class="column">
                    <!-- Links -->
                    <h6 class="title is-4 mb-4">
                        {{ $t('useful-links') }}
                    </h6>
                    <p>
                        <a @click="goto('/')" class="text-reset">{{ $t('about-us') }}</a><br />
                        <a @click="goto('/profile')" class="text-reset">{{ $t('profile') }}</a><br />
                        <a @click="goto('/map')" class="text-reset">{{ $t('map') }}</a><br />
                        <a href="https://github.com/anonymous">
                          <img src="./assets/GitHub-Mark-32px.png" alt="https://github.com/anonymous">
                        </a>
                    </p>
                </div>
                <div class="column">
                    <h6 class="title is-4 mb-4">
                        {{ $t('contact') }}
                    </h6>
                    <p>
                        <a href="mailto: info@shareish.org">info@shareish.org</a>
                    </p>
                </div>
        </div>
    </footer>


  </div>
</template>

<script>
  import axios from 'axios'
  import ShareishNavbar from '@/components/ShareishNavbar';

  export default {
    name: 'App',
    components: {ShareishNavbar},
    beforeCreate() {
      this.$store.commit('initializeStore');
      const token = this.$store.state.token;

      if (token) {
        axios.defaults.headers.common['Authorization'] = "Token " + token;
      }
      else {
        axios.defaults.headers.common['Authorization'] = "";
      }
    },

    methods: {
      goto(url) {
        this.$router.push(url)
      },
      // changeLanguage(obj){
      //   localStorage.setItem('language',obj.target.value)
      // },
    },
  }
</script>

<style lang="scss">
@import '@/assets/styles/main.scss';

.wrapper {
  display: flex;
  height: 100%;
  width: 100%;
  flex-direction: column;
  background: white;
}

.section-content {
  flex: 1;
  overflow-y: auto;
  /* position: relative; */
}


  //@import '../node_modules/bulma';
  .is-vcentered {
    display: flex;
    flex-wrap: wrap;
    align-content: center; /* used this for multiple child */
    align-items: center; /* if an only child */
  }
  .wrapper {
    margin-right: auto; /* 1 */
    margin-left: auto; /* 1 */
  }
  .footer {
    height: 220px;
    padding: 5mm;
  }
</style>
