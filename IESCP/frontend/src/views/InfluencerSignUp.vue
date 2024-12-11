<!-- <template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo03" aria-controls="navbarTogglerDemo03" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <router-link class="navbar-brand" to="/">IESCP</router-link>
    </div>
   </nav>     
    <div class="content-container">
        <div class="card bg-dark text-white p-5" style="width: 40rem; margin-left: auto; margin-right: auto;">
        <div class="card-body">
            <div v-if="successMessage" class="alert alert-success" role="alert">
            {{ successMessage }}
            </div>
            <div v-if="errorMessage" class="alert alert-danger" role="alert">
            {{ errorMessage }}
            </div>
            <h3 class="card-title pb-3" style="text-align: center;">Influencer SignUp</h3>
                <div class="mb-3">
                    <label for="fName" class="form-label">Username</label>
                    <input type="text" class="form-control" v-model="username">
                </div>
                <div class="mb-3">
                    <label for="exampleInputEmail1" class="form-label">Email</label>
                    <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" v-model="email">
                </div>
                <div class="mb-3">
                    <label for="inputPassword" class="form-label">Password</label>
                    <input type="password" class="form-control" id="inputPassword" v-model="password">
                </div>
                <div class="mb-3">
                    <label for="influencername" class="form-label">Name</label>
                    <input type="text" class="form-control" id="influencername" v-model="influencername">
                </div>
                <div class="mb-3">
                    <label for="inputcategory" class="form-label">Category</label>
                    <input type="text" class="form-control" id="category" v-model="category">
                </div>
                <div class="mb-3">
                    <label for="inputniche" class="form-label">Niche</label>
                    <input type="text" class="form-control" id="niche" v-model="niche">
                </div>
                <div class="mb-3">
                    <label for="inputyoutube_follower" class="form-label">Youtube Subscribers</label>
                    <input type="text" class="form-control" id="youtube_follower" v-model="youtube_follower">
                </div>
                <div class="mb-3">
                    <label for="inputyoutube_link" class="form-label">Youtube Channel Link</label>
                    <input type="text" class="form-control" id="youtube_link" v-model="youtube_link">
                </div>
                <div class="mb-3">
                    <label for="inputinstagram_follower" class="form-label">Instagram Followers</label>
                    <input type="text" class="form-control" id="instagram_follower" v-model="instagram_follower">
                </div>
                <div class="mb-3">
                    <label for="instagram_link" class="form-label">Instagram Profile Link</label>
                    <input type="text" class="form-control" id="instagram_link" v-model="instagram_link">
                </div>
                <div class="mb-3">
                    <label for="inputtwitter_follower" class="form-label">Twitter Followers</label>
                    <input type="text" class="form-control" id="twitter_follower" v-model="twitter_follower">
                </div>
                <div class="mb-3">
                    <label for="twitter_link" class="form-label">Twitter Profile Link</label>
                    <input type="text" class="form-control" id="twitter_link" v-model="twitter_link">
                </div>
                <div class="mb-3">
                    <input type="hidden" name="roles" value="Influencer">
                </div>
                <button class="btn btn-primary" @click="userSignUp">SignUp</button>
        </div>
        <router-link to="/user-login"> Already have an account? Login here.</router-link>
        <router-link to="/sponsor-signup"> Are you a Sponsor? Signup here.</router-link>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

    export default {
        name: 'InfluencerSignUp',
        data(){
            return{
                username:"",
                email:"",
                password:"",
                role:"user",
                successMessage: "",
                errorMessage: ""
            }
        },
        methods:{
             async userSignUp(){
             try{
                const apiURL="http://127.0.0.1:5000/api/UserSignUp";
                const signupData = {"username":this.username,
                                    "email":this.email,
                                    "password":this.password,
                                    "role":this.role}
                console.log("signupData",signupData)
            
                let result=await axios.post(apiURL,signupData);
                this.successMessage = "Success. Redirecting to login...";
                this.errorMessage = "";
                setTimeout(() => {
                    this.$router.push("/user-login");
                    console.log(result.data)
                }, 2000);

             }
             catch(error){
                console.error('Axios error:', error.message);
                this.errorMessage = "Failed, Please try again.";
                this.successMessage = "";

                setTimeout(() => {
                    this.errorMessage = "";
                    this.successMessage = "";
                }, 2500);
             }

             }
        }

    }
</script>
<style>
.content-container {
    height: 100vh;
    background-image: url("../assets/homepage.jpg");
    background-repeat: no-repeat;
    background-position: center center;
    background-size: cover;
    padding-bottom: 10%;
}
</style> -->


<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo03" aria-controls="navbarTogglerDemo03" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <router-link class="navbar-brand" to="/">IESCP</router-link>
        </div>
    </nav>     
    <div class="container py-5">
        <div class="card bg-dark text-white p-5" style="width: 40rem; margin-left: auto; margin-right: auto;">
            <div class="card-body">
                <div v-if="successMessage" class="alert alert-success" role="alert">
                    {{ successMessage }}
                </div>
                <div v-if="errorMessage" class="alert alert-danger" role="alert">
                    {{ errorMessage }}
                </div>
                <h3 class="card-title pb-3" style="text-align: center;">Influencer SignUp</h3>
                <div class="mb-3">
                    <label for="fName" class="form-label">Username <span class="required">*</span></label>
                    <input type="text" class="form-control" v-model="username">
                </div>
                <div class="mb-3">
                    <label for="exampleInputEmail1" class="form-label">Email <span class="required">*</span></label>
                    <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" v-model="email">
                </div>
                <div class="mb-3">
                    <label for="inputPassword" class="form-label">Password <span class="required">*</span></label>
                    <input type="password" class="form-control" id="inputPassword" v-model="password">
                </div>
                <div class="mb-3">
                    <label for="influencername" class="form-label">Name</label>
                    <input type="text" class="form-control" id="influencername" v-model="influencername">
                </div>
                <div class="mb-3">
                    <label for="inputcategory" class="form-label">Category</label>
                    <input type="text" class="form-control" id="category" v-model="category">
                </div>
                <div class="mb-3">
                    <label for="inputniche" class="form-label">Niche</label>
                    <input type="text" class="form-control" id="niche" v-model="niche">
                </div>
                <div class="mb-3">
                    <label for="inputyoutube_follower" class="form-label">Youtube Subscribers</label>
                    <input type="text" class="form-control" id="youtube_follower" v-model="youtube_follower">
                </div>
                <div class="mb-3">
                    <label for="inputyoutube_link" class="form-label">Youtube Channel Link</label>
                    <input type="text" class="form-control" id="youtube_link" v-model="youtube_link">
                </div>
                <div class="mb-3">
                    <label for="inputinstagram_follower" class="form-label">Instagram Followers</label>
                    <input type="text" class="form-control" id="instagram_follower" v-model="instagram_follower">
                </div>
                <div class="mb-3">
                    <label for="instagram_link" class="form-label">Instagram Profile Link</label>
                    <input type="text" class="form-control" id="instagram_link" v-model="instagram_link">
                </div>
                <div class="mb-3">
                    <label for="inputtwitter_follower" class="form-label">Twitter Followers</label>
                    <input type="text" class="form-control" id="twitter_follower" v-model="twitter_follower">
                </div>
                <div class="mb-3">
                    <label for="twitter_link" class="form-label">Twitter Profile Link</label>
                    <input type="text" class="form-control" id="twitter_link" v-model="twitter_link">
                </div>
                <div class="mb-3">
                    <input type="hidden" name="roles" value="Influencer">
                </div>
                <button class="btn btn-primary" @click="userSignUp">SignUp</button>
            </div>
            <router-link to="/user-login"> Already have an account? Login here.</router-link>
            <router-link to="/sponsor-signup"> Are you a Sponsor? Signup here.</router-link>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'InfluencerSignUp',
    data(){
        return {
            username: "",
            email: "",
            password: "",
            role: "influencer",
            influencername: "",
            category: "",
            niche: "",
            youtube_follower: "",
            youtube_link: "",
            instagram_follower: "",
            instagram_link: "",
            twitter_follower: "",
            twitter_link: "",
            successMessage: "",
            errorMessage: ""
        }
    },
    methods:{
        async userSignUp(){
            try {
                const apiURL = "http://127.0.0.1:5000/api/UserSignUp";
                const signupData = {
                    username: this.username,
                    email: this.email,
                    password: this.password,
                    role: this.role,
                    influencername: this.influencername,
                    category: this.category,
                    niche: this.niche,
                    youtube_follower: this.youtube_follower,
                    youtube_link: this.youtube_link,
                    instagram_follower: this.instagram_follower,
                    instagram_link: this.instagram_link,
                    twitter_follower: this.twitter_follower,
                    twitter_link: this.twitter_link
                };
                console.log("signupData", signupData);
                
                let result = await axios.post(apiURL, signupData);
                this.successMessage = "Success. Redirecting to login...";
                this.errorMessage = "";
                setTimeout(() => {
                    this.$router.push("/user-login");
                    console.log(result.data);
                }, 2000);
            } catch (error) {
                console.error('Axios error:', error.message);
                this.errorMessage = "Failed, Please try again.";
                this.successMessage = "";
                setTimeout(() => {
                    this.errorMessage = "";
                    this.successMessage = "";
                }, 2500);
            }
        }
    }
}
</script>

<style>
.required {
    color: red;
}
</style>
