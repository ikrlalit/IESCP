<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo03"
                aria-controls="navbarTogglerDemo03" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <router-link class="navbar-brand" to="/">IESCP</router-link>
        </div>
    </nav>
    <div class="container py-5">
        <div class="card bg-dark text-white mx-auto p-5" style="width: 30rem;">
            <div class="card-body">
                <div v-if="successMessage" class="alert alert-success" role="alert">
                    {{ successMessage }}
                </div>
                <div v-if="errorMessage" class="alert alert-danger" role="alert">
                    {{ errorMessage }}
                </div>
                <h3 class="card-title pb-3" style="text-align: center;">Login</h3>
                <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input type="" class="form-control" v-model="email" required>
                </div>
                <div class="mb-3">
                    <label for="inputPassword" class="form-label">Password</label>
                    <input type="password" class="form-control" v-model="password" required>
                </div>
                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" id="rememberMe" name="remember_me">
                    <label class="form-check-label" for="rememberMe">Remember Me</label>
                </div>
                <button class="btn btn-primary" @click="login">Login</button>
            </div>
            <router-link to="/influencer-signup"> Don't have a account? Signup here.</router-link>
            <router-link to="/sponsor-signup"> Are you a Sponsor? Signup here.</router-link>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: 'UserLogin',
    data() {
        return {
            email: "",
            password: "",
            successMessage: "",
            errorMessage: ""
        }
    },
    methods: {
        async login() {
            const apiURL = "http://127.0.0.1:5000/api/UserLogin";
            const loginData = { "email": this.email, "password": this.password }
            try {
                let result = await axios.post(apiURL, loginData);
                if (result.data.status_code === 200) {
                    localStorage.setItem("user-token", result.data.data["access_token"])
                    if (result.data.data['role'] === 'influencer') {
                        this.successMessage = "Login Success. Redirecting..";
                        this.errorMessage = "";
                        console.log("111111111111111111111")
                        this.$router.push({ name: "InfluencerDashboard" });

                    }
                    if (result.data.data['role'] === 'admin') {
                        this.successMessage = "Login Success. Redirecting..";
                        this.errorMessage = "";

                        this.$router.push({ name: "AdminDashboard" })
                    }
                    console.log("eeeeeeeeeeee",result.data.data['role'],result.data.data['status'])
                    if (result.data.data['role'] === 'sponsor') {
                        if (result.data.data['status'] === 'approved') {
                            this.successMessage = "Login Success. Redirecting..";
                            this.errorMessage = "";
                            this.$router.push({ name: "SponsorDashboard" });
                        } else {
                            this.successMessage = "";
                            this.errorMessage = "Login Failed. Account Not Approved Yet.";
                        }
                    }
                    // {
                    //     this.successMessage = "Login Success. Redirecting..";
                    //     this.errorMessage = "";
                    //     this.$router.push({name:"SponsorDashboard"})
                    // } 
                    // if(result.data.data['role']=='sponsor' && result.data.data['status']=='pending' )
                    // {
                    //     this.successMessage = "";
                    //     this.errorMessage = "Login Failed. Account Not Apporved Yet.";
                    //     // this.$router.push({name:"SponsorDashboard"})
                    // }                          
                } else if (result.data.status_code === 400) {
                    this.successMessage = "";
                    this.errorMessage = "Authentication failed! Invalid password.";

                } else if (result.data.status_code === 404) {
                    this.successMessage = "";
                    this.errorMessage = "User doesn't exists. Please sign up.";
                } else {
                    this.successMessage = "";
                    this.errorMessage = "Something went wrong. Please try again.";
                }
            } catch (error) {
                if (error.response) {

                    this.successMessage = "";
                    this.errorMessage = "Something went wrong. Please try again.";
                }
                else {
                    this.successMessage = "";
                    this.errorMessage = "Something went wrong. Please try again.";
                }
            }
        }
    }
}
</script>
<style></style>
