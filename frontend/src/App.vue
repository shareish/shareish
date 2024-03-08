<template>
  <div class="layout-surrounding">
    <template v-if="$route.meta.layout === 'no-navbar'">
      
      <b-notification v-if="showInstallPrompt && !localTimeStorage.value" type="is-info" has-icon class="notification-overlay"> 
        <div class="content">
          <p>{{$t('description-install')}}</p>
          <div class="button-container">
            <b-button @click="dismiss" size="is-small" type="is-light" >{{ $t('button-dismiss') }}</b-button>
            <b-button @click="install" size="is-small" type="is-light" >{{$t('button-install') }}</b-button>
          </div>
        </div>
      </b-notification>

      <no-navbar-layout>
        <router-view />
      </no-navbar-layout>

    </template>
    <template v-else>
      <b-notification v-if="showInstallPrompt && !localTimeStorage.value" type="is-info" has-icon class="notification-overlay"> 
        <div class="content">
          <p>{{$t('description-install')}}</p>
          <div class="button-container">
            <b-button @click="dismiss" size="is-small" type="is-light" >{{ $t('button-dismiss') }}</b-button>
            <b-button @click="install" size="is-small" type="is-light" >{{$t('button-install') }}</b-button>
          </div>
        </div>
      </b-notification>
      
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
  data() {
    return {
      showInstallPrompt: false,
      deferredPrompt: null,
      localTimeStorage : {
        value : false,
      }
    };
  },
  components: {NoNavbarLayout, DefaultLayout},
  beforeCreate() {
    this.$store.commit('initializeStore');
    const token = this.$store.state.token;
    axios.defaults.headers.common['Authorization'] = (token) ? "Token " + token : "";
  },
  created(){
    window.addEventListener("beforeinstallprompt", e => {
      e.preventDefault();
      this.deferredPrompt = e;
      this.showInstallPrompt = true;
    });
    window.addEventListener("appinstalled", () => {
      this.deferredPrompt = null;
      this.showInstallPrompt = false;
    });

    this.checkDismiss();
  },
  methods: {
    dismiss() {
      this.showInstallPrompt = false;
      this.setWithExpiry("isDismiss",true,1)
      this.localTimeStorage.value = true;
      this.checkDismiss();
    },
    install() {
      if (this.deferredPrompt) {
        this.deferredPrompt.prompt();
        this.deferredPrompt.userChoice.then(choiceResult => {
          if (choiceResult.outcome === "accepted") {
            console.log("User accepted the installation");
          } else {
            console.log("User dismissed the installation");
          }
          this.deferredPrompt = null;
          this.showInstallPrompt = false;
        });
      }
    },
    getExpiry(key){
      const itemStr = localStorage.getItem(key);

      if(!itemStr){
        return false
        
      }
      const item = JSON.parse(itemStr)
      const now = new Date()

      if(now.getTime() > item.expiry){
        localStorage.removeItem(key)
        return false
        console.log("expiry date passed, notification sent !")
      }

      console.log("expiry date not yet passed, notification not sent !")

      return item.value
    },
    setWithExpiry(key,value,ttlInDays){

      const now = new Date()
      const ttlInMilliseconds = ttlInDays * 24 * 60 * 60 * 1000;
      const expiry = now.getTime() + ttlInMilliseconds;

      const item = {
        value: value,
        expiry: expiry
      };

      

      console.log("the notification will be re-posted on :"  + new Date(expiry))

      localStorage.setItem(key,JSON.stringify(item));
    },
    checkDismiss() {
      const isDismissed = this.getExpiry("isDismiss");
      if (isDismissed) {
        this.localTimeStorage.value = true;
      }
    }
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

.notification-overlay {
  position: fixed;
  top: 20px;
  right: 20px;
  max-width: 400px; 
  z-index: 9999; 
}

button{
  margin-left: 10px;
}

</style>
