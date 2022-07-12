<template>
    <div class="columns">
        <div class="column is-4 is-offset-4">
            <h1 class="title">Log In</h1>

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
    methods: {
        async submitForm(e){
            axios.defaults.headers.common["Authorization"] = ""
            localStorage.removeItem("token")

            const formData = {
                email: this.email,
                password: this.password
            }
            
            axios
                .post("/api/v1/token/login/", formData)
                .then(response => {
                    const token = response.data.auth_token
                    this.$store.commit('setToken', token)
                    axios.defaults.headers.common["Authorization"] = "Token " + token
                    localStorage.setItem("token", token)
                    this.$router.push('/dashboard')
                })
                .catch(error => {
                    if(error.response){
                        for (const property in error.response.data) {
                            this.error.push(`${property}: ${error.response.data[property]}`)
                        }
                        console.log(JSON.stringify(error.response.data))
                    }else if (error.message){
                        console.log(JSON.stringify(error.message))
                    }else{
                        console.log(JSON.stringify(error))
                    }
                })
        }
    },
}
</script>