<template>
    <div>
    <SponsorHeaderComp :authenticated="isAuthenticated" />
    <div class="container py-5">  
        <div class="card bg-dark text-white p-5" style="width: 40rem; margin-left: auto; margin-right: auto;">
            <div class="card-body">
                <div v-if="successMessage" class="alert alert-success" role="alert">
                    {{ successMessage }}
                </div>
                <div v-if="errorMessage" class="alert alert-danger" role="alert">
                    {{ errorMessage }}
                </div>
                <h3 class="card-title pb-3" style="text-align: center;">Update AdRequest</h3>
                <div class="mb-3">
                    <label for="companyid" class="form-label">Campaign Id</label>
                    <input type="number" style="background-color:darkgray;" class="form-control" id="campaign_id" v-model="campaign_id" readonly>
                </div>
                <div class="mb-3">
                    <label for="company name" class="form-label">Campaign Name</label>
                    <input type="text" style="background-color:darkgray;" class="form-control" id="campaign_name" v-model="campaign_name" readonly>
                </div>
                <div class="mb-3">
                    <label for="influencer_id" class="form-label">InfluencerId</label>
                    <input type="number" style="background-color:darkgray;" class="form-control" id="influencer_id" v-model="influencer_id" readonly>
                </div>
                <div class="mb-3">
                    <label for="influencer_name" class="form-label">Influencer Name</label>
                    <input type="text" style="background-color:darkgray;" class="form-control" id="influencer_name" v-model="influencer_name" readonly>
                </div>
                <div class="mb-3">
                    <label for="requirements" class="form-label">Requirements</label>
                    <input type="text" class="form-control" id="requirements" v-model="requirements">
                </div>
                <div class="mb-3">
                    <label for="payment_amount" class="form-label">Payment Amount</label>
                    <input type="text" class="form-control" id="payment_amount" v-model="payment_amount">
                </div>
                <button class="btn btn-primary" @click="updateAdRequest">Update</button>
            </div>
        </div>
    </div> 
</div> 
</template>

<script>
import axios from 'axios';
import SponsorHeaderComp from '@/components/SponsorHeaderComp.vue';

export default {
    name: 'UpdateAdRequest',
    components: {
        SponsorHeaderComp
    },
    data(){
        return{
            isAuthenticated: this.checkUserAuthentication(),
            campaign_id:"",
            campaign_name:"",
            influencer_id:"",
            influencer_name:"",
            payment_amount:"",
            requirements:"",
        }
    },
    mounted() {
        this.fetchAdRequest();
    },
    methods:{
        checkUserAuthentication() {
            return localStorage.getItem('user-token') !== null;
        },
        async fetchAdRequest() {
            try {
                const adRequestId = this.$route.params.id;
                const apiURL = `http://127.0.0.1:5000/api/AdRequest/${adRequestId}`;
                const token = localStorage.getItem('user-token');
                const response = await axios.get(apiURL, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (response.data.status_code === 200) {
                    console.log("RESSSSSSSSSSSSS",response.data.data)
                    this.campaign_id = response.data.data['campaign_id'];
                    this.campaign_name= response.data.data['campaign_name'];
                    this.influencer_id=response.data.data['influencer_id'];
                    this.influencer_name=response.data.data['influencer_name'];
                    this.payment_amount=response.data.data['payment_amount']
                    this.requirements=response.data.data['requirements'];
                } else {
                    this.errorMessage = response.data.message || 'An error occurred while fetching the data.';
                }
            } catch (error) {
                this.errorMessage = error.response?.data?.message || 'An error occurred while fetching the data.';
            }
        },
         async updateAdRequest(){
             try{
                const adRequestId = this.$route.params.id;
                const apiURL=`http://127.0.0.1:5000/api/AdRequest/${adRequestId}`;
                const token = localStorage.getItem('user-token');
                const profileUpdateData = {
                    "campaign_id": this.campaign_id,
                    "campaign_name": this.campaign_name,
                    "influencer_id": this.influencer_id,
                    "influencer_name": this.influencer_name,
                    "payment_amount": this.payment_amount,
                    "requirements": this.requirements,
                };
                console.log("signupData", profileUpdateData);
            
                let result = await axios.put(apiURL,profileUpdateData,{
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                this.successMessage = "AdRequest updated successfully.";
                this.errorMessage = "";
                setTimeout(() => {
                    this.$router.push("/sponsor-adrequest-list");
                    console.log(result.data);
                }, 2000);

             }
             catch(error){
                console.error('Axios error:', error.message);
                this.errorMessage = "Failed, Please try again.";
                this.successMessage = "";

                setTimeout(() => {
                    this.errorMessage = "";
                    this.successMessage = "";
                }, 2500);
             }
         }
    }
}
</script>

