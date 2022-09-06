<template>
    <div class="page-item">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Your conversations</h1>
            </div>

            <div class="column is-6" v-for="conversation in conversations" v-bind:key="conversation.id">
                <router-link :to="{ name: 'conversationDetail', params: { id: conversation.id }}" class="button is-light is-normal is-responsive is-hovered" v-if="this.isUp2Date(conversation) == true">{{ conversation.slug }}</router-link>
                <router-link :to="{ name: 'conversationDetail', params: { id: conversation.id }}" class="button is-warning is-normal is-responsive is-hovered" v-else>{{ conversation.slug }}</router-link>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'Conversations',
    data() {
        return {
            conversations: [],
        }
    },
    async mounted() {
        await this.getConversations()
        document.title = "Shareish | My Conversations"
    },
    methods: {
        async getConversations() {
            await axios
                .get('/api/v1/conversations/')
                .then(response => {
                    for(let i = 0; i < response.data.length; i++){
                        this.conversations.push(response.data[i])
                    }
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        },
        isUp2Date(conversation){
            if(this.$store.state.user.id == conversation['owner']){
                if(conversation['up2date_owner'] == true){
                    return true
                }else{
                    return false
                }
            }else{
                if(conversation['up2date_buyer'] == true){
                    return true
                }else{
                    return false
                }
            }
        }
    },
}

</script>