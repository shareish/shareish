<template>
    <div class="page-signup">
        <div class="column is-4 is-offset-4">
            <h1 class="title">{{$t('reset-password')}}</h1>

            <form @submit.prevent="submitForm">
                <div class="field">
                    <label>{{$t('email')}}</label>
                    <div class="control">
                        <input type="email" name="email" class="input" v-model="email" required>
                    </div>
                </div>

                <div class="field">
                    <div class="control">
                        <button class="button is-success">{{ $t('reset-password') }}</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name : 'ResetPassword',
    data() {
        return {
            email: '',
            errors: []
        }
    },
    mounted(){
        document.title = `Shareish | ${this.$t('reset-password')}`;
    },
    methods: {
        async submitForm(e) {
            this.errors.splice(0);

            const formData = {
                email: this.email,
            }
            try {
              await axios.post("/api/v1/users/reset_password/", formData);
              await this.$router.push('/');
              this.$buefy.snackbar.open({
                duration: 5000,
                type: 'is-success',
                message: this.$t('notif-success-password-reset-sent'),
                pauseOnHover: true,
              });
            }
            catch(error) {
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
                errorMessage = this.$t('notif-error-password-reset-sent');
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