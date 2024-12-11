<template>
    <SponsorHeaderComp :authenticated="isAuthenticated" />
    <div class="container">
        <div class="row">
            <div class="card text-center">
                <div class="card-body">
                    <h5 class="card-title">New Campaign</h5>
                    <router-link :to="{ name: 'NewCampaign' }" class="btn btn-add mx-2">+</router-link>
                </div>
            </div>
            <div v-for="campaign in campaigns" :key="campaign.id" class="card text-center">
                <router-link :to="`/sponsor-campaign-detail/${campaign.id}`" class="router-link-card">
                    <div class="card-body">
                        <h5 class="card-title">{{ campaign.name }}</h5>
                        <div class="title-separator"></div>
                        <p class="card-text">{{ campaign.description }}</p>
                        <span>
                            <router-link :to="`/update-campaign/${campaign.id}`"
                                class="btn btn-update mx-2">Update</router-link>
                            <a href="#" @click.prevent="openModal(campaign.id)" class="btn btn-delete">Delete</a>
                        </span>
                    </div>
                </router-link>
            </div>
        </div>
        <div v-if="showModal" class="modal fade show" style="display: block;" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                    <div class="modal-body" style="background-color:darkslategray;">
                        <p style="color: azure;">Are you sure you want to delete this item?</p>
                        <button @click="deleteCampaign" class="btn btn-confirm mx-2">Yes</button>
                        <button @click="showModal = false" class="btn btn-cancel">No</button>
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
    name: 'SponsorCampaignList',
    components: {
        SponsorHeaderComp
    },
    data() {
        return {
            isAuthenticated: false,
            campaigns: [],
            showModal: false,
            itemIdToDelete: null
        };
    },
    methods: {
        checkUserAuthentication() {
            return localStorage.getItem('user-token') !== null;
        },
        openModal(id) {
            this.itemIdToDelete = id;
            this.showModal = true;
        },
        async fetchCampaignData() {
            const apiURL = "http://127.0.0.1:5000/api/GetCampaignList";
            const token = localStorage.getItem('user-token');
            try {
                let response = await axios.get(apiURL,{
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (response.data.status_code === 200) {
                    this.campaigns = response.data.data;
                } else {
                    console.error("Failed to fetch campaigns:", response.data.message);
                }
            } catch (error) {
                console.error("Error fetching campaigns:", error);
            }
        },
        async deleteCampaign() {
            const apiURL = `http://127.0.0.1:5000/api/Campaign/${this.itemIdToDelete}`;
            const token = localStorage.getItem('user-token');
            try {
                let response = await axios.delete(apiURL, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (response.data.status_code === 200) {
                    this.campaigns = this.campaigns.filter(campaign => campaign.id !== this.itemIdToDelete);
                    this.showModal = false;
                    this.itemIdToDelete = null;
                } else {
                    console.error("Failed to delete campaign:", response.data.message);
                }
            } catch (error) {
                console.error("Error deleting campaign:", error);
            }
        }
    },
    created() {
        this.isAuthenticated = this.checkUserAuthentication();
        this.fetchCampaignData();
    }
}
</script>

<style scoped>
/* .card-custom {
    width: 18rem;
    margin: 20px;
    color: #c59393;
} */
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
    /* background-color: #4caf50;
    color: #121212; */
    background-color: #333; 
    color: #fff;           
    padding: 20px;
    border-radius: 8px;  
    text-align: center;    
}

.btn-cancel {
    background-color: #f44336;
    color: #121212;
}
/* .card {
    background-color: #333; 
    color: #fff;           
    padding: 20px;
    border-radius: 8px;  
    text-align: center;    
} */
.title-separator {
    border-bottom: 2px solid #ccc; 
    margin: 10px 0;              
}
</style>
