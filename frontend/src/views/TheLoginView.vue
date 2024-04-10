<template>
  <div id="page-log-in" class="columns">
    <div class="column is-6 is-offset-3">
      <h1 class="title">{{ $t('log-in') }}</h1>
      <b-message v-if="!responseOK" :title="$t('error_keys__BAD_LOGIN')" type="is-danger">
        {{ $t('error_keys__ACCOUNT_DOESNT_EXIST') }}
      </b-message>
        <b-field :label="$t('email-or-username')" :message="errors.first('authValue')" :type="{'is-danger': errors.has('authValue')}">
          <b-input v-model="authValue" name="authValue" icon-pack="fas" icon="user" icon-right="close-circle" icon-right-clickable
                @icon-right-click="clearAuthIconClick" 
                v-validate="'required'"
                />
        </b-field>
      <b-message v-if="showDisabledAccountLink" title="Account disabled" type="is-primary">
        {{ $t('help_login-disabled-account') }} <router-link :to="{name: 'recoverAccount'}">{{ $t('click-here') }}</router-link>.
      </b-message>
      <b-message v-if="showScheduledDeletionAccountLink" title="Account scheduled for deletion" type="is-danger">
        <span v-html="$t('help_login-scheduled-deletion-account', {x: daysBeforeDeletion})" /> <router-link :to="{name: 'recoverAccount'}">{{ $t('click-here') }}</router-link>.
      </b-message> 
      <b-field :label="$t('password')" :message="errors.first('password')" :type="{'is-danger': errors.has('password')}">
        <b-input v-model="password" name="password" password-reveal type="password" icon-pack="fas" icon="lock" v-validate="'required'"/>
      </b-field>
      <router-link :to="{name: 'resetPassword'}">{{ $t('password-forgotten-?') }}</router-link>
      <b-button class="mt-4 ml-0" type="is-primary" :loading="waitingFormResponse" @click="submitForm" expanded>{{ $t('log-in') }}</b-button>
      <div class="has-text-centered"> <!-- Pour centrer le contenu -->
        <p class="mt-5">{{ $t('OR') }}</p>
        <hr class="mt-2"> 
      </div>
      <b-button type="is-primary is-light"
        label="GOOGLE"
        icon-pack="fab"
        icon-left="fab fa-google"
        expanded
        class="ml-0">
      </b-button>
      <b-button type="is-primary is-light"
        label="FACEBOOK"
        icon-pack="fab"
        icon-left="fab fa-facebook"
        expanded
        class="ml-0 mt-2">
      </b-button>
      <b-button type="is-primary is-light"
        label="TWITTER"
        icon-pack="fab"
        icon-left="fab fa-twitter"
        expanded
        class="ml-0 mt-2">
      </b-button>
      <b-button type="is-primary is-light"
        label="MASTODON"
        icon-pack="fab"
        icon-left="fab fa-mastodon"
        expanded
        class="ml-0 mt-2">
      </b-button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import ErrorHandler from "@/mixins/ErrorHandler";

export default {
  name: "TheLoginView",
  mixins: [ErrorHandler],
  $_veeValidate: {
    validator: 'new'
  },
  data() {
    return {
      authValue: '',
      password: '',
      waitingFormResponse: false,
      showDisabledAccountLink: false,
      showScheduledDeletionAccountLink: false,
      daysBeforeDeletion: 0,
      responseOK: true,
    }
  },
  created() {
    document.title = `Shareish | ${this.$t('log-in')}`;
  },
  methods: {
    clearAuthIconClick() {
        this.authValue = '';
    },
    async submitForm() {
      this.waitingFormResponse = true;

      let result = await this.$validator.validateAll();

      if(result){
        const formData = {
          authValue: this.authValue,
          password: this.password
        }

        try {
          const auth = (await axios.post("/api/v1/auth/login/", formData)).data;

          axios.defaults.headers.common["Authorization"] = "Token " + auth['token'];
          this.$store.commit('setToken', auth['token']);
          localStorage.setItem("token", auth['token']);
          this.$store.commit('setUserID', auth['id']);
          localStorage.setItem("user_id", auth['id']);
          
          await this.$router.push('/map');
        }
        catch (error) {
          if (this.isKeyedError(error)) {
            const key = this.getErrorKey(error);
            console.log(key);
            if (key === 'DISABLED_ACCOUNT') {
              this.showDisabledAccountLink = true;
            } else if (key === 'SCHEDULED_DELETION_ACCOUNT') {
              this.showScheduledDeletionAccountLink = true;
              this.daysBeforeDeletion = Number(error.response.data.days_left);
            }
          }
          this.responseOK = false;
        }

      }

      this.waitingFormResponse = false;      
    }
  }
}
</script>
