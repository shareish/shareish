<template>
  <div id="wrapper">
    <nav class="navbar is-fixed-top is-dark" id="navigation-bar" role="navigation" style="z-index: 99999;">
      <div class="navbar-brand">
        <router-link to="/dashboard" class="navbar-item">
          <img src='../public/mymap/images/logo.png' width="50" height="30" class="navbar-item" alt="Logo">
        </router-link>
        <button role="button" id="navigation-burger" class="navbar-burger" dataTarget="navigation-menu" @click="toggleDropdown">
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
        </button>
      </div>
      <div id="navigation-menu" class="navbar-menu">
        <div class="navbar-start" v-if="$store.state.isAuthenticated">
          <div class="navbar-item field has-addons">
            <div class="control is-expanded">
              <input type="text" class="input" v-bind:placeholder="$t('search')" v-model="search">
            </div>
            <div class="control">
              <button class="button is-light is-hovered" @click="submitSearch()">{{ $t('search') }}</button>
            </div>
          </div>
        </div>
        <div class="navbar-end">
          <template v-if="$store.state.isAuthenticated">
            <div class="navbar-item">
              <div class="select is-rounded">
                <select v-model="$i18n.locale" @change="changeLanguage">
                  <option value="en">En</option>
                  <option value="fr">Fr</option>
                </select>
              </div>
            </div>
            <div class="navbar-item" @click="toggleDropdown()">
              <router-link to="/dashboard">{{ $t('map') }}</router-link>
            </div>
            <div class="navbar-item" @click="toggleDropdown()">
              <router-link to="/dashboard/items">{{ $t('browse') }}</router-link>
            </div>
            <div class="navbar-item" @click="toggleDropdown()">
              <router-link to="/dashboard/items/add">{{ $t('additem') }}</router-link>
            </div>
            <div class="navbar-item" @click="toggleDropdown()">
              <router-link to="/dashboard/my-account">{{ $t('my-account') }}</router-link>
            </div>
            <div class="navbar-item" @click="toggleDropdown()" v-if="$store.state.notifications > 0">
              <router-link to="/dashboard/conversations">{{ $t('chatrooms') }} ({{ $store.state.notifications }})</router-link>
            </div>
            <div class="navbar-item" @click="toggleDropdown()" v-else>
              <router-link to="/dashboard/conversations">{{ $t('chatrooms') }}</router-link>
            </div>
          </template>

          <template v-else>
            <div class="navbar-item" @click="toggleDropdown()">
              <router-link to="/">{{ $t('home') }}</router-link>
            </div>
            <div class="navbar-item">
              <div class="select is-rounded">
                <select v-model="$i18n.locale" @change="changeLanguage">
                  <option value="en">En</option>
                  <option value="fr">Fr</option>
                </select>
              </div>
            </div>
            <div class="navbar-item">
              <div class="buttons">
                <router-link to="/sign-up" class="button is-success" @click="toggleDropdown()"><strong>{{ $t('sign-up') }}</strong></router-link>
                <router-link to="/log-in" class="button is-light" @click="toggleDropdown()">{{ $t('log-in') }}</router-link>
              </div>
            </div>
          </template>
        </div>
      </div>
    </nav>

    <section class="section">
      <router-view/>
    </section>

    <footer class="footer">
        <div class="columns">
                <div class="column">
                    <!-- Content -->
                    <h6 class="title is-4 mb-4">Shareish</h6>
                    <!-- <img src="./assets/anonymous_institute.svg" alt="the anonymous Institute">//-->
                    <address> XXX Anonymous 
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
                        <a @click="goto('/dashboard/my-account')" class="text-reset">{{ $t('my-account') }}</a><br />
                        <a @click="goto('/dashboard')" class="text-reset">{{ $t('map') }}</a><br />
                        <a href="https://github.com/anonymous">
                          <img src="./assets/GitHub-Mark-32px.png" alt="https://github.com/shareish">
                        </a><br />
                        
                    </p>
                </div>

                <div class="column">
                    <h6 class="title is-4 mb-4">
                        {{ $t('contact') }}
                    </h6>
                    <p>
                        <a href = "mailto: info@shareish.org">info@shareish.org</a>
                    </p>

                </div>
        </div>
    </footer>


  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'App',
    beforeCreate() {
      this.$store.commit('initializeStore')
      const token = this.$store.state.token

      if(token){
        axios.defaults.headers.common['Authorization'] = "Token " + token
      }else{
        axios.defaults.headers.common['Authorization'] = ""
      }


    },

    mounted(){
      if(this.$store.state.isAuthenticated){
        axios
          .get('/api/v1/conversations_update/')
          .then(response => {
            console.log(response.data)
            this.$store.state.notifications = response.data
          })
          .catch(error => {
            console.log(error)
          })
      }
    },

    data() {
        return {
            search: '',
            responseSearch: [],
        }
    },

    methods: {
      goto(url) {
        this.$router.push(url)
      },
      changeLanguage(obj){
        localStorage.setItem('language',obj.target.value)
      },
      submitSearch(){
        if(this.search == ''){
          alert('The search is empty.')
          return false
        }else{
          this.$router.push({ name: 'resultsSearch', params: {data: this.search}})
        }
      },
      toggleDropdown(){
        // Display or remove the dropdown menu on the screen.
        const nav = document.getElementById('navigation-menu')
        const burger = document.getElementById('navigation-burger')
        nav.classList.toggle("is-active")
        burger.classList.toggle("is-active")
      }
    },
  }
</script>

<style lang="scss">
  @import '../node_modules/bulma';
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
