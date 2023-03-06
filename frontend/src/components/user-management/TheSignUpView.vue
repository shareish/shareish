<template>
  <div id="page-sign-up">
    <div class="column is-4 is-offset-4">
      <h1 class="title">{{ $t('sign-up') }}
        <b-tooltip :label="$t('help_signup')" multilined position="is-right">
          <i class="icon far fa-question-circle"></i>
        </b-tooltip>
      </h1>
      <div class="field">
        <label>{{ $t('email') }}</label>
        <div class="control">
          <b-tooltip :label="$t('help_email')" multilined position="is-bottom">
            <input v-model="email" class="input" name="email" required type="email">
          </b-tooltip>
        </div>
      </div>
      <div class="field">
        <label>{{ $t('username') }}</label>
        <div class="control">
          <b-tooltip :label="$t('help_username')" multilined position="is-bottom">
            <input v-model="username" class="input" name="username" required type="text">
          </b-tooltip>
        </div>
      </div>
      <div class="field">
        <label>{{ $t('firstname') }}</label>
        <div class="control">
          <b-tooltip :label="$t('help_firstname')" multilined position="is-bottom">
            <input v-model="first_name" class="input" name="first_name" required type="text">
          </b-tooltip>
        </div>
      </div>
      <div class="field">
        <label>{{ $t('lastname') }}</label>
        <div class="control">
          <b-tooltip :label="$t('help_lastname')" multilined position="is-bottom">
            <input v-model="last_name" class="input" name="last_name" required type="text">
          </b-tooltip>
        </div>
      </div>
      <div class="field">
        <label>{{ $t('password') }}</label>
        <div class="control">
          <b-tooltip :label="$t('help_password')" multilined position="is-bottom">
            <input v-model="password" class="input" name="password" required type="password">
          </b-tooltip>
        </div>
      </div>
      <div class="field">
        <div class="control">
          <b-button class="button is-success" :loading="waitingFormResponse" @click="submitForm">{{ $t('sign-up') }}</b-button>
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
