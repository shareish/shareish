<template>
    <div class="page-signup">
        <div class="column is-4 is-offset-4">
            <h1 class="title">Password reset</h1>
            <p>
                Indicate your email address so that we can send you an email to reset your password.
            </p>

            <p id="errorLog" class="is-danger" style="display: none;">
                The email does not exist.
            </p>

            <form @submit.prevent="submitForm">
                <div class="field">
                    <label>E-mail</label>
                    <div class="control">
                        <input type="email" name="email" class="input" v-model="email" required>
                    </div>
                </div>

                <div class="field">
                    <div class="control">
                        <button class="button is-success">Send email</button>
                    </div>
                </div>
            </form>

            <p id="successReset" class="is-danger" style="display: none;">
                The email have been sent. Go check your emails to finish the reset of your password.
            </p>
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
        }
    },
    mounted(){
        document.title = 'Shareish | Password reset'
    },
    methods: {
        submitForm(e) {
            const formData = {
                email: this.email,
            }
            let successReset = document.getElementById("successReset")
            successReset.style.display ='none'
            let logAlert = document.getElementById("errorLog")
            logAlert.style.display = 'none'
            axios
                .post("/api/v1/users/reset_password/", formData)
                .then(response => {
                    successReset.style.display = 'block'
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