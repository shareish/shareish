<template>
  <div id="page-sign-up" class="columns is-mobi">
    <div class="column is-6 is-offset-3">
      <h1 class="title">{{ $t('sign-up') }}
        <b-tooltip :label="$t('help_signup')" multilined position="is-right">
          <i class="icon far fa-question-circle"></i>
        </b-tooltip>
      </h1>
        <b-field :message="errors.first('email')" :type="{'is-danger': errors.has('email')}">
          <template #label>
            {{ $t('email') }}
            <b-tooltip :label="$t('help_email')" multilined position="is-bottom">
            <i class="icon far fa-question-circle"></i>
          </b-tooltip>
          </template>
          <b-input v-model="email" name="email" type="email" icon-pack="fas" icon="envelope" expanded v-validate="'required'"/>
        </b-field>

        <b-field :message="errors.first('username')" :type="{'is-danger': errors.has('username')}">
          <template #label>
            {{ $t('username') }}
            <b-tooltip :label="$t('help_username')" multilined position="is-right">
              <i class="icon far fa-question-circle"></i>
            </b-tooltip>
          <b-input v-model="username" name="username"  type="search" icon-pack="fas" icon="user" v-validate="'required'"/>
          </template>
        </b-field>

        <b-field :message="errors.first('first_name')" :type="{'is-danger': errors.has('first_name')}">
          <template #label>
            {{ $t('firstname') }}
            <b-tooltip :label="$t('help_firstname')" multilined position="is-right">
              <i class="icon far fa-question-circle"></i>
            </b-tooltip>
          </template>
          <b-input v-model="first_name" name="first_name"  type="search" icon-pack="fas" icon="user" v-validate="'required'"/>
        </b-field>


        <b-field :message="errors.first('last_name')" :type="{'is-danger': errors.has('last_name')}">
          <template #label>
            {{ $t('lastname') }}
            <b-tooltip :label="$t('help_lastname')" multilined position="is-right">
              <i class="icon far fa-question-circle"></i>
            </b-tooltip>
          </template>
          <b-input v-model="last_name" name="last_name" type="search" icon-pack="fas" icon="user" v-validate="'required'"/>
        </b-field>

        <b-field :message="errors.first('password')" :type="{'is-danger': errors.has('password')}">
          <template #label>
            {{ $t('password') }}
            <b-tooltip :label="$t('help_password')" multilined position="is-right" expanded>
              <i class="icon far fa-question-circle"></i>
            </b-tooltip>
          </template>
          <b-input v-model="password" name="password" type="password" password-reveal icon-pack="fas" icon="lock" expanded v-validate="'required'"/>

        </b-field>
      <div>
      <b-checkbox class="mt-4" v-model="agreement">{{ $t('terms_read_agree')}} <router-link to="/#terms_conditions">{{ $t('terms_conditions_privacy_policy') }}</router-link></b-checkbox>      
	    <hr class="mt-1 mb-1">
      {{ $t('after_registration_settings') }}
      </div>
      <b-button :disabled="!agreement" type="is-primary" class="ml-0 mt-3" :loading="waitingFormResponse" @click="submitForm" expanded>{{ $t('sign-up') }}</b-button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TheSignUpView',
  $_veeValidate: {
    validator: 'new'
  },
  data() {
    return {
      email: '',
      password: '',
      username: '',
      first_name: '',
      last_name: '',
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

      let result = await this.$validator.validateAll();

      if(result){
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
      }
      this.waitingFormResponse = false;
    }
  }
}
</script>
