<template>
  <div id="page-sign-up">
    <div class="column is-4 is-offset-4">
      <h1 class="title">{{ $t('sign-up') }}
        <b-tooltip :label="$t('help_signup')" multilined position="is-right">
          <i class="icon far fa-question-circle"></i>
        </b-tooltip>
      </h1>
      <div>
	<br /><b-checkbox id="agreement" v-model="agreement">{{ $t('terms_read_agree')}} <router-link to="/#terms_conditions">{{ $t('terms_conditions_privacy_policy') }}</router-link></b-checkbox><br /><br />
      </div>
      <div class="field">
        <label>{{ $t('email') }}</label>
        <div class="control">
          <b-tooltip :label="$t('help_email')" multilined position="is-bottom">
            <b-input id="email" v-model="email" name="email" required type="email" icon-pack="fas" icon="envelope"/>
          </b-tooltip>
        </div>
      </div>
      <div class="field">
        <label>{{ $t('username') }}</label>
        <div class="control">
          <b-tooltip :label="$t('help_username')" multilined position="is-bottom">
            <b-input id="username" v-model="username" name="username" required type="search" icon-pack="fas" icon="user"/>
          </b-tooltip>
        </div>
      </div>
      <div class="field">
        <label>{{ $t('firstname') }}</label>
        <div class="control">
          <b-tooltip :label="$t('help_firstname')" multilined position="is-bottom">
            <b-input id="firstname" v-model="first_name" name="first_name" required type="search" icon-pack="fas" icon="user"/>
          </b-tooltip>
        </div>
      </div>
      <div class="field">
        <label>{{ $t('lastname') }}</label>
        <div class="control">
          <b-tooltip :label="$t('help_lastname')" multilined position="is-bottom">
            <b-input id="lastname" v-model="last_name" name="last_name" required type="search" icon-pack="fas" icon="user"/>
          </b-tooltip>
        </div>
      </div>
      <div class="field">
        <label>{{ $t('password') }}</label>
        <div class="control">
          <b-tooltip :label="$t('help_password')" multilined position="is-bottom">
            <b-input id="password" v-model="password" name="password" required type="password" password-reveal icon-pack="fas" icon="lock"/>
          </b-tooltip>
        </div>
      </div>
      <div>
	{{ $t('after_registration_settings') }}
      </div>
      <div class="field">
        <div class="control">
          <b-button :disabled="!agreement" type="is-primary" :loading="waitingFormResponse" @click="submitForm">{{ $t('sign-up') }}</b-button>
        </div>
      </div>
      
      
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TheSignUpView',
  data() {
    return {
      email: '',
      password: '',
      username: '',
      first_name: '',
      last_name: '',
      errors: [],
      agreement: false,	
      waitingFormResponse: false
    }
  },
  mounted() {
    document.title = `Shareish | ${this.$t('sign-up')}`
  },
  methods: {
    async submitForm() {
      this.waitingFormResponse = true;

      this.errors = [];

      const formData = {
        email: this.email,
        password: this.password,
        username: this.username,
        first_name: this.first_name,
        last_name: this.last_name,
      }

      try {
        await axios.post("/api/v1/users/", formData);
        this.$buefy.snackbar.open({
          duration: 5000,
          type: 'is-success',
          message: this.$t('notif-success-user-sign-up'),
          pauseOnHover: true
        });
        await this.$router.push('/log-in');
      }
      catch (error) {
        if (error.response) {
          for (const property in error.response.data) {
            if (Array.isArray(error.response.data[property])) {
              for (const idx in error.response.data[property])
                this.errors.push(`${property}: ${error.response.data[property][idx]}`);
            } else {
              this.errors.push(`${property}: ${error.response.data[property]}`);
            }
          }
          console.log(JSON.stringify(error.response.data));
        } else if (error.message) {
          console.log(JSON.stringify(error.message));
        } else {
          console.log(JSON.stringify(error));
        }

        let errorMessage = this.$t('notif-error-user-sign-up');
        if (this.errors.length > 0) {
          errorMessage = this.errors.join('<br />');
        }

        this.$buefy.snackbar.open({
          duration: 5000,
          type: 'is-danger',
          message: errorMessage,
          pauseOnHover: true
        });
      }

      this.waitingFormResponse = false;
    }
  }
}
</script>
