<template>
    <SponsorHeaderComp :authenticated="isAuthenticated" />

    <div class="container">
        <div class="input-group mb-3">
            <input type="text" class="form-control p-2" placeholder="find influencers ... " v-model="searchquery">
            <button class="btn btn-warning" type="submit" @click="searchInfluencer">Search</button>
        </div>
    </div>
    <div class="container">
        <h4>Recommended Influencers</h4><br>
        <div v-if="influencersdata.length > 0">
            <div class="row">
                <div v-for="(influencer, index) in influencersdata" :key="index" class="col-md-4 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <router-link :to="`/influencer-detail/${influencer.id}`" class="router-link-card">
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
import SponsorHeaderComp from '@/components/SponsorHeaderComp.vue';

export default {
    name: 'SponsorDashboard',
    components: {
        SponsorHeaderComp
    },
    data() {
        return {
            isAuthenticated: this.checkUserAuthentication(),
            searchquery: "",
            influencersdata: []
        }

    },
    async mounted() {
        this.RecomendedInfluencer();
    },
    methods: {
        checkUserAuthentication() {
            return localStorage.getItem('user-token') !== null;
        },
        async RecomendedInfluencer() {
            try {
                const apiURL = "http://127.0.0.1:5000/api/GetRecommendedInfluencers";
                const token = localStorage.getItem('user-token');
                let result = await axios.get(apiURL, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                this.influencersdata = result.data.data;
            }
            catch (error) {
                console.error('Axios error:', error.message);

            }
        },
        searchInfluencer() {
            this.$router.push({
                name: 'SponsorSearchResult',
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
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
</style>