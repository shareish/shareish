<template>
  <div class="layout-surrounding">
    <template v-if="$route.meta.layout === 'no-navbar'">
      <no-navbar-layout>
        <router-view />
      </no-navbar-layout>
    </template>
    <template v-else>
      <default-layout>
        <router-view />
      </default-layout>
    </template>
  </div>
</template>

<script>
import axios from "axios"
import DefaultLayout from "@/layouts/DefaultLayout.vue";
import NoNavbarLayout from "@/layouts/NoNavbarLayout.vue";


export default {
  name: 'App',
  components: {NoNavbarLayout, DefaultLayout},
  beforeCreate() {
    this.$store.commit('initializeStore');
    const token = this.$store.state.token;
    axios.defaults.headers.common['Authorization'] = (token) ? "Token " + token : "";
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/main.scss";

.wbbw {
  word-break: break-word;
}

.wspw {
  white-space: pre-wrap;
}

.wsnw {
  white-space: nowrap;
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

.w-75 {
  width: 75%;
}

.h-align-center {
  position: relative;

  & > * {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
  }
}

.vh-align-center {
  position: relative;

  & > * {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
}
</style>
