<template>

    <InfluencerHeaderComp :authenticated="isAuthenticated" />
    <!-- <div> -->
    <!-- <div class="container">
            <div class="row">
                <div>Pending AdRequests</div>
                <div v-for="adrequest in pendingAdRequests" :key="adrequest.id" class="card card-custom text-center">
                    <router-link :to="`/adrequest-detail/${adrequest.id}`">
                        <div class="card-body">
                            <h5 class="card-title">{{ adrequest.sponsor_name }}</h5>
                            <p class="card-text">{{ adrequest.messages }}</p>
                            <p class="card-text">Amount: {{ adrequest.payment_amount }}</p>
                            <span>
                                <button class="btn btn-update mx-2"
                                    @click="approveAdRequest('Accepted', adrequest.id)">Message</button>
                                <button class="btn btn-update mx-2"
                                    @click="approveAdRequest('Accepted', adrequest.id)">Accept</button>
                                <button class="btn btn-delete mx-2"
                                    @click="approveAdRequest('Rejected', adrequest.id)">Reject</button>
                            </span>
                        </div>
                    </router-link>
                </div>

                <div>Accepted AdRequests</div>
                <div v-for="adrequest in acceptedAdRequests" :key="adrequest.id" class="card card-custom text-center">
                    <router-link :to="`/adrequest-detail/${adrequest.id}`">
                        <div class="card-body">
                            <h5 class="card-title">{{ adrequest.influencer_name }}</h5>
                            <p class="card-text">{{ adrequest.messages }}</p>
                            <p class="card-text">Amount: {{ adrequest.payment_amount }}</p>
                            <span>
                            <button class="btn btn-update mx-2" @click="approveAdRequest('Accepted',adrequest.id)">Accept</button>
                            <button class="btn btn-delete mx-2" @click="approveAdRequest('Rejected',adrequest.id)">Reject</button>
                        </span> -->
    <!-- </div>
                    </router-link>
                </div>
            </div>
        </div>
    </div> -->
    <div class="container">
        <div class="row">
            <div>
                <h4>Pending AdRequests</h4>
            </div>
            <div v-for="adrequest in pendingAdRequests" :key="adrequest.id" class="card text-center">
                <div class="card-body">
                    <router-link :to="`/adrequest-detail/${adrequest.id}`" class="router-link-card">
                        <h5 class="card-title">{{ adrequest.campaign_name }}</h5>
                        <div class="title-separator"></div>
                        <p class="card-text">Requested By: {{ adrequest.sponsor_name }}</p>
                        <p class="card-text">Amount: {{ adrequest.payment_amount }}</p>
                    </router-link>
                    <span>
                        <button class="btn btn-success mx-2" @click="navigateToMessages(adrequest)">Message</button>
                        <button class="btn btn-primary mx-2"
                            @click="approveAdRequest('Accepted', adrequest.id)">Accept</button>
                        <button class="btn btn-warning mx-2"
                            @click="approveAdRequest('Rejected', adrequest.id)">Reject</button>
                    </span>
                </div>
            </div>

            <div>
                <h4>Accepted AdRequests</h4>
            </div>
            <div v-for="adrequest in acceptedAdRequests" :key="adrequest.id" class="card text-center">

                <div class="card-body"></div><router-link :to="`/adrequest-detail/${adrequest.id}`"
                    class="router-link-card">

                    <h5 class="card-title">{{ adrequest.campaign_name }}</h5>
                    <div class="title-separator"></div>
                    <p class="card-text">Sponsor:{{ adrequest.sponsor_name }}</p>
                    <p class="card-text">Amount: {{ adrequest.payment_amount }}</p>
                </router-link>
                <span>
                    <button class="btn btn-success mx-2" @click="navigateToMessages(adrequest)">Message</button>
                </span>
            </div>
        </div>

        <!-- </div> -->
    </div>
</template>
<script>
import InfluencerHeaderComp from '@/components/InfluencerHeaderComp.vue';
import axios from 'axios';

export default {
    name: 'InfluencerAdrequest',
    components: {
        InfluencerHeaderComp,
    },
    data() {
        return {
            isAuthenticated: false,
            adrequests: [],
            pendingAdRequests: [],
            acceptedAdRequests: [],
        };
    },
    created() {
        this.fetchAdRequestData();
        this.isAuthenticated = this.checkUserAuthentication();
    },
    methods: {
        checkUserAuthentication() {
            return localStorage.getItem('user-token') !== null;
        }, async fetchAdRequestData() {
            const apiURL = 'http://127.0.0.1:5000/api/GetAdRequestListByInfluencerIdAPI';
            try {
                const token = localStorage.getItem('user-token');
                let response = await axios.get(apiURL, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (response.data.status_code === 200) {
                    this.adrequests = response.data.data;
                    this.pendingAdRequests = this.adrequests.filter(adrequest => adrequest.status === 'Pending');
                    this.acceptedAdRequests = this.adrequests.filter(adrequest => adrequest.status === 'Accepted');
                    console.log("ppppppppppp", this.pendingAdRequests)
                    console.log("accepppppppppppppp", this.acceptedAdRequests)
                } else {
                    console.error("Failed to fetch campaigns:", response.data.message);
                }
            } catch (error) {
                console.error("Error fetching campaigns:", error);
            }
        },
        navigateToMessages(adrequest) {
        this.$router.push({
            name: 'MessagesComp',
            query: {
                sponsorId: adrequest.sponsor_id,
                influencerId: adrequest.influencer_id,
                campaignId: adrequest.campaign_id,
            },
        });
    },
        async approveAdRequest(status, adRequestId) {
            const apiURL = `http://127.0.0.1:5000/api/AdRequest/${adRequestId}`;
            const token = localStorage.getItem('user-token');
            try {
                let response = await axios.put(apiURL, {
                    "status": status
                }, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (response.status === 200) {
                    this.adrequests = this.adrequests.filter(adrequest => adrequest.id !== adRequestId);

                    console.log(`Ad request ${status} successfully.`);
                } else {
                    console.error(`Failed to ${status} ad request:`, response.data.message);
                }
            } catch (error) {
                console.error(`Error ${status} ad request:`, error);
            }
        }
    },
};
</script>

<style scoped>
.router-link-card {
    text-decoration: none; 
    color: inherit; 
    display: block; 
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card {
    width: 25rem;
    margin: 15px;
    background-color: #333; 
    color: #fff;           
    padding: 20px;
    border-radius: 8px;  
    text-align: center;    

}
.title-separator {
    border-bottom: 2px solid #ccc; 
    margin: 10px 0;              
}

.btn-confirm {
    background-color: #4caf50;
    color: #121212;
}

.btn-cancel {
    background-color: #f44336;
    color: #121212;
}
</style>
