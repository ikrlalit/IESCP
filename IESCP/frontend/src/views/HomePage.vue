<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo03"
                aria-controls="navbarTogglerDemo03" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <router-link class="navbar-brand mx-3" to="/">IESCP</router-link>
        </div>
    </nav>
    <div class="home-container d-flex justify-content-center align-items-center min-vh-100" >
        <div class="card text-white p-5"
            style="text-align: center; width: 600px; background: rgba(0, 0, 0, 0.8); box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); border-radius: 15px;">
            <div class="card-body">
                <p class="card-text" style="font-size: 1.5rem;">Welcome to</p>
                <p class="large-text" style="font-size: 2.5rem; font-weight: bold;">IESCP</p>
                <p class="card-text" style="font-size: 1.2rem;">Influencer Engagement and Sponsor Cooperation Platform
                </p>
                <a href="#" class="btn btn-primary py-2 px-4 mt-3" @click="login">Login</a>
                <a href="#" class="btn btn-primary py-2 px-4 mt-3 mx-2" @click="signup">SignUp</a>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "HomePage",
    methods: {
        login() {
            this.$router.push({ name: "UserLogin" });
        },
        signup() {
            this.$router.push({ name: "InfluencerSignUp" });
        }
    }
}
</script>

<style>
body,
html {
    margin: 0;
    padding: 0;
    height: 100%;
    background: linear-gradient(to right, #141E30, #243B55);
    color: #fff;
    font-family: 'Arial', sans-serif;
}

.navbar {
    background-color: #141E30 !important;
}

.home-container {
    background-color: transparent;
    height: 100vh; /* Full viewport height */
    width: 100vw;
}

.card {
    background: rgba(0, 0, 0, 0.8);
    border: none;
}

.large-text {
    color: #ffffff;
}

.btn-primary {
    background-color: #007bff;
    border: none;
    transition: background-color 0.3s ease;
}

.btn-primary:hover {
    background-color: #0056b3;
}
</style>