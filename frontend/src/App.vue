<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/dashboard" class="navbar-item">
          <img src='../public/mymap/images/logo.png' width="50" height="30" class="navbar-item" alt="Logo">
        </router-link>
      </div>

      <div class="navbar-menu">
        <div class="navbar-end">
          <template v-if="$store.state.isAuthenticated">
            <router-link to="/dashboard/items" class="navbar-item">Items</router-link>
            <router-link to="/dashboard/items/add" class="navbar-item">Add item</router-link>
            <router-link to="/dashboard/my-account" class="navbar-item">My Account</router-link>
          </template>

          <template v-else>
            <router-link to="/" class="navbar-item">Home</router-link>

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
        axios.defaults.headers.common['Authorization'] = "Token" + token
      }else{
        axios.defaults.headers.common['Authorization'] = ""
      }
    },

    methods: {
      goto(url) {
        this.$router.push(url)
      }
    },
  }
</script>

<style lang="scss">
  @import '../node_modules/bulma';
</style>
