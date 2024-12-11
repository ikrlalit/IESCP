<template>
    <InfluencerHeaderComp :authenticated="isAuthenticated"/>
    
    <div class="container">
        <div class="input-group mb-3">
            <input type="text" class="form-control p-2" placeholder="Find Campaigns ... " v-model="searchquery">
            <button class="btn btn-warning" type="submit" @click="influencerDashboardSearch" >Search</button>
        </div>
    </div>
    <div class="container">
        <div v-if="searchresult.length > 0">
            <div class="row">
                <div v-for="(campaign, index) in searchresult" :key="index" class="col-md-4 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">{{ campaign.name }}</h5>
                            <div class="title-separator"></div>
                            <p class="card-text">{{ campaign.description }}</p>
                            <p class="card-text"><strong>Budget:</strong> {{ campaign.budget }}</p>
                            <p class="card-text"><strong>Start Date:</strong> {{ campaign.start_date}}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-else>
            No Result Found!
        </div>
    </div>
    
</template>

<script>
import axios from 'axios';
import InfluencerHeaderComp from '@/components/InfluencerHeaderComp.vue';
export default{
    name:'InfluencerDashboardSearchResult',
    components: {
      InfluencerHeaderComp
  },
  data(){
    return{
        isAuthenticated:this.checkUserAuthentication(),
        searchquery : "",
        searchresult:[]
    }

  },
  mounted() {
        this.searchquery = this.$route.query.q || "";
        if (this.searchquery) {
            this.influencerDashboardSearch();
        }
    },
  methods:{
    checkUserAuthentication(){
        return localStorage.getItem('user-token') !== null;
    },
    async influencerDashboardSearch(){
            if (!this.searchquery.trim()) {
                this.searchresult = []; 
                return;
            }
             try{
                const apiURL="http://127.0.0.1:5000/api/InfluencerDashboardSearchAPI";
                const searchdata = {
                    "searchquery": this.searchquery,
                };
                console.log("searchdata", searchdata);
            
                let result = await axios.post(apiURL, searchdata);
                this.searchresult = result.data.data;
                if (this.searchresult.length>0){
                    this.searchquery='' 
                }
                console.log("jdkkkkkkkkkkkkkkkkkkk",this.searchresult)
             }
             catch(error){
                console.error('Axios error:', error.message);
    
             }
         }
  }
}
</script>

<style scoped> 
.card {
    background-color: #333; 
    color: #fff;           
    padding: 20px;
    border-radius: 8px;  
    text-align: center;    
}
.title-separator {
    border-bottom: 2px solid #ccc; 
    margin: 10px 0;              
}

</style>