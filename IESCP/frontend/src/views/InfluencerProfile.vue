 <template>
    <div>
      <InfluencerHeaderComp :authenticated="isAuthenticated" />
      <div class="container text-center">
        <h2>Profile</h2>
        <div v-if="profileData">
          <p><strong>Username:</strong> {{ profileData.username }}</p>
          <p><strong>Name:</strong> {{ profileData.name }}</p>
          <p><strong>Email:</strong> {{ profileData.email }}</p>
          <p><strong>Role:</strong> {{ profileData.role }}</p>
          <p><strong>Category:</strong> {{ profileData.category }}</p>
          <p><strong>Niche:</strong> {{ profileData.niche }}</p>
          <p><strong>Instagram Follower:</strong> {{ profileData.instagram_follower }}</p>
          <p><strong>Instagram Link:</strong> <a :href="profileData.instagram_link" target="_blank">{{ profileData.instagram_link }}</a></p>
          <p><strong>Twitter Follower:</strong> {{ profileData.twitter_follower }}</p>
          <p><strong>Twitter Link:</strong> <a :href="profileData.twitter_link" target="_blank">{{ profileData.twitter_link }}</a></p>
          <p><strong>YouTube Follower:</strong> {{ profileData.youtube_follower }}</p>
          <p><strong>YouTube Link:</strong> <a :href="profileData.youtube_link" target="_blank">{{ profileData.youtube_link }}</a></p>
          <router-link :to="`/update-influencer-profile/${profileData.id}`" class="btn btn-warning mx-2">Edit</router-link>
        </div>
        <div v-else>
          <p>Loading profile data...</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import InfluencerHeaderComp from '@/components/InfluencerHeaderComp.vue';
  import axios from 'axios';
  
  export default {
    name: 'InfluencerProfile',
    components: {
      InfluencerHeaderComp,
    },
    data() {
      return {
        isAuthenticated: this.checkUserAuthentication(),
        profileData: null,
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
        const apiURL = 'http://127.0.0.1:5000/api/NewInfluencerProfile';
        try {
          const token = localStorage.getItem('user-token');
          const response = await axios.get(apiURL, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          if (response.data.status_code === 200) {
            this.profileData = response.data.data;
            console.log("Profile data:", response.data.data);
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
  
