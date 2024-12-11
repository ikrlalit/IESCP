<template>
    <SponsorHeaderComp :authenticated="isAuthenticated" />
    <div class="container">
        <div class="row">
            <div><h4>Pending AdRequests</h4></div>
            <div v-for="adrequest in pendingAdRequests" :key="adrequest.id" class="card text-center">
                    <div class="card-body">
                        <router-link :to="`/adrequest-detail/${adrequest.id}`" class="router-link-card">
                        <h5 class="card-title">{{ adrequest.campaign_name }}</h5>
                        <div class="title-separator"></div>
                        <p class="card-text">Requested to: {{ adrequest.influencer_name }}</p>
                        <p class="card-text">Amount: {{ adrequest.payment_amount }}</p></router-link>
                        <span>
                            <button class="btn btn-success mx-2" @click="navigateToMessages1(adrequest)">Message</button>
                            <router-link :to="`/update-adrequest/${adrequest.id}`"
                                class="btn btn-update mx-2">Update</router-link>
                            <button class="btn btn-delete mx-2" @click="deleteAdRequest(adrequest.id)">Delete</button>
                        </span>
                    </div>
            </div>

            <div><h4>Accepted AdRequests</h4></div>
            <div v-for="adrequest in acceptedAdRequests" :key="adrequest.id" class="card text-center">
                
                    <div class="card-body">
                        <router-link :to="`/adrequest-detail/${adrequest.id}`" class="router-link-card">                        <h5 class="card-title">{{ adrequest.campaign_name }}</h5>
                        <div class="title-separator"></div>
                        <p class="card-text">Accepted By:{{ adrequest.influencer_name }}</p>
                        <p class="card-text">Amount: {{ adrequest.payment_amount }}</p>
                    </router-link>
                        <span>
                            <button class="btn btn-success mx-2" @click="navigateToMessages1(adrequest)">Message</button>
                            
                            <!-- <button v-if="ispaid" class="btn btn-warning mx-2" @click="getPaymentStatus(adrequest)">Pay</button>
                            <button v-if="ispaid" class="btn btn-warning mx-2" disabled>Payed</button> -->
                        
                        </span>
                    </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import SponsorHeaderComp from '@/components/SponsorHeaderComp.vue';

export default {
    name: 'SponsorAdRequestList',
    components: {
        SponsorHeaderComp
    },
    data() {
        return {
            isAuthenticated: false,
            adrequests: [],
            pendingAdRequests: [],
            acceptedAdRequests: [],
            ispaid:false,
        };
    },
    methods: {
        checkUserAuthentication() {
            return localStorage.getItem('user-token') !== null;
        },
        // async getPaymentStatus(adrequest){
        //     const paymentpayload = {
        //     "sponsorId": adrequest.sponsor_id,
        //     "influencerId": adrequest.influencer_id,
        //     "campaignId": adrequest.campaign_id,

        //     }
        //     const apiURL=`http://127.0.0.1:5000/api/GetPaymentStatus`;
        //     const token = localStorage.getItem('user-token');
        //     let result = await axios.post(apiURL,paymentpayload,{
        //             headers: {
        //                 'Authorization': `Bearer ${token}`
        //             }
        //         });
        //     console.log(result)
        //     if (result.data.status_code === 200 && result.data.message==="Data fetched.") {
        //         this.ispaid=true

        //     }else{
        //         this.ispaid=false

        //     }


        // },
        navigateToMessages1(adrequest) {

        console.log("HHHHHHHHHHHHHHHHHHHHHHHHHHH")
        this.$router.push({
            
            name: 'MessageCompSponsor',
            query: {
                sponsorId: adrequest.sponsor_id,
                influencerId: adrequest.influencer_id,
                campaignId: adrequest.campaign_id,
            },
        });
    },
        async fetchAdRequestData() {
            const apiURL = "http://127.0.0.1:5000/api/GetAdRequestListBySponsorIdAPI";
            try {
                const token = localStorage.getItem('user-token');
                let response = await axios.get(apiURL, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (response.data.status_code === 200) {
                    this.adrequests = response.data.data;
                    console.log("DDDDDDDD",this.adrequests )
                    this.pendingAdRequests = this.adrequests.filter(adrequest => adrequest.status === 'Pending');
                    this.acceptedAdRequests = this.adrequests.filter(adrequest => adrequest.status === 'Accepted');
                } else {
                    console.error("Failed to fetch campaigns:", response.data.message);
                }
            } catch (error) {
                console.error("Error fetching campaigns:", error);
            }
        },
        async deleteAdRequest(adRequestId) {
            const confirmed = window.confirm("Are you sure you want to delete this Ad Request?");
            if (!confirmed) {
                return; 
            }
            const apiURL = `http://127.0.0.1:5000/api/AdRequest/${adRequestId}`;
            const token = localStorage.getItem('user-token');
            try {
                let response = await axios.delete(apiURL, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (response.status === 200) {
                    console.log("Success")
                    alert("Ad Request deleted successfully!");
                    await this.fetchAdRequestData();

                } else {
                    console.error(`Failed `, response.data.message);
                }
            } catch (error) {
                console.error(`Error:`, error);
            }
        }
    },
    created() {
        this.isAuthenticated = this.checkUserAuthentication();
        this.fetchAdRequestData();
    }
}
</script>

<style scoped>

.d-flex {
    align-items: center;
    margin: 5px;
}

.btn-update {
    background-color: #ffc107;
    color: white;
}

.btn-add {
    color: white;
    font-size: 45px;
}

.btn-delete {
    background-color: #dc3545;
    color: white;
}

.modal.fade.show {
    display: block;
    background-color: rgba(0, 0, 0, 0.8);
}

.modal-dialog-centered {
    display: flex;
    align-items: center;
    justify-content: center;
}

.modal-content {
    background-color: #2e2e2e;
    color: #e0e0e0;
    padding: 1rem;
    border: none;
}

.btn-confirm {
    background-color: #4caf50;
    color: #121212;
}

.btn-cancel {
    background-color: #f44336;
    color: #121212;
}
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

</style>
