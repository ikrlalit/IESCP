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
                <h3 class="card-title pb-3" style="text-align: center;">Sponsor SignUp</h3>
                <div class="mb-3">
                    <label for="username" class="form-label">Username <span class="required">*</span></label>
                    <input type="text" class="form-control" v-model="username" id="username">
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
                    <label for="companyname" class="form-label">Company/Individual Name <span class="required">*</span></label>
                    <input type="text" class="form-control" id="companyname" v-model="companyname">
                </div>
                <div class="mb-3">
                    <label for="industry" class="form-label">Industry <span class="required">*</span></label>
                    <input type="text" class="form-control" id="industry" v-model="industry">
                </div>
                <div class="mb-3">
                    <label for="budget" class="form-label">Budget <span class="required">*</span></label>
                    <input type="text" class="form-control" id="budget" v-model="budget">
                </div>
                <div class="mb-3">
                    <label for="contactemail" class="form-label">Contact Email <span class="required">*</span></label>
                    <input type="email" class="form-control" id="contactemail" v-model="contactemail">
                </div>
                <div class="mb-3">
                    <label for="websitelink" class="form-label">Website/Social Media Link</label>
                    <input type="text" class="form-control" id="websitelink" v-model="websitelink">
                </div>
                <div class="mb-3">
                    <input type="hidden" name="roles" value="sponsor">
                </div>
                <button class="btn btn-primary" @click="userSignUp">SignUp</button>
            </div>
            <router-link to="/user-login"> Already have an account? Login here.</router-link>
            <router-link to="/influencer-signup"> Click here to sign up.</router-link>
        </div>
    </div>  
</template>

<script>
import axios from 'axios';

export default {
    name: 'SponsorSignUp',
    data(){
        return{
            username:"",
            email:"",
            password:"",
            companyname:"",
            industry:"",
            budget:"",
            contactemail:"",
            websitelink:"",
            role:"sponsor",
            successMessage: "",
            errorMessage: ""
        }
    },
    methods:{
         async userSignUp(){
             try{
                const apiURL="http://127.0.0.1:5000/api/UserSignUp";
                const signupData = {
                    "username": this.username,
                    "email": this.email,
                    "password": this.password,
                    "companyname": this.companyname,
                    "industry": this.industry,
                    "budget": this.budget,
                    "contactemail": this.contactemail,
                    "websitelink": this.websitelink,
                    "role": this.role
                };
                console.log("signupData", signupData);
            
                let result = await axios.post(apiURL, signupData);
                this.successMessage = "SignUp success redirecting to login..";
                this.errorMessage = "";
                setTimeout(() => {
                    this.$router.push("/user-login");
                    console.log(result.data);
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

.required {
    color: red;
}
</style> 
