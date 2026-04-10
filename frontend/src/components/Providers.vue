<template>
    <div>
        <div class="custom-divider">
            <span>{{$t('pick_provider')}}</span>
        </div>

        <div class="buttons is-centered">
            <b-tooltip label="Google" type="is-dark" position="is-bottom">
                <b-button @click="login('google')">
                    <b-icon pack="fab" icon="google" size="is-medium" type="is-primary"></b-icon>
                </b-button>
            </b-tooltip>
            
            <b-tooltip label="Openstreetmap" type="is-dark" position="is-bottom">
                <b-button @click="login('openstreetmap')">
                    <b-icon pack="fa" icon="map" size="is-medium" type="is-primary"></b-icon>
                </b-button>
            </b-tooltip>
                              
            <b-tooltip label="Wikipedia" type="is-dark" position="is-bottom">
                <b-button @click="login('mediawiki')">
                    <b-icon pack="fab" icon="wikipedia-w" size="is-medium" type="is-primary"></b-icon>
                </b-button>
            </b-tooltip>

            <b-tooltip label="Microsoft" type="is-dark" position="is-bottom">
                <b-button @click="login('microsoft')">
                    <b-icon pack="fab" icon="microsoft" size="is-medium" type="is-primary"></b-icon>
                </b-button>
            </b-tooltip>

            <b-tooltip label="Github" type="is-dark" position="is-bottom">
                <b-button @click="login('github')">
                    <b-icon pack="fab" icon="github" size="is-medium" type="is-primary"></b-icon>
                </b-button>
            </b-tooltip>
        </div>
    </div> 
</template>

<script>
export default({
    data() {
        return {
            ip: "http://127.0.0.1:8000",
        }
    },
    methods:{
        login(provider){
            const endpoints = {
                google: "/accounts/google/login/",
                openstreetmap: "/accounts/oidc/openstreetmap/login/",
                mediawiki: "/accounts/mediawiki/login/",
                microsoft: "/accounts/microsoft/login/",
                github: "/accounts/github/login/"
            };

            const path = endpoints[provider];
            if(path){
                window.location.href = this.ip + path;
            }else{
                console.error("Provider not found");
            }
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
