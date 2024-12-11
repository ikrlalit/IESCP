<template>
    <header>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container-fluid">
                <router-link class="navbar-brand" to="/">IESCP</router-link>
                <div class="navbar-nav ml-auto">
                    <router-link class="nav-link" to="/sponsor-dashboard" exact-active-class="active">Home</router-link>
                    <router-link class="nav-link" to="/sponsor-adrequest-list"
                        exact-active-class="active">AdRequests</router-link>
                    <router-link class="nav-link" to="/Sponsor-Campaign-list" exact-active-class="active">Campaigns</router-link>
                    <router-link class="nav-link" to="/sponsor-profile" exact-active-class="active">My
                        Profile</router-link>
                    <router-link v-if="authenticated" class="nav-link logout-link" to="/user-login" @click="logout"
                        exact-active-class="active">Logout</router-link>
                </div>
            </div>
        </nav>
    </header>
</template>

<script>
export default {
    name: "SponsorHeaderComp",
    props: {
        authenticated: {
            type: Boolean,
            required: true,
        },
    },
    methods: {
        logout() {
            localStorage.removeItem("user-token");
            // Optionally navigate to a different route after logout
            // this.$router.push('/user-login');
        },
    },
};
</script>

<style scoped>
.navbar {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.nav-link {
    color: white;
    margin-right: 15px;
    /* Increase spacing among menu items */
    transition: background-color 0.3s, color 0.3s;
    /* Smooth transition */
}

.nav-link:hover {
    background-color: rgba(255, 255, 255, 0.1);
    /* Hover background effect */
    color: #ffc107;
    /* Hover text color */
}

.active {
    font-weight: bold;
    /* Highlight current menu item */
    color: #ffc107 !important;
    /* Change text color of active item */
}

.logout-link {
    cursor: pointer;
    text-decoration: none;
    /* Remove underline */
}
</style>
