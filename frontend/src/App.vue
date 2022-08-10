<template>
  <div id="wrapper">
    <nav class="navbar is-fixed-top is-dark" style="z-index: 99999;">
      <div class="navbar-brand">
        <router-link to="/dashboard" class="navbar-item">
          <img src='../public/mymap/images/logo.png' width="50" height="30" class="navbar-item" alt="Logo">
        </router-link>
        <!-- <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false">
          <span aria-hidden="false">salut</span>
          <span aria-hidden="true">coucou</span>
          <span>gobaby</span>
        </a> -->
        <!-- <div class="navbar-burger">
          <template v-if="$store.state.isAuthenticated">
            <div class="navbar-item">
              <div class="select is-rounded">
                <select v-model="$i18n.locale" @change="changeLanguage">
                  <option value="en">En</option>
                  <option value="fr">Fr</option>
                </select>
              </div>
            </div>
            <router-link to="/dashboard/items" class="navbar-item">Items</router-link>
            <router-link to="/dashboard/items/add" class="navbar-item">Add item</router-link>
            <router-link to="/dashboard/my-account" class="navbar-item">My Account</router-link>
            <router-link to="/dashboard/conversations" class="navbar-item">Chat Rooms</router-link>
          </template>

          <template v-else>
            <router-link to="/" class="navbar-item">Home</router-link>
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
        </div> -->
      </div>

      <div class="navbar-menu">
        <div class="navbar-start">
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
            <router-link to="/dashboard/items" class="navbar-item">Items</router-link>
            <router-link to="/dashboard/items/add" class="navbar-item">Add item</router-link>
            <router-link to="/dashboard/my-account" class="navbar-item">My Account</router-link>
            <router-link to="/dashboard/conversations" class="navbar-item">Chat Rooms</router-link>
          </template>

          <template v-else>
            <router-link to="/" class="navbar-item">Home</router-link>
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
      }
    },
  }
</script>

<style lang="scss">
  @import '../node_modules/bulma';
</style>

<style scoped>

</style>
