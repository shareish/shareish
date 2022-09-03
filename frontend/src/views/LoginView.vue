<template>
    <div class="columns">
        <div class="column is-4 is-offset-4">
            <h1 class="title">Log In</h1>

            <p id="errorLog" class="is-danger" style="display: none;">
                The username or the password is invalid, or your account is not activated yet (go check your emails).
            </p>

            <form @submit.prevent="submitForm">
                <div class="field">
                    <label>Email</label>
                    <div class="control">
                        <input type="email" name="email" class="input" v-model="email">
                    </div>
                </div>

                <div class="field">
                    <label>Password</label>
                    <div class="control">
                        <input type="password" name="password" class="input" v-model="password">
                    </div>
                </div>

                <div class="notification is-dnager" v-if="errors.length">
                    <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                </div>

                <div class="field">
                    <div class="control">
                        <button class="button is-succes">Log in</button>
                    </div>
                </div>
            </form>
            <router-link to="/reset-password">You forgot your password?</router-link>
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
        document.title = "Shareish | Log in"
    },
    methods: {
        async submitForm(e){
            axios.defaults.headers.common["Authorization"] = ""
            localStorage.removeItem("token")

            const formData = {
                email: this.email,
                password: this.password
            }

            let logAlert = document.getElementById("errorLog")
            logAlert.style.display = 'none'
            
            axios
                .post("/api/v1/token/login/", formData)
                .then(response => {
                    const token = response.data.auth_token
                    this.$store.commit('setToken', token)
                    axios.defaults.headers.common["Authorization"] = "Token " + token
                    localStorage.setItem("token", token)
                    axios
                        .get("api/v1/users/me/")
                        .then(response => {
                            this.$store.commit('setUserID', response.data['id'])
                            localStorage.setItem("user_id", response.data['id'])
                        })
                        .catch(error => {
                            console.log(JSON.stringify(error))
                        })
                    this.$router.push('/dashboard')
                })
                .catch(error => {
                    logAlert.style.display = 'block'
                    console.log(error)
                })
        }
    },
}
</script>