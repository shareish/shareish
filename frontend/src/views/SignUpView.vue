<template>
    <div class="page-signup">
        <div class="column is-4 is-offset-4">
            <h1 class="title">Sign Up</h1>

            <p id="errorLog" class="is-danger" style="display: none;">
                The username or the email is already taken.
            </p>

            <form @submit.prevent="submitForm">
                <div class="field">
                    <label>E-mail</label>
                    <div class="control">
                        <input type="email" name="email" class="input" v-model="email" required>
                    </div>
                </div>

                <div class="field">
                    <label>Username</label>
                    <div class="control">
                        <input type="text" name="username" class="input" v-model="username" required>
                    </div>
                </div>

                <div class="field">
                    <label>First Name</label>
                    <div class="control">
                        <input type="text" name="first_name" class="input" v-model="first_name" required>
                    </div>
                </div>

                <div class="field">
                    <label>Last Name</label>
                    <div class="control">
                        <input type="text" name="last_name" class="input" v-model="last_name" required>
                    </div>
                </div>

                <div class="field">
                    <label>Password</label>
                    <div class="control">
                        <input type="password" name="password" class="input" v-model="password" required>
                    </div>
                </div>

                <div class="notification is-danger" v-if="errors.length">
                    <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                </div>

                <div class="field">
                    <div class="control">
                        <button class="button is-success">Sign Up</button>
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
        document.title = 'Shareish | Sign up'
    },
    methods: {
        submitForm(e) {
            const formData = {
                email: this.email,
                password: this.password,
                username: this.username,
                first_name: this.first_name,
                last_name: this.last_name,
            }
            let logAlert = document.getElementById("errorLog")
            logAlert.style.display = 'none'
            axios
                .post("/api/v1/users/", formData)
                .then(response => {
                    this.$router.push('/log-in')
                })
                .catch(error => {
                    logAlert.style.display = 'block'
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