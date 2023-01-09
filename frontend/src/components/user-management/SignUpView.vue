<template>
    <div class="page-signup">
        <div class="column is-4 is-offset-4">
            <h1 class="title">{{$t('sign-up')}} <b-tooltip position="is-right" :label="$t('help_signup')" multilined> <i class="icon far fa-question-circle"></i> </b-tooltip></h1>
	    
            <form @submit.prevent="submitForm">
                <div class="field">
                  <label>{{$t('email')}}</label>
                  <div class="control">
		    <b-tooltip position="is-bottom" :label="$t('help_email')" multilined>
		      <input type="email" name="email" class="input" v-model="email" required>
		      </b-tooltip>
                    </div>
                </div>

                <div class="field">
                    <label>{{$t('username')}}</label>
                    <div class="control">
		      <b-tooltip position="is-bottom" :label="$t('help_username')" multilined>
                        <input type="text" name="username" class="input" v-model="username" required>
			</b-tooltip>
                    </div>
                </div>

                <div class="field">
                    <label>{{ $t('firstname') }}</label>
                    <div class="control">
		      <b-tooltip position="is-bottom" :label="$t('help_firstname')" multilined>
                        <input type="text" name="first_name" class="input" v-model="first_name" required>
		      </b-tooltip>
                    </div>
                </div>

                <div class="field">
                    <label>{{$t('lastname')}}</label>
                    <div class="control">
		      <b-tooltip position="is-bottom" :label="$t('help_lastname')" multilined>
                        <input type="text" name="last_name" class="input" v-model="last_name" required>
			</b-tooltip>
                    </div>
                </div>

                <div class="field">
                  <label>{{$t('password')}}</label>
                  <div class="control">
		    <b-tooltip position="is-bottom" :label="$t('help_password')" multilined>
                      <input type="password" name="password" class="input" v-model="password" required>
		    </b-tooltip>
                    </div>
                </div>

                <div class="field">
                    <div class="control">
                        <button class="button is-success">{{$t('sign-up')}}</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name : 'SignUp',
    data() {
        return {
            email: '',
            password: '',
            username: '',
            first_name: '',
            last_name: '',
            errors: [],
        }
    },
    mounted(){
        document.title = `Shareish | ${this.$t('sign-up')}`
    },
    methods: {
        async submitForm(e) {
            this.errors.splice(0);

            const formData = {
                email: this.email,
                password: this.password,
                username: this.username,
                first_name: this.first_name,
                last_name: this.last_name,
            }
            try {
              await axios.post("/api/v1/users/", formData);
              await this.$router.push('/log-in');
              this.$buefy.snackbar.open({
                duration: 5000,
                type: 'is-success',
                message: this.$t('notif-success-user-sign-up'),
                pauseOnHover: true,
              });
            }
            catch(error) {
                if(error.response) {
                    for (const property in error.response.data) {
                      if (Array.isArray(error.response.data[property])) {
                        for (const idx in error.response.data[property]) {
                          const message = error.response.data[property][idx];
                          this.errors.push(`${property}: ${message}`);
                        }
                      }
                      else {
                        this.errors.push(`${property}: ${error.response.data[property]}`);
                      }
                    }
                    console.log(JSON.stringify(error.response.data));
                }
                else if (error.message) {
                    console.log(JSON.stringify(error.message));
                }
                else {
                    console.log(JSON.stringify(error));
                }

                let errorMessage = this.$t('notif-error-user-sign-up');
                if (this.errors.length > 0) {
                  errorMessage = this.errors.join('<br>');
                }

                this.$buefy.snackbar.open({
                  duration: 5000,
                  type: 'is-danger',
                  message: errorMessage,
                  pauseOnHover: true,
                });
            }
        }
    },
}
</script>
