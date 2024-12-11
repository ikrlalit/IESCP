<template>
    <div>
      <InfluencerHeaderComp :authenticated="isAuthenticated" />
      <div class="container py-5">
        <div class="card bg-dark text-white p-5" style="width: 40rem; margin-left: auto; margin-right: auto;">
          <div class="card-body">
            <div v-if="successMessage" class="alert alert-success" role="alert">
              {{ successMessage }}
            </div>
            <div v-if="errorMessage" class="alert alert-danger" role="alert">
              {{ errorMessage }}
            </div>
            <h3 class="card-title pb-3" style="text-align: center;">Update Influencer Profile</h3>
            <div class="mb-3">
              <label for="name" class="form-label">Name</label>
              <input type="text" class="form-control" id="name" v-model="name">
            </div>
            <div class="mb-3">
              <label for="category" class="form-label">Category</label>
              <input type="text" class="form-control" id="category" v-model="category">
            </div>
            <div class="mb-3">
              <label for="niche" class="form-label">Niche</label>
              <input type="text" class="form-control" id="niche" v-model="niche">
            </div>
            <div class="mb-3">
              <label for="instagram_link" class="form-label">Instagram Link</label>
              <input type="url" class="form-control" id="instagram_link" v-model="instagram_link">
            </div>
            <div class="mb-3">
              <label for="instagram_follower" class="form-label">Instagram Followers</label>
              <input type="text" class="form-control" id="instagram_follower" v-model="instagram_follower">
            </div>
            <div class="mb-3">
              <label for="twitter_link" class="form-label">Twitter Link</label>
              <input type="url" class="form-control" id="twitter_link" v-model="twitter_link">
            </div>
            <div class="mb-3">
              <label for="twitter_follower" class="form-label">Twitter Followers</label>
              <input type="text" class="form-control" id="twitter_follower" v-model="twitter_follower">
            </div>
            <div class="mb-3">
              <label for="youtube_link" class="form-label">YouTube Link</label>
              <input type="url" class="form-control" id="youtube_link" v-model="youtube_link">
            </div>
            <div class="mb-3">
              <label for="youtube_follower" class="form-label">YouTube Followers</label>
              <input type="text" class="form-control" id="youtube_follower" v-model="youtube_follower">
            </div>
            <button class="btn btn-warning" @click="updateInfluencerProfile">Update</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import InfluencerHeaderComp from '@/components/InfluencerHeaderComp.vue';
  
  export default {
    name: 'UpdateInfluencerProfile',
    components: {
      InfluencerHeaderComp
    },
    data() {
      return {
        isAuthenticated: this.checkUserAuthentication(),
        name: "",
        category: "",
        niche: "",
        instagram_link: "",
        instagram_follower: "",
        twitter_link: "",
        twitter_follower: "",
        youtube_link: "",
        youtube_follower: "",
        successMessage: "",
        errorMessage: ""
      };
    },
    mounted() {
      this.fetchProfileData();
    },
    methods: {
      checkUserAuthentication() {
        return localStorage.getItem('user-token') !== null;
      },
      async fetchProfileData() {
        try {
          const apiURL = "http://127.0.0.1:5000/api/NewInfluencerProfile";
          const token = localStorage.getItem('user-token');
          const response = await axios.get(apiURL, {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });
          if (response.data.status_code === 200) {
            const data = response.data.data;
            this.name = data.name;
            this.category = data.category;
            this.niche = data.niche;
            this.instagram_link = data.instagram_link;
            this.instagram_follower = data.instagram_follower;
            this.twitter_link = data.twitter_link;
            this.twitter_follower = data.twitter_follower;
            this.youtube_link = data.youtube_link;
            this.youtube_follower = data.youtube_follower;
          } else {
            this.errorMessage = response.data.message || 'An error occurred while fetching the data.';
          }
        } catch (error) {
          this.errorMessage = error.response?.data?.message || 'An error occurred while fetching the data.';
        }
      },
      async updateInfluencerProfile() {
        try {
          const infid = this.$route.params.id;
          const apiURL = `http://127.0.0.1:5000/api/NewInfluencerProfile/${infid}`;
          const token = localStorage.getItem('user-token');
          const profileUpdateData = {
            name: this.name,
            category: this.category,
            niche: this.niche,
            instagram_link: this.instagram_link,
            instagram_follower: this.instagram_follower,
            twitter_link: this.twitter_link,
            twitter_follower: this.twitter_follower,
            youtube_link: this.youtube_link,
            youtube_follower: this.youtube_follower
          };
  
          const result = await axios.put(apiURL, profileUpdateData, {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });
          console.log(result)
          this.successMessage = "Profile updated successfully.";
          this.errorMessage = "";
          setTimeout(() => {
            this.$router.push("/influencer-profile");
          }, 2000);
        } catch (error) {
          console.error('Axios error:', error.message);
          this.errorMessage = "Failed to update profile. Please try again.";
          this.successMessage = "";
  
          setTimeout(() => {
            this.errorMessage = "";
            this.successMessage = "";
          }, 2500);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .card {
    background-color: #333;
    color: #fff;
    padding: 20px;
    border-radius: 8px;
  }
  </style>