<template>
    <div class="columns">
        <div class="column is-4 is-offset-4">
            <h1 class="title">{{$t('log-in')}}</h1>

            <form @submit.prevent="submitForm">
                <div class="field">
                    <label>{{ $t('email') }}</label>
                    <div class="control">
                        <input type="email" name="email" class="input" v-model="email">
                    </div>
                </div>

                <div class="field">
                    <label>{{ $t('password') }}</label>
                    <div class="control">
                        <input type="password" name="password" class="input" v-model="password">
                    </div>
                </div>

                <div class="notification is-danger" v-if="errors.length">
                    <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                </div>

                <div class="field">
                    <div class="control">
                        <button class="button is-success">{{$t('log-in')}}</button>
                    </div>
                </div>
            </form>
            <router-link to="/reset-password">{{ $t('password-forgotten-?') }}</router-link>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: "Login",
    data() {
        return {
            email: '',
            password: '',
            errors: []
        }
    },
    mounted() {
        document.title = `Shareish | ${this.$t('log-in')}`;
    },
    methods: {
        async submitForm(e){
            const formData = {
                email: this.email,
                password: this.password
            }

            try {
              const response = await axios.post("/api/v1/token/login/", formData);
              const token = response.data.auth_token;
              axios.defaults.headers.common["Authorization"] = "Token " + token;
              this.$store.commit('setToken', token);
              localStorage.setItem("token", token);

              const user = (await axios.get("api/v1/users/me/")).data;
              this.$store.commit('setUserID', user['id']);
              localStorage.setItem("user_id", user['id']);

              await this.$router.push('/dashboard');
            }
            catch (error) {
              console.log(error);
              this.$buefy.snackbar.open({
                duration: 5000,
                type: 'is-danger',
                message: this.$t('notif-error-user-login'),
                pauseOnHover: true,
              });
            }
        }
    },
}
</script>