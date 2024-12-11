<template>
    <div>
        <SponsorHeaderComp :authenticated="isAuthenticated" />
        <div class="container chat-container">
            <div class="row">
                <!-- Chat Title -->
                <div class="chat-title">
                    <h3>{{ activeChatName }}</h3>
                </div>
                <!-- Chat Box -->
                <div class="chat-box">
                    <div class="messages">
                        <div v-for="message in messages" :key="message.id"
                            :class="['message', message.sender === 'me' ? 'sent' : 'received']">
                            <p>{{ message.messages }}</p>
                        </div>
                    </div>
                    <div class="input-area">
                        <input type="text" v-model="newMessage" @keyup.enter="sendMessage"
                            placeholder="Type a message..." />
                        <button @click="sendMessage">Send</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import SponsorHeaderComp from '@/components/SponsorHeaderComp.vue';
import axios from 'axios';

export default {
    name: 'MessageCompSponsor',
    components: {
        SponsorHeaderComp,
    },
    data() {
        return {
            isAuthenticated: false,
            activeChatName: 'Chat', 
            sponsorId: this.$route.query.sponsorId || '', 
            influencerId: this.$route.query.influencerId || '',
            campaignId: this.$route.query.campaignId || '',
            messages: [],
            newMessage: '', 
        };
    },
    created() {
        this.isAuthenticated = this.checkUserAuthentication();
        this.fetchMessages();
    },
    methods: {
        checkUserAuthentication() {
            return localStorage.getItem('user-token') !== null;
        },
        async fetchMessages() {
            const apiURL = 'http://127.0.0.1:5000/api/GetAllMessages';
            console.log("DSSSSSSSSSSSSSSSSSS111111", this.sponsorId, this.influencerId, this.campaignId)
            try {
                const token = localStorage.getItem('user-token');
                const payload = {
                    "sponsor_id": this.sponsorId,
                    "campaign_id": this.campaignId,
                    "influencer_id": this.influencerId
                }
                let response = await axios.post(apiURL, payload, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                if (response.data.status_code === 200) {
                    this.messages = response.data.data;
                    console.log("mssssssssssg", response.data.data)
                } else {
                    console.error('Failed to fetch messages:', response.data.message);
                }
            } catch (error) {
                console.error('Error fetching messages:', error);
            }
        },
        async sendMessage() {
            if (!this.newMessage.trim()) return;
            const token = localStorage.getItem('user-token');



            try {
                const payloaddata = {
                    campaign_id: this.campaignId,
                    influencer_id: this.influencerId,
                    sponsor_id:this.sponsorId,
                    messages: this.newMessage,
                };

                const apiURL1 = "http://127.0.0.1:5000/api/AddNewMessage";
                const response = await axios.post(apiURL1, payloaddata, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                if (response.data.status_code === 200) {
                    // this.messages.push({ text: this.newMessage });
                    // this.newMessage = '';
                    this.fetchMessages()

                } else {
                    console.error('Failed to send message:', response.data.message);
                }
            } catch (error) {
                console.error('Error sending message:', error);
            }
        },
    },
};
</script>
<style scoped>
.chat-container {
    margin-top: 20px;
}

.chat-title {
    text-align: center;
    margin-bottom: 10px;
}

.chat-box {
    border: 1px solid #ccc;
    border-radius: 10px;
    padding: 10px;
    height: 400px;
    display: flex;
    text-decoration-color: black;
    flex-direction: column;
    justify-content: space-between;
    background-color: #f9f9f9;
}

.messages {
    overflow-y: auto;
    flex-grow: 1;
    padding: 10px;
    margin-bottom: 10px;
    color: black;
}

.message {
    margin: 5px 0;
    padding: 10px;
    border-radius: 8px;
    max-width: 70%;
}

.sent {
    background-color: #cce5ff;
    align-self: flex-end;
}

.received {
    background-color: #e2e3e5;
    align-self: flex-start;
}

.input-area {
    display: flex;
    gap: 10px;
}

input[type='text'] {
    flex: 1;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
}

button {
    padding: 10px 15px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

button:hover {
    background-color: #0056b3;
}
</style>