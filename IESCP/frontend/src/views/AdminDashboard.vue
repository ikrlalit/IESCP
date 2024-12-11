<!-- <template>
  <AdminHeaderComp :authenticated="isAuthenticated"/>
  <div class="container">
  <div class="row">
    <div class="col-md-6" style="text-align: center;">
      <div class="container" v-if="dashboardData">
        <h3>Overview</h3>
        <p>Total Campaigns: {{ dashboardData.total_campaign }}</p>
        <p>Total AdRequest: {{ dashboardData.total_adrequest }}</p>
        <p>Total Sponsors: {{ dashboardData.total_sponsors }}</p>
        <p>Total Influencers: {{ dashboardData.total_influencers }}</p>
      </div>
    </div>
    <div class="col-md-6" style="text-align: center;">
      <h3>Pending Approvals</h3>
      <div class="container" v-for="sponsor in dashboardData.pending_sponsor_accounts" :key="sponsor.id">
        <p>{{ sponsor.username }}</p>
        <p>{{ sponsor.email }}</p>
        <button @click="updateSponsorStatus(sponsor.id, 1)">Approve</button>
        <button @click="updateSponsorStatus(sponsor.id, 0)">Reject</button>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import AdminHeaderComp from '@/components/AdminHeaderComp.vue';
import axios from 'axios';

export default {
  name: 'AdminDashboard',
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
          isApproved: isApproved,
          exportStatus: ""
        });
        this.fetchDashboardData(); 
      } catch (error) {
        console.error("Error updating sponsor status:", error);
      }
    },
    async exportCSV() {
      try {
        this.exportStatus = "Starting export...";
        
        const startResponse = await axios.get('/start-csv-export');
        const taskId = startResponse.data.task_id;

        this.exportStatus = "Export in progress...";
        let isReady = false;


        while (!isReady) {
          await new Promise((resolve) => setTimeout(resolve, 2000));

          const resultResponse = await axios.get(`/get-csv-file/${taskId}`, {
            responseType: 'blob'
          });

          if (resultResponse.status === 200) {
            const url = window.URL.createObjectURL(new Blob([resultResponse.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'exported_file.csv');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            this.exportStatus = "Download complete!";
            isReady = true;
          } else if (resultResponse.status === 405) {
            this.exportStatus = "Still processing...";
          }
        }
      } catch (error) {
        console.error("Error exporting CSV:", error);
        this.exportStatus = "Error during export.";
      }
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
</style> -->
<template>
  <AdminHeaderComp :authenticated="isAuthenticated" />
  <div class="container">
    <div class="row">
      <div class="col-md-6" style="text-align: center;">
        <div class="container" v-if="dashboardData">
          <h3>Overview</h3>
          <p>Total Campaigns: {{ dashboardData.total_campaign }}</p>
          <p>Total AdRequest: {{ dashboardData.total_adrequest }}</p>
          <p>Total Sponsors: {{ dashboardData.total_sponsors }}</p>
          <p>Total Influencers: {{ dashboardData.total_influencers }}</p>
          <button @click="exportCSV">Export Campaign List CSV</button>
          <p v-if="exportStatus">{{ exportStatus }}</p>
        </div>
      </div>
      <div class="col-md-6" style="text-align: center;">
        <h3>Pending Approvals</h3>
        <div class="container" v-for="sponsor in dashboardData.pending_sponsor_accounts" :key="sponsor.id">
          <p>{{ sponsor.username }}</p>
          <p>{{ sponsor.email }}</p>
          <button @click="updateSponsorStatus(sponsor.id, 1)">Approve</button>
          <button @click="updateSponsorStatus(sponsor.id, 0)">Reject</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AdminHeaderComp from '@/components/AdminHeaderComp.vue';
import axios from 'axios';

export default {
  name: 'AdminDashboard',
  components: {
    AdminHeaderComp
  },
  data() {
    return {
      isAuthenticated: this.checkUserAuthentication(),
      dashboardData: {},
      exportStatus: ""
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
        const result = await axios.get(apiURL);
        this.dashboardData = result.data;
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      }
    },
    async exportCSV() {
      try {
        this.exportStatus = "Starting export...";
        const startResponse = await axios.get('http://127.0.0.1:5000/start-csv-export');
        const taskId = startResponse.data.task_id;

        this.exportStatus = "Export in progress...";
        let isReady = false;

        while (!isReady) {
          await new Promise((resolve) => setTimeout(resolve, 2000)); 

          const resultResponse = await axios.get(`http://127.0.0.1:5000/get-csv-file/${taskId}`, {
            responseType: 'blob'
          });

          if (resultResponse.status === 200) {
            const url = window.URL.createObjectURL(new Blob([resultResponse.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'exported_file.csv');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            this.exportStatus = "Download complete!";
            isReady = true;
          } else if (resultResponse.status === 405) {
            this.exportStatus = "Still processing...";
          }
        }
      } catch (error) {
        console.error("Error exporting CSV:", error);
        this.exportStatus = "Error during export.";
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
