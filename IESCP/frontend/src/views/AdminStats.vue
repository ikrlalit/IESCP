<template>
    <AdminHeaderComp :authenticated="isAuthenticated"/>
    <div class="container">Admin Stats</div>
  </template>
  
  <script>
  import AdminHeaderComp from '@/components/AdminHeaderComp.vue';
  import axios from 'axios';
  
  export default {
    name: 'AdminStats',
    components: {
      AdminHeaderComp
    },
    data() {
      return {
        isAuthenticated: this.checkUserAuthentication(),
        dashboardData: {}
      };
    },
    methods: {
      checkUserAuthentication() {
        return localStorage.getItem('user-token') !== null;
      },
      async updateSponsorStatus(sponsorUserId, isApproved) {
        try {
          const apiURL = `http://127.0.0.1:5000/api/UpdateSponsorStatus`;
          await axios.put(apiURL, {
            sponsorUserId: sponsorUserId,
            isApproved: isApproved
          });
          this.fetchDashboardData(); 
        } catch (error) {
          console.error("Error updating sponsor status:", error);
        }
      },
      async fetchDashboardData() {
        try {
          const apiURL = "http://127.0.0.1:5000/api/GetAdminDashboardData";
          let result = await axios.get(apiURL);
          this.dashboardData = result.data;
          console.log(this.dashboardData)
        } catch (error) {
          console.error("Error fetching dashboard data:", error);
        }
      }
    },
    async mounted() {
      this.fetchDashboardData();
    }
  };
  </script>
  
  <style>
  </style>
  