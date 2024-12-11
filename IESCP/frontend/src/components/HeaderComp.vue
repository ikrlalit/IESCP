<template>
    <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
        <router-link class="navbar-brand" to="/">IESCP</router-link>
        <router-link v-if="authenticated" to="/user-login"  @click="logout" class="logout-link">Logout</router-link>
    </div>
    </nav>
  </header>
</template>

<script>
export default{
    name:'HeaderComp',
    props:{
        authenticated:Boolean
    },
    methods:{
        logout(){
        
            localStorage.removeItem('user-token');
        }
    }
}

</script>
<style>
.logout-link {
  color: white;
  text-decoration: none; 
  /* Remove underline */

  .navbar {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.logout-link {
  cursor: pointer;
}
}
</style>