<template>
  <div id="wrapper" class="wrapper">
    <the-navbar />
    <section class="section">
      <router-view />
    </section>
    <footer class="footer">
      <div class="container">
        <div class="columns">
          <div class="column">
            <h6 class="title is-4 mb-4">Shareish</h6>
            <address class="custom-flex-column">
              <span>XXX Anonymous</span>
              <span>XXX Anonymous</span>
              <span>XXX Anonymous</span>
              <span>XXX Anonymous (for Review)</span>
            </address>
          </div>
          <div class="column">
            <h6 class="title is-4 mb-4">
              {{ $t('useful-links') }}
            </h6>
            <div class="custom-flex-column">
              <router-link :to="{name: 'about'}">{{ $t('about-us') }}</router-link>
              <router-link :to="{name: 'account'}">{{ $t('account') }}</router-link>
              <router-link :to="{name: 'map'}">{{ $t('map') }}</router-link>
              <a href="https://github.com/anonymous">
                <img alt="https://github.com/anonymous" src="./assets/GitHub-Mark-32px.png">
              </a>
            </div>
          </div>
          <div class="column">
            <h6 class="title is-4 mb-4">
              {{ $t('contact') }}
            </h6>
            <div class="custom-flex-column">
              <a href="mailto:info@shareish.org">info@shareish.org</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import axios from "axios"
import TheNavbar from "@/components/TheNavbar.vue";
import ErrorHandler from "@/mixins/ErrorHandler";

export async function logout(instance) {
  try {
    await axios.post("/api/v1/token/logout/");
    axios.defaults.headers.common["Authorization"] = "";
    localStorage.removeItem("token");
    instance.$store.commit('removeToken');
    instance.$store.commit('removeUserID');
    await instance.$router.push("/log-in");
  }
  catch (error) {
    ErrorHandler.methods.snackbarError(error);
  }
}

export default {
  name: 'App',
  components: {TheNavbar},
  beforeCreate() {
    this.$store.commit('initializeStore');
    const token = this.$store.state.token;
    axios.defaults.headers.common['Authorization'] = (token) ? "Token " + token : "";
  }
}
</script>

<style scoped>
.wrapper {
  display: flex;
  height: 100%;
  width: 100%;
  flex-direction: column;
  background: white;
  margin-right: auto;
  margin-left: auto;
}

.custom-flex-column {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
</style>

<style lang="scss">
@import "@/assets/styles/main.scss";

.wbbw {
  word-break: break-word;
}

.wspw {
  white-space: pre-wrap;
}

.v-align-center {
  position: relative;

  & > * {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
  }
}

.w-100 {
  width: 100%;
}
</style>
