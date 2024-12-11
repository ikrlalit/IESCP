<template>
    <div>
      <InfluencerHeaderComp :authenticated="isAuthenticated" />
      <div class="container text-center">
        <h2>Campaign</h2>
        <div v-if="campaignDetail">
        <p><strong>Id : </strong> {{ campaignDetail.id }}</p>
        <p><strong>UUID : </strong> {{ campaignDetail.uuid }}</p>
        <p><strong>Campaign Name : </strong> {{ campaignDetail.name }}</p>
        <p><strong>Description : </strong> {{ campaignDetail.description }}</p>
        <p><strong>Start Date : </strong> {{ campaignDetail.start_date }}</p>
        <p><strong>End Date : </strong> {{ campaignDetail.end_date }}</p>
        <p><strong>Budget : </strong> {{ campaignDetail.budget }}</p>
        <p><strong>Visibility : </strong> {{ campaignDetail.visibility }}</p>
        <p><strong>Primary goal : </strong> {{ campaignDetail.primary_goal }}</p>
        <p><strong>Secondary goal : </strong> {{ campaignDetail.secondary_goal }}</p>
        <p><strong>Created At : </strong> {{ campaignDetail.created_at }}</p>
        </div>
        <div v-else>
          <p>Loading data...</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import InfluencerHeaderComp from '@/components/InfluencerHeaderComp.vue';
  import axios from 'axios';
  
  export default {
    name: 'CampaignDetail',
    components: {
        InfluencerHeaderComp,
    },
    data() {
      return {
        isAuthenticated: this.checkUserAuthentication(),
        campaignDetail: null, 
        id:null,
      };
    },
    created() {
      this.getCampaignData();
    },
    methods: {
      checkUserAuthentication() {
        return localStorage.getItem('user-token') !== null;
      },
      async getCampaignData() {
        const id = this.$route.params.id;
        const apiURL = `http://127.0.0.1:5000/api/Campaign/${id}`;
    
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
    },
  };
  </script>
