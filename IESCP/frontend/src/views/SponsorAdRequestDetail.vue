<template>
    <div>
      <SponsorHeaderComp :authenticated="isAuthenticated" />
      <div class="container text-center">
        <h2>AdRequest Detail</h2>
        <div v-if="adrequestDetail">
        data found
        <p><strong>Id : </strong> {{ adrequestDetail.id }}</p>
        <p><strong>UUID : </strong> {{ adrequestDetail.uuid }}</p>
        <p><strong>Campaign Name : </strong> {{ adrequestDetail.campaign_name }}</p>
        <p><strong>Influencer Name : </strong> {{ adrequestDetail.Influencer_name }}</p>
        <p><strong>Message : </strong> {{ adrequestDetail.messages }}</p>
        <p><strong>Requirements : </strong> {{ adrequestDetail.requirements }}</p>
        <p><strong>Payment Amount : </strong> {{ adrequestDetail.payment_amount }}</p>
        <p><strong>Status : </strong> {{ adrequestDetail.status }}</p>
        <p><strong>Created At : </strong> {{ adrequestDetail.created_at }}</p>
        </div>
        <div v-else>
          <p>Loading data...</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import SponsorHeaderComp from '@/components/SponsorHeaderComp.vue';
  import axios from 'axios';
  
  export default {
    name: 'SponsorAdRequestDetail',
    components: {
      SponsorHeaderComp,
    },
    data() {
      return {
        isAuthenticated: this.checkUserAuthentication(),
        adrequestDetail: null, 
        id:null,
      };
    },
    created() {
      this.getAdreqData();
    },
    methods: {
      checkUserAuthentication() {
        return localStorage.getItem('user-token') !== null;
      },
      async getAdreqData() {
        const id = this.$route.params.id;
        const apiURL = `http://127.0.0.1:5000/api/AdRequest/${id}`;
    
        try {
          const token = localStorage.getItem('user-token');
          const response = await axios.get(apiURL, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          if (response.data.status_code === 200) {
            this.adrequestDetail = response.data.data;
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
  
  