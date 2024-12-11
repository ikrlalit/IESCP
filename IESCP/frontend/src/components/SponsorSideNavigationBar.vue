<template>
    <div class="card-body">
        <ul class="list-group">
            <div class="mb-3">
                <input type="text" class="form-control" placeholder="Search..." v-model="searchQuery" />
            </div>
        </ul>
    </div>
    <div class="card-body">
        <ul class="list-group">
            <router-link to="/sponsor-dashboard" class="list-group-item">Home</router-link>
            <router-link to="/new-adrequest" class="list-group-item">New AdRequest</router-link>
            <router-link to="/new-campaign" class="list-group-item">New Campaign</router-link>
            <router-link to="/sponsor-profile" class="list-group-item">My Profile</router-link>
        </ul>
    </div>
</template>

<script>
export default {
    name: 'SponsorSideNavigationBar',
}
</script>
<style></style>