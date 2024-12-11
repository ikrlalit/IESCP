<template>
    <InfluencerHeaderComp :authenticated="isAuthenticated" />

    <div class="container">
        <div class="input-group mb-3">
            <input type="text" class="form-control p-2" placeholder="Find Campaigns ... " v-model="searchquery">
            <button class="btn btn-warning" type="submit" @click="searchCampaign">Search</button>
        </div>
    </div>
    <div class = "container">
        <h4>Recommended Campaigns</h4><br>
        <div v-if="recommendedcomps.length > 0">
            <div class="row">
                <div v-for="(campaign, index) in recommendedcomps" :key="index" class="col-md-4 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <router-link :to="`/campaign-detail/${campaign.id}`" class="router-link-card">
                            <h5 class="card-title">{{ campaign.name }}</h5>
                            <div class="title-separator"></div>
                            <p class="card-text">{{ campaign.description }}</p>
                            <p class="card-text"><strong>Budget:</strong> {{ campaign.budget }}</p>
                            <p class="card-text"><strong>Start Date:</strong> {{ campaign.start_date}}</p>
                        </router-link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import InfluencerHeaderComp from '@/components/InfluencerHeaderComp.vue';
export default {
    name: 'InfluencerDashboard',
    components: {
        InfluencerHeaderComp
    },
    data() {
        return {
            isAuthenticated: this.checkUserAuthentication(),
            searchquery: "",
            searchresult: [],
            recommendedcomps: []
        }

    },
    async mounted() {
        this.RecommendedCampaigns();
    },
    methods: {
        checkUserAuthentication() {
            return localStorage.getItem('user-token') !== null;
        },
        async RecommendedCampaigns() {
            try {
                const apiURL = "http://127.0.0.1:5000/api/GetRecommendedCampaigns";
                const token = localStorage.getItem('user-token');
                let result = await axios.get(apiURL,{
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                this.recommendedcomps = result.data.data
                console.log(result.data.data ,"reeeeeeeeeeeeee")
            }
            catch (error) {
                console.error('Axios error:', error.message);

            }
        },
        searchCampaign() {
            this.$router.push({
                name: 'InfluencerDashboardSearchResult',
                query: { q: this.searchquery }
            });
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
.router-link-card {
    text-decoration: none;
    color: inherit;
    display: block;
    transition: transform 0.2s ease, box-shadow 0.2s ease;}
</style>