<template>
    <div>
        <SponsorHeaderComp :authenticated="isAuthenticated" />
        <div class="container mt-4 py-5">
            <div class="card bg-dark text-white p-5" style="width: 40rem; margin-left: auto; margin-right: auto;">
                <div class="card-body">
                    <h3 class="card-title pb-3" style="text-align: center;">Update Campaign</h3>
                    <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
                    <div v-if="successMessage" class="alert alert-success mt-3">{{ successMessage }}</div>
                    <div class="mb-3">
                        <label for="name" class="form-label">Name</label>
                        <input type="text" class="form-control" id="name" v-model="campaign.name" required>
                    </div>
                    <div class="mb-3">
                        <label for="description" class="form-label">Description</label>
                        <textarea class="form-control" id="description" v-model="campaign.description"
                            required></textarea>
                    </div>
                    <div class="mb-3">
                        <label for="startDate" class="form-label">Start Date</label>
                        <input type="date" class="form-control" id="startDate" v-model="campaign.start_date" required>
                    </div>
                    <div class="mb-3">
                        <label for="endDate" class="form-label">End Date</label>
                        <input type="date" class="form-control" id="endDate" v-model="campaign.end_date" required>
                    </div>
                    <div class="mb-3">
                        <label for="budget" class="form-label">Budget</label>
                        <input type="number" class="form-control" id="budget" v-model="campaign.budget" required>
                    </div>
                    <div class="mb-3">
                        <label for="visibility" class="form-label">Visibility</label>
                        <select class="form-control" id="visibility" v-model="campaign.visibility" required>
                            <option value="public">Public</option>
                            <option value="private">Private</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="primary_goal" class="form-label">Primary Goals</label>
                        <textarea class="form-control" id="primary_goal" v-model="campaign.primary_goal"></textarea>
                    </div>
                    <div class="mb-3">
                        <label for="secondary_goal" class="form-label">Secondary Goals</label>
                        <textarea class="form-control" id="secondary_goal" v-model="campaign.secondary_goal"></textarea>
                    </div>

                    <button class="btn btn-primary" @click="updateCampaign">Update</button>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import SponsorHeaderComp from '@/components/SponsorHeaderComp.vue';
import axios from 'axios';

export default {
    name: 'UpdateCampaign',
    components: {
        SponsorHeaderComp
    },
    data() {
        return {
            isAuthenticated: this.checkUserAuthentication(),
            campaign: {
                id: null,
                name: '',
                description: '',
                start_date: '',
                end_date: '',
                budget: '',
                visibility: 'public',
                primary_goal: '',
                secondary_goal: ''
            },
            errorMessage: '',
            successMessage: ''
        };
    },
    mounted() {
        this.fetchCampaignData();
    },
    methods: {
        checkUserAuthentication() {
            return localStorage.getItem('user-token') !== null;
        },
        async fetchCampaignData() {
            try {
                const id = this.$route.params.id;
                const apiURL = `http://127.0.0.1:5000/api/Campaign/${id}`;
                const token = localStorage.getItem('user-token');
                const response = await axios.get(apiURL, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (response.data.status_code === 200) {
                    Object.assign(this.campaign, response.data.data);
                } else {
                    this.errorMessage = response.data.message || 'An error occurred while fetching the campaign.';
                }
            } catch (error) {
                this.errorMessage = error.response?.data?.message || 'An error occurred while fetching the campaign.';
            }
        },
        async updateCampaign() {
            try {
                const apiURL = `http://127.0.0.1:5000/api/Campaign/${this.campaign.id}`;
                const token = localStorage.getItem('user-token');
                const response = await axios.put(apiURL, this.campaign, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (response.data.status_code === 200) {
                    this.successMessage = 'Campaign updated successfully!';
                    this.errorMessage = '';
                    setTimeout(() => {
                    this.$router.push("/sponsor-campaign-list");
                }, 2000);
                } else {
                    this.errorMessage = response.data.message || 'An error occurred while updating the campaign.';
                    this.successMessage = '';
                }
            } catch (error) {
                this.errorMessage = error.response?.data?.message || 'An error occurred while updating the campaign.';
                this.successMessage = '';
            }
        }
    }
}
</script>
