<template>
    <div>
      <SponsorHeaderComp :authenticated="isAuthenticated" />
      <div class="container text-center">
        <h2>Profile</h2>
        <div v-if="profileData">
          <p><strong>Username:</strong> {{ profileData.username }}</p>
          <p><strong>Email:</strong> {{ profileData.email }}</p>
          <p><strong>Role:</strong> {{ profileData.role }}</p>
          <p><strong>Account Status:</strong> {{ profileData.status }}</p>
          <p><strong>Name:</strong> {{ profileData.name }}</p>
          <p><strong>Industry:</strong> {{ profileData.industry }}</p>
          <p><strong>Budget:</strong> {{ profileData.budget }}</p>
          <p><strong>Contact Email:</strong> {{ profileData.contact_email }}</p>
          <p><strong>Website Link:</strong> {{ profileData.website_link }}</p>
          <p><strong>Account created at:</strong> {{ profileData.created_at }}</p>
          <router-link :to="`/update-sponsor-profile/${profileData.id}`" class="btn btn-warning mx-2">Edit</router-link>
        </div>
        <div v-else>
          <p>Loading profile data...</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import SponsorHeaderComp from '@/components/SponsorHeaderComp.vue';
  import axios from 'axios';
  
  export default {
    name: 'SponsorProfile',
    components: {
      SponsorHeaderComp,
    },
    data() {
      return {
        isAuthenticated: this.checkUserAuthentication(),
        profileData: null, // Initialize as null to show loading state
      };
    },
    created() {
      this.getProfileData();
    },
    methods: {
      checkUserAuthentication() {
        return localStorage.getItem('user-token') !== null;
      },
      async getProfileData() {
        const apiURL = 'http://127.0.0.1:5000/api/NewSponsorProfile';
        try {
          const token = localStorage.getItem('user-token');
          const response = await axios.get(apiURL, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          if (response.data.status_code === 200) {
            this.profileData = response.data.data;
            console.log("daataaaaaaaaa",response.data.data)
          } else {
            console.error('Failed to fetch profile data:', response.data.message);
          }
        } catch (error) {
          console.error('Error fetching profile data:', error);
        }
      },
    },
  };
  </script>
  
  