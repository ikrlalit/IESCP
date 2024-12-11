<template>
    <div>
        <SponsorHeaderComp :authenticated="isAuthenticated" />
        <div class="container mt-4">
            <div class="card bg-dark text-white p-5" style="width: 40rem; margin-left: auto; margin-right: auto">
                <div class="card-body">
                    <div v-if="successMessage" class="alert alert-success" role="alert">
                        {{ successMessage }}
                    </div>
                    <div v-if="errorMessage" class="alert alert-danger" role="alert">
                        {{ errorMessage }}
                    </div>
                    <h3 class="card-title pb-3" style="text-align: center">
                        New AdRequest
                    </h3>
                    <div class="mb-3">
                        <label for="campaignId" class="form-label">Campaign Id</label>
                        <input type="number" style="background-color:darkgray;" class="form-control" id="campaignId"
                            v-model="campaignDetail.id" readonly />
                    </div>
                    <div class="mb-3">
                        <label for="campaignName" class="form-label">Campaign Name</label>
                        <input type="text" style="background-color:darkgray;" class="form-control" id="campaignName"
                            v-model="campaignDetail.name" readonly />
                    </div>
                    <div class="mb-3 position-relative">
                        <label for="influencerSearch" class="form-label">Search Influencer</label>
                        <input type="text" class="form-control" id="influencerSearch" v-model="searchTerm"
                            @input="searchInfluencers" @focus="showDropdown = true" @blur="hideDropdown"
                            autocomplete="off" />
                        <ul v-if="showDropdown && influencers.length" class="list-group position-absolute w-100"
                            style="max-height: 200px; overflow-y: auto; z-index: 1000;">
                            <li v-for="influencer in influencers" :key="influencer.id"
                                class="list-group-item list-group-item-action"
                                @mousedown="selectInfluencer(influencer)">
                                {{ influencer.name }}
                            </li>
                        </ul>
                    </div>
                    <div class="mb-3">
                        <label for="messages" class="form-label">Messages</label>
                        <textarea class="form-control" id="messages" v-model="adRequest.messages"></textarea>
                    </div>
                    <div class="mb-3">
                        <label for="requirements" class="form-label">Requirements</label>
                        <textarea class="form-control" id="requirements" v-model="adRequest.requirements"
                            required></textarea>
                    </div>
                    <div class="mb-3">
                        <label for="paymentAmount" class="form-label">Payment Amount</label>
                        <input type="number" class="form-control" id="paymentAmount" v-model="adRequest.payment_amount"
                            required />
                    </div>
                    <button class="btn btn-primary" @click="submitAdRequest">
                        Send Request
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import SponsorHeaderComp from "@/components/SponsorHeaderComp.vue";
import axios from "axios";

export default {
    name: "NewAdRequest",
    components: {
        SponsorHeaderComp,
    },
    data() {
        return {
            isAuthenticated: false,
            adRequest: {
                campaign_id: "",
                influencer_id: "",
                requirements: "",
                payment_amount: "",
            },
            messages: {
                campaign_id: "",
                influencer_id: "",
                messages: "",
                ad_id: ""
            },
            campaignDetail: {},
            id: null,
            searchTerm: "",
            influencers: [],
            showDropdown: false,
            errorMessage: '',
            successMessage: ''
        };
    },
    created() {
        this.isAuthenticated = this.checkUserAuthentication();
        this.getCampaignData();
    },
    methods: {
        checkUserAuthentication() {
            return localStorage.getItem("user-token") !== null;
        },
        async getCampaignData() {
            this.adRequest.campaign_id = this.$route.params.id;
            const apiURL = `http://127.0.0.1:5000/api/Campaign/${this.adRequest.campaign_id}`;

            try {
                const token = localStorage.getItem('user-token');
                const response = await axios.get(apiURL, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                if (response.data.status_code === 200) {
                    this.campaignDetail = response.data.data;
                } else {
                    console.error('Failed to fetch data:', response.data.message);
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        },
        async searchInfluencers() {
            const apiURL = "http://127.0.0.1:5000/api/GetInfluencersList";
            try {
                const token = localStorage.getItem('user-token');
                const response = await axios.post(apiURL, { SearchTerm: this.searchTerm }, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                if (response.data.status_code === 200) {
                    this.influencers = response.data.data;
                } else {
                    console.error('Failed to fetch influencers:', response.data.message);
                }
            } catch (error) {
                console.error('Error fetching influencers:', error);
            }
        },
        selectInfluencer(influencer) {
            this.adRequest.influencer_id = influencer.id;
            this.searchTerm = influencer.name;
            this.showDropdown = false;
        },
        hideDropdown() {
            setTimeout(() => {
                this.showDropdown = false;
            }, 500);
        },
        async submitAdRequest() {
            try {
                const token = localStorage.getItem('user-token');
                const apiURL = "http://127.0.0.1:5000/api/AdRequest";
                const response = await axios.post(apiURL, this.adRequest, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });

                if (response.data.status_code === 200 && response.data.message === 'Adrequest created successfully') {
                    this.messages = {
                        campaign_id: this.adRequest.campaign_id,
                        influencer_id: this.adRequest.influencer_id,
                        messages: this.adRequest.messages,
                        ad_id: response.data.data.id,
                    };

                    const apiURL1 = "http://127.0.0.1:5000/api/AddNewMessage";
                    const response1 = await axios.post(apiURL1, this.messages, {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    });
                    console.log(response1)
                    this.successMessage = 'Adrequest successfull!';
                    this.errorMessage = '';
                    setTimeout(() => {
                        this.$router.push("/sponsor-adrequest-list");
                    }, 2000);
                } else {
                    this.errorMessage = response.data.message || 'An error occurred while creating adrequest.';
                    this.successMessage = '';
                }
            } catch (error) {
                this.errorMessage = error.response?.data?.message || 'An error occurred while creating adrequest.';
                this.successMessage = '';
            }
        },
    },
};
</script>
