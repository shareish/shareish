<template>
    <div>
        <div class="custom-divider">
            <span>{{$t('pick_provider')}}</span>
        </div>

        <div class="buttons is-centered">
            <b-tooltip label="Google" type="is-dark" position="is-bottom">
                <b-button @click="login('google')">
                    <img src="@/assets/icons/google.svg" alt="Google">
                </b-button>
            </b-tooltip>
            
            <b-tooltip label="Openstreetmap" type="is-dark" position="is-bottom">
                <b-button @click="login('openstreetmap')">
                    <img src="@/assets/icons/openstreetmap.svg" alt="Openstreetmap">
                </b-button>
            </b-tooltip>
                              
            <b-tooltip label="Wikipedia" type="is-dark" position="is-bottom">
                <b-button @click="login('mediawiki')">
                    <img src="@/assets/icons/wikipedia.svg" alt="Wikipedia">
                </b-button>
            </b-tooltip>

            <b-tooltip label="Microsoft" type="is-dark" position="is-bottom">
                <b-button @click="login('microsoft')">
                    <img src="@/assets/icons/microsoft-icon.svg" alt="Microsoft">
                </b-button>
            </b-tooltip>

            <b-tooltip label="Github" type="is-dark" position="is-bottom">
                <b-button @click="login('github')">
                    <img src="@/assets/icons/github.svg" alt="Github">
                </b-button>
            </b-tooltip>
        </div>
    </div> 
</template>

<script>
import axios from "axios"
export default({
    data() {
        return {
            ip: axios.defaults.baseURL,
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
        padding: 0;
        height: 3rem;
        width: 3rem;
        align-items: center;
        justify-content: center;
    }

    .buttons .button img{
        width: 75%;
        height: 75%;
    }
    
</style>
