<template>
    <div class="box">
        <div class="columns">
            <div class="column is-3 mb-2">
                <button class="button is-danger is-responsive" @click="openModal">Delete Conversation</button>
            </div>
            <div class="column is-3 is-offset-3 mb-2">
                <button class="button is-info is-responsive" @click="gotoItem">Go to Item</button>
            </div>
        </div>
        
        <div class="container" id="confirm">
            <div class="modal" id="modal">
                <div class="modal-background"></div>
                <div class="modal-content">
                    <div class="box">
                        <h1 class="title">Do you really want to delete this conversation?</h1>
                        <div class="columns is-centered p-2">
                            <button class="button is-info column is-3 p-2" @click="deleteConversation">Delete</button>
                            <button class="button is-danger column is-3 is-offset-3 p-2" @click="closeModal">Cancel</button>
                        </div>
                    </div>
                </div>
                
            </div>
        </div>
        <div class="conv-messages"  v-for="message in messages" v-bind:key="message.id" id="conv-messages">
            <article class="message is-dark" v-if="message.user != userID">
                <div class="message-body">
                    {{ message.content }}
                </div>
            </article>
            <article class="message" v-else>
                <div class="message-body">
                    {{ message.content }}
                </div>
            </article>
        </div>
        <div class="conv-messages" id="conv-messages-new"></div>

        <article class="message">
            <div class="message-body">
                <div class="columns">
                    <div class="column is-two-thirds">
                        <label for="newMessage">Message</label>
                        <div class="field">
                            <div class="control">
                                <textarea class="textarea is-rounded" placeholder="" id="newMessage" name="newMessage" v-model="message" required>
                                </textarea>
                            </div>
                        </div>
                    </div>
                    <div class="column is-one-third is-centered is-vcentered">
                        <div class="field">
                            <button class="button is-info" @click="sendMessage">Send</button>
                        </div>
                    </div>
                </div>
            </div>
        </article>
    </div>    
</template>

<script>
import axios from 'axios'
export default {
    name: 'ConversationDetail',
    data() {
        return {
            conversation: {},
            message: '',
            ws: null,
            messages: [],
            conversationID: null,
        }
    },
    beforeRouteLeave (to, from, next) {
        this.beforeWindowUnload()
        next()
    },
    beforeDestroy() {
        window.removeEventListener('beforeunload', this.beforeWindowUnload)
    },
    async mounted() {
        this.conversationID = this.$route.params.id
        this.userID = this.$store.state.user.id
        window.addEventListener('beforeunload', this.beforeWindowUnload)
        await this.getConversation()
        await this.getMessages()
        await this.createWebSocket()
    },
    methods: {
        async getConversation() {
            await axios
                .get(`/api/v1/conversations/${this.conversationID}`)
                .then(response => {
                    this.conversation = response.data
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        },
        async getMessages() {
            let maxlength = this.conversation['messages'].length
            for(let i = 0; i < maxlength; i++){
                await axios
                    .get(`/api/v1/messages/${this.conversation['messages'][i]}`)
                    .then(response => {
                        this.pushMessages(response.data)
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })
            }
        },
        async createWebSocket(){
            console.log("Starting connection to WebSocket Server")

            this.ws = new WebSocket(
                'ws://'
                + window.location.hostname 
                + '/ws/'
                + this.conversation['name']
                + '/'
            )

            this.ws.addEventListener("message", (e) => {
                const data = JSON.parse(e.data)
                if(data.content){
                    if(data.user_id == this.userID){
                        document.querySelector('#conv-messages-new').innerHTML += '<article class="message"> <div class="message-body">' + data.content + '</div></article>'
                    }else{
                        document.querySelector('#conv-messages-new').innerHTML += '<article class="message is-dark"> <div class="message-body">' + data.content + '</div></article>'
                    }
                    
                }else{
                    alert('The message was empty')
                }
            })

            this.ws.onclose = function(e) {
                console.log(e)
                console.log("Closed")
            }

            this.ws.onopen = function(e) {
                console.log(e)
                console.log("Successfully connected to the echo websocket server...")
            }
        },
        pushMessages(message){
            this.messages.push(message)
        },
        sendMessage(){
            this.ws.send(
                JSON.stringify({
                    'content': this.message,
                    'conversation_id': this.conversation['id'],
                    'user_id': this.userID,
                })
            )
            this.message = ''
            return false;
        },
        beforeWindowUnload(e) {
            this.ws.close()  
        },
        openModal(){
            let elem = document.getElementById("modal")
            elem.classList.add("is-active")
        },
        closeModal(){
            let elem = document.getElementById("modal")
            elem.classList.remove("is-active")
        },
        deleteConversation(){
            axios
                .delete(`/api/v1/conversations/${this.conversationID}/`)
                .then(_ => {
                    this.$router.push('/dashboard/conversations')
                })
                .catch(error => {
                    alert('You cannot delete this conversation.')
                    console.log(JSON.stringify(error))
                })
        },
        gotoItem(){
            this.$router.push({ name: 'itemDetail', params: { id: this.conversation['item'] }})
        }
    },
}
</script>

<style scoped>
.is-vcentered {
  display: flex;
  flex-wrap: wrap;
  align-content: center;
  align-items: center;
}
</style>