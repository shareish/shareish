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
              <input type="text" class="input" placeholder="Search..." v-model="search">
            </div>
            <div class="control">
              <button class="button is-light is-hovered" @click="submitSearch()">Search</button>
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
              <router-link to="/dashboard/items">Items</router-link>
            </div>
            <div class="navbar-item" @click="toggleDropdown()">
              <router-link to="/dashboard/items/add">Add item</router-link>
            </div>
            <div class="navbar-item" @click="toggleDropdown()">
              <router-link to="/dashboard/my-account">My Account</router-link>
            </div>
            <div class="navbar-item" @click="toggleDropdown()">
              <router-link to="/dashboard/conversations">Chat Rooms</router-link>
            </div>
          </template>

          <template v-else>
            <div class="navbar-item" @click="toggleDropdown()">
              <router-link to="/">Home</router-link>
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
                <router-link to="/sign-up" class="button is-success"><strong>Sign up</strong></router-link>
                <router-link to="/log-in" class="button is-light">Log in</router-link>
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
                    <address> Université de Liège
                        <br>Place du 20-Août, 7
                        <br>B- 4000 Liège, Belgique
                    </address>
                    <!--Replace this with a good address TODO-->
                </div>

                <div class="column">
                    <!-- Links -->
                    <h6 class="title is-4 mb-4">
                        Useful links
                    </h6>
                    <p>
                        <a @click="goto('/')" class="text-reset">Home</a><br />
                        <a @click="goto('/dashboard/my-account')" class="text-reset">Profil</a><br />
                        <!--<a @click="goto('/add-item')" class="text-reset">Add item</a><br />
                        <a @click="goto('/groups')" class="text-reset">Groups</a><br />-->
                        
                    </p>
                </div>

                <div class="column">
                    <h6 class="title is-4 mb-4">
                        Contact
                    </h6>
                    <p>
                        info@example.com
                        <br><a href="tel:+3240123456">+32 4 012 34 56</a>
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
</style>
