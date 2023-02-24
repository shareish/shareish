<template>
    <div class="columns">
        <div class="column is-4 is-offset-4">
            <h1 class="title">{{ $t('reset-password') }}</h1>

            <form @submit.prevent="submitForm">
                <div class="field">
                    <label>{{ $t('password') }}</label>
                    <div class="control">
                        <input type="password" name="password" :placeholder="$t('enter-new-password')" class="input" v-model="password">
                    </div>
                </div>

                <div class="field">
                    <div class="control">
                        <button class="button is-succes">{{$t('reset-password')}}</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name : 'ResetPasswordConfirm',
    data() {
        return {
            uid: '',
            token: '',
            password: '',
            errors: []
        }
    },
    mounted(){
        document.title = `Shareish | ${this.$t('reset-password')}`;
        this.uid = this.$route.params.uid;
        this.token = this.$route.params.token;
    },
    methods: {
        async submitForm(e){
            this.errors.splice(0);

            const formData = {
                uid: this.uid,
                token: this.token,
                new_password: this.password
            };

            try {
              await axios.post("/api/v1/users/reset_password_confirm/", formData);
              await this.$router.push('/');
              this.$buefy.snackbar.open({
                duration: 5000,
                type: 'is-success',
                message: this.$t('notif-success-password-reset'),
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
                errorMessage = this.$t('notif-error-reset-password');
              }

              this.$buefy.snackbar.open({
                duration: 5000,
                type: 'is-danger',
                message: errorMessage,
                pauseOnHover: true,
              });
            }
        }
    }
}
</script>