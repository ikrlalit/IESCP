<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo03" aria-controls="navbarTogglerDemo03" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <router-link class="navbar-brand" to="/">IESCP</router-link>
    </div>
   </nav>     
    <div class="content-container">
        <div class="card bg-dark text-white p-5" style="width: 30rem; margin-left: auto; margin-right: auto;">
        <div class="card-body">
            <div v-if="successMessage" class="alert alert-success" role="alert">
            {{ successMessage }}
            </div>
            <div v-if="errorMessage" class="alert alert-danger" role="alert">
            {{ errorMessage }}
            </div>
            <h3 class="card-title pb-3" style="text-align: center;">Admin SignUp</h3>
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
        name: 'AdminSignUp',
        data(){
            return{
                username:"",
                email:"",
                password:"",
                role:"admin",
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
/* .content-container {
    height: 100vh;
    background-image: url("../assets/homepage.jpg");
    background-repeat: no-repeat;
    background-position: center center;
    background-size: cover;
    padding-bottom: 10%;
} */
</style>