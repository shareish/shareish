<template>
    <div class="columns">
        <div class="column is-4 is-offset-4">
            <h1 class="title">Password reset</h1>

            <p id="errorLog" class="is-danger" style="display: none;">
                The password is invalid.
            </p>

            <form @submit.prevent="submitForm">
                <div class="field">
                    <label>Password</label>
                    <div class="control">
                        <input type="password" name="password" placeholder="Enter your new password here..." class="input" v-model="password">
                    </div>
                </div>

                <div class="field">
                    <div class="control">
                        <button class="button is-succes">Confirm password change</button>
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
        }
    },
    mounted(){
        document.title = 'Shareish | Reset Password Confirm'
        this.uid = this.$route.params.uid
        this.token = this.$route.params.token
    },
    methods: {
        async submitForm(e){
            axios.defaults.headers.common["Authorization"] = ""
            localStorage.removeItem("token")

            const formData = {
                uid: this.uid,
                token: this.token,
                new_password: this.password
            }

            let logAlert = document.getElementById("errorLog")
            logAlert.style.display = 'none'
            
            axios
                .post("/api/v1/users/reset_password_confirm/", formData)
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
    }
}
</script>