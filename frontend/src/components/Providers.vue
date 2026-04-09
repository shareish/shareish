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
            
            <b-tooltip label="Openstreetmap" type="is-dark" position="is-bottom">
                <b-button @click="oidcOSM">
                    <b-icon pack="fa" icon="map" size="is-medium" type="is-primary"></b-icon>
                </b-button>
            </b-tooltip>
                              
            <b-tooltip label="Wikipedia" type="is-dark" position="is-bottom">
                <b-button @click="oidcWikipedia">
                    <b-icon pack="fab" icon="wikipedia-w" size="is-medium" type="is-primary"></b-icon>
                </b-button>
            </b-tooltip>

            <b-tooltip label="Facebook" type="is-dark" position="is-bottom">
                <b-button @click="oidcFacebook">
                    <b-icon pack="fab" icon="facebook" size="is-medium" type="is-primary"></b-icon>
                </b-button>
            </b-tooltip>

            <b-tooltip label="Microsoft" type="is-dark" position="is-bottom">
                <b-button @click="oidcMicrosoft">
                    <b-icon pack="fab" icon="microsoft" size="is-medium" type="is-primary"></b-icon>
                </b-button>
            </b-tooltip>

            <b-tooltip label="Apple" type="is-dark" position="is-bottom">
                <b-button @click="oidcApple">
                    <b-icon pack="fab" icon="apple" size="is-medium" type="is-primary"></b-icon>
                </b-button>
            </b-tooltip>

            <b-tooltip label="Github" type="is-dark" position="is-bottom">
                <b-button @click="oidcGithub">
                    <b-icon pack="fab" icon="github" size="is-medium" type="is-primary"></b-icon>
                </b-button>
            </b-tooltip>
        </div>
    </div> 
</template>

<script>
export default({
    methods:{
        async oidcGoogle(){
            window.location.href = "http://127.0.0.1:8000/accounts/google/login/";
        },
        async oidcOSM(){
            window.location.href = "http://127.0.0.1:8000/accounts/oidc/openstreetmap/login/";
        },
        async oidcWikipedia(){
            window.location.href = "http://127.0.0.1:8000/accounts/mediawiki/login/";
        },
        async oidcFacebook(){
            window.location.href = "http://127.0.0.1:8000/accounts/facebook/login/";
        },
        async oidcMicrosoft(){
            window.location.href = "http://localhost:8000/accounts/microsoft/login/";
        },
        async oidcApple(){
            window.location.href = "http://127.0.0.1:8000/accounts/apple/login/";
        },
        async oidcGithub(){
            window.location.href = "http://127.0.0.1:8000/accounts/github/login/";
        },
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
