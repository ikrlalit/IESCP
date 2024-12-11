<template>
    <SponsorHeaderComp :authenticated="isAuthenticated" />

    <div class="container">
        <div class="input-group mb-3">
            <input type="text" class="form-control p-2" placeholder="find influencers ... " v-model="searchquery">
            <button class="btn btn-warning" type="submit" @click="sponsorDashboardSearch" >Search</button>
        </div>
    </div>
    <div class="container">
        <div v-if="searchresult.length > 0">
            <div class="row">
                <div v-for="(influencer, index) in searchresult" :key="index" class="col-md-4 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">{{ influencer.name }}</h5>
                            <div class="title-separator"></div>
                            <p class="card-text"><strong>Category:</strong> {{ influencer.category }}</p>
                            <p class="card-text"><strong>Niche:</strong> {{ influencer.niche }}</p>

                            <div class="social-media-icons mt-3">
                                <a :href="influencer.instagram_link" target="_blank" class="me-3" title="Instagram">
                                    <i class="bi bi-instagram"></i> {{ influencer.instagram_follower }}
                                </a>
                                <a :href="influencer.twitter_link" target="_blank" class="me-3" title="Twitter">
                                    <i class="bi bi-twitter"></i> {{ influencer.twitter_follower }}
                                </a>
                                <a :href="influencer.youtube_link" target="_blank" title="YouTube">
                                    <i class="bi bi-youtube"></i> {{ influencer.youtube_follower }}
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-else>
            No Result Found
        </div>
        </div>
</template>

<script>
import axios from 'axios';
import SponsorHeaderComp from '@/components/SponsorHeaderComp.vue';

export default {
    name: 'SponsorSearchResult',
    components: {
        SponsorHeaderComp
    },
    data() {
        return {
            isAuthenticated: this.checkUserAuthentication(),
            searchquery : "",
            searchresult:[]
        }

    },
    mounted() {
        this.searchquery = this.$route.query.q || "";
        if (this.searchquery) {
            this.sponsorDashboardSearch();
        }
    },
    methods: {
        checkUserAuthentication() {
            return localStorage.getItem('user-token') !== null;
        },
        async sponsorDashboardSearch(){
             try{
                const apiURL="http://127.0.0.1:5000/api/SponsorDashboardSearchAPI";
                const searchdata = {
                    "searchquery": this.searchquery,
                };
            
                let result = await axios.post(apiURL, searchdata);
                this.searchresult = result.data.data;
                console.log("dddddddddddddddddddddddddd",result)
             }
             catch(error){
                console.error('Axios error:', error.message);
    
             }
         },
         searchInfluencer() {
            this.$router.push({
                name: 'SponsorSearchResult',
                query: { q: this.searchquery }
            });
        },
         async fetchSponsorSearchResult() {
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
                    this.pendingAdRequests=this.adrequests.filter(adrequest => adrequest.status === 'Pending');
                    this.acceptedAdRequests=this.adrequests.filter(adrequest => adrequest.status === 'Accepted');
                } else {
                    console.error("Failed to fetch campaigns:", response.data.message);
                }
            } catch (error) {
                console.error("Error fetching campaigns:", error);
            }
        }
    }
}
</script>
<style scoped> 
.card {
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