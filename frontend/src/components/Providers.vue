<template>
    <div>
        <div class="custom-divider">
            <span>{{$t('pick_provider')}}</span>
        </div>

        <div class="buttons is-centered">
            <b-tooltip label="Google" type="is-dark" position="is-bottom">
                <b-button @click="oidcGoogle">
                    <b-icon pack="fab" icon="google" size="is-medium" type="is-primary"></b-icon>
                </b-button>
            </b-tooltip>
            
            <b-tooltip label="Google" type="is-dark" position="is-bottom">
                <b-button @click="oidcGoogle">
                    <b-icon pack="fab" icon="google" size="is-medium" type="is-primary"></b-icon>
                </b-button>
            </b-tooltip>
                              
            <b-tooltip label="Google" type="is-dark" position="is-bottom">
                <b-button @click="oidcGoogle">
                    <b-icon pack="fab" icon="google" size="is-medium" type="is-primary"></b-icon>
                </b-button>
            </b-tooltip>

            <b-tooltip label="Google" type="is-dark" position="is-bottom">
                <b-button @click="oidcGoogle">
                    <b-icon pack="fab" icon="google" size="is-medium" type="is-primary"></b-icon>
                </b-button>
            </b-tooltip>

            <b-tooltip label="Google" type="is-dark" position="is-bottom">
                <b-button @click="oidcGoogle">
                    <b-icon pack="fab" icon="google" size="is-medium" type="is-primary"></b-icon>
                </b-button>
            </b-tooltip>

            <b-tooltip label="Google" type="is-dark" position="is-bottom">
                <b-button @click="oidcGoogle">
                    <b-icon pack="fab" icon="google" size="is-medium" type="is-primary"></b-icon>
                </b-button>
            </b-tooltip>
        </div>
    </div> 
</template>

<script>
export default({
    methods:{
        async oidcGoogle(){
            window.location.href = "http://localhost:8000/accounts/google/login/";
        }
    },
})
</script>

<style>
    .custom-divider{
        display: flex;
        align-items: center;
        text-align: center;
        margin: 20px 0;
        width: 100%;
    }

    .custom-divider::before,.custom-divider::after{
        content: '';
        flex: 1;
        border-bottom: 1px solid #000;
    }

    .custom-divider span{
        padding: 0 15px;
        color: #7a7a7a;
        font-weight: 500;
        white-space: nowrap;
    }

    .buttons .button{
        height: 3rem;
        width: 3rem;
    }
</style>
