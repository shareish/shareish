<template>
    <div class="columns">
        <div class="column is-4 is-offset-4">
            <h1 class="title">{{$t('activate-your-account')}}</h1>

            <form @submit.prevent="resendActivation" v-if="allowResend">
                <div class="field">
                    <label>{{$t('email')}}</label>
                    <div class="control">
                        <input type="email" name="email" class="input" v-model="email" required>
                    </div>
                </div>

                <div class="field">
                    <div class="control">
                        <button class="button is-success">{{ $t('resend-activation') }}</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name : 'ActivateEmail',
    data() {
        return {
            email: '',
            errors: [],
            allowResend: false
        }
    },
    mounted(){
        document.title = `Shareish | ${this.$t('activate-your-account')}`;
        this.uid = this.$route.params.uid;
        this.token = this.$route.params.token;
        this.submitActivation();
    },
    methods: {
        async submitActivation(){
          this.errors.splice(0);

            axios.defaults.headers.common["Authorization"] = "";
            localStorage.removeItem("token");

            const formData = {
                uid: this.uid,
                token: this.token
            };

            try {
              await axios.post("/api/v1/users/activation/", formData);
              await this.$router.push('/log-in');
            }
            catch(error) {
              this.allowResend = true;
              let errorMessage;
              if(error.response){
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
                errorMessage = this.errors.join('<br />');
              }
              else if (error.message){
                console.log(JSON.stringify(error.message));
                errorMessage = error.message;
              }
              else{
                console.log(JSON.stringify(error));
                errorMessage = this.$t('notif-error-email-activation');
              }

              this.$buefy.snackbar.open({
                duration: 5000,
                type: 'is-danger',
                message: errorMessage,
                pauseOnHover: true,
              });
            }
        },
        async resendActivation(){
            const formData = {
                email: this.email
            }

            try {
              await axios.post("/api/v1/users/resend_activation/", formData);
              this.$buefy.snackbar.open({
                duration: 5000,
                type: 'is-success',
                message: this.$t('notif-success-resend-activation'),
                pauseOnHover: true,
              });
            }
            catch(error) {
              console.log(error);
              this.$buefy.snackbar.open({
                duration: 5000,
                type: 'is-danger',
                message: this.$t('notif-error-resend-activation'),
                pauseOnHover: true,
              });
            }
        }
    },
}
</script>