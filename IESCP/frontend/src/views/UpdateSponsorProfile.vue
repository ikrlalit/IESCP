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
                <h3 class="card-title pb-3" style="text-align: center;">Update Sponsor Profile</h3>
                <div class="mb-3">
                    <label for="companyname" class="form-label">Company/Individual Name</label>
                    <input type="text" class="form-control" id="companyname" v-model="companyname">
                </div>
                <div class="mb-3">
                    <label for="industry" class="form-label">Industry</label>
                    <input type="text" class="form-control" id="industry" v-model="industry">
                </div>
                <div class="mb-3">
                    <label for="budget" class="form-label">Budget</label>
                    <input type="text" class="form-control" id="budget" v-model="budget">
                </div>
                <div class="mb-3">
                    <label for="contactemail" class="form-label">Contact Email</label>
                    <input type="email" class="form-control" id="contactemail" v-model="contactemail">
                </div>
                <div class="mb-3">
                    <label for="websitelink" class="form-label">Website/Social Media Link</label>
                    <input type="text" class="form-control" id="websitelink" v-model="websitelink">
                </div>
                <button class="btn btn-warning" @click="updateSponsorProfile">Update</button>
            </div>
        </div>
    </div> 
</div> 
</template>

<script>
import axios from 'axios';
import SponsorHeaderComp from '@/components/SponsorHeaderComp.vue';

export default {
    name: 'UpdateSponsorProfile',
    components: {
        SponsorHeaderComp
    },
    data(){
        return{
            isAuthenticated: this.checkUserAuthentication(),
            companyname:"",
            industry:"",
            budget:"",
            contactemail:"",
            websitelink:"",
            successMessage: "",
            errorMessage: ""
        }
    },
    mounted() {
        this.fetchProfileData();
    },
    methods:{
        checkUserAuthentication() {
            return localStorage.getItem('user-token') !== null;
        },
        async fetchProfileData() {
            try {
                const apiURL = "http://127.0.0.1:5000/api/NewSponsorProfile";
                const token = localStorage.getItem('user-token');
                const response = await axios.get(apiURL, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (response.data.status_code === 200) {
                    this.companyname = response.data.data['name'];
                    this.industry= response.data.data['industry'];
                    this.budget=response.data.data['budget'];
                    this.contactemail=response.data.data['contact_email'];
                    this.websitelink=response.data.data['website_link']
                } else {
                    this.errorMessage = response.data.message || 'An error occurred while fetching the data.';
                }
            } catch (error) {
                this.errorMessage = error.response?.data?.message || 'An error occurred while fetching the data.';
            }
        },
         async updateSponsorProfile(){
             try{
                const id = this.$route.params.id;
                const apiURL=`http://127.0.0.1:5000/api/NewSponsorProfile/${id}`;
                const token = localStorage.getItem('user-token');
                const profileUpdateData = {
                    "companyname": this.companyname,
                    "industry": this.industry,
                    "budget": this.budget,
                    "contactemail": this.contactemail,
                    "websitelink": this.websitelink,
                };
                console.log("signupData", profileUpdateData);
            
                let result = await axios.put(apiURL,profileUpdateData,{
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                this.successMessage = "Profile updated successfully.";
                this.errorMessage = "";
                setTimeout(() => {
                    this.$router.push("/sponsor-profile");
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
<style>

</style>

