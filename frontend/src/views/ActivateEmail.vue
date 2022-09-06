<template>
    <div class="columns">
        <div class="column is-4 is-offset-4">
            <h1 class="title">Account activation</h1>

            <p id="errorLog" class="is-danger" style="display: none;">
                The activation went wrong.
            </p>

            <form @submit.prevent="resendActivation">
                <div class="field">
                    <label>E-mail</label>
                    <div class="control">
                        <input type="email" name="email" class="input" v-model="email" required>
                    </div>
                </div>

                <div class="field">
                    <div class="control">
                        <button class="button is-success">Resend activation</button>
                    </div>
                </div>
            </form>
            <p id="resend" class="is-success" style="display: none;">The activation email has been resent.</p>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name : 'ResetPasswordConfirm',
    data() {
        return {
            email: ''
        }
    },
    mounted(){
        document.title = 'Shareish | Email Activation'
        this.uid = this.$route.params.uid
        this.token = this.$route.params.token
        this.submitActivation()
    },
    methods: {
        async submitActivation(){
            axios.defaults.headers.common["Authorization"] = ""
            localStorage.removeItem("token")

            const formData = {
                uid: this.uid,
                token: this.token
            }

            let logAlert = document.getElementById("errorLog")
            logAlert.style.display = 'none'
            
            axios
                .post("/api/v1/users/activation/", formData)
                .then(response => {
                    this.$router.push('/dashboard')
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
        },
        resendActivation(){
            let resend = document.getElementById("resend")
            resend.style.display = 'none'

            let logAlert = document.getElementById("errorLog")
            logAlert.style.display = 'none'

            const formData = {
                email: this.email
            }

            axios
                .post("/api/v1/users/resend_activation/", formData)
                .then(response => {
                    resend.style.display = 'block'
                })
                .catch(error => {
                    logAlert.style.display = 'block'
                    console.log(error)
                })
        }
    },
}
</script>