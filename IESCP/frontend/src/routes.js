import { createRouter, createWebHistory } from 'vue-router'
import UserLogin from './views/UserLogin.vue';
import HomePage from './views/HomePage.vue';
import AdminDashboard from './views/AdminDashboard.vue';
import SponsorDashboard from './views/SponsorDashboard.vue';
import SponsorSignUp from './views/SponsorSignUp.vue';
import InfluencerDashboard from './views/InfluencerDashboard.vue';
import InfluencerSignUp from './views/InfluencerSignUp.vue';
import AdminSignUp from './views/AdminSignUp.vue';
import NewAdRequest from './views/NewAdRequest.vue';
import NewCampaign from './views/NewCampaign.vue';
import SponsorProfile from './views/SponsorProfile.vue';
import AdminStats from './views/AdminStats.vue';
import InfluencerProfile from './views/InfluencerProfile.vue';
import InfluencerStats from './views/InfluencerStats.vue';
import SponsorCampaignList from './views/SponsorCampaignList.vue';
import UpdateCampaign from './views/UpdateCampaign.vue';
import UpdateSponsorProfile from './views/UpdateSponsorProfile.vue';
import SponsorCampaignDetail from './views/SponsorCampaignDetail.vue';
import SponsorAdRequestList from './views/SponsorAdRequestList.vue';
import SponsorAdRequestDetail from './views/SponsorAdRequestDetail.vue';
import InfluencerDashboardSearchResult from './views/InfluencerDashboardSearchResult.vue';
import SponsorSearchResult from './views/SponsorSearchResult.vue';
import InfluencerAdrequest from './views/InfluencerAdrequest.vue';
import UpdateAdRequest from './views/UpdateAdRequest.vue';
import MessagesComp from './views/MessagesComp.vue';
import MessageCompSponsor from './views/MessageCompSponsor.vue';
import InfluencerDetail from './views/InfluencerDetail.vue';
import UpdateInfluencerProfile from './views/UpdateInfluencerProfile.vue';
import CampaignDetail from './views/CampaignDetail.vue';

const routes=[{
    name:'HomePage',
    component:HomePage,
    path:'/'
},
    
{
    name:'InfluencerSignUp',
    component:InfluencerSignUp,
    path:'/influencer-signup'
    
},  
{
    name:'AdminSignUp',
    component:AdminSignUp,
    path:'/admin-signup'
},  

{
    name:'UserLogin',
    component:UserLogin,
    path:'/user-login'
},
{
    name:'SponsorSignUp',
    component:SponsorSignUp,
    path:'/sponsor-signup'
},  

{
    name:'SponsorDashboard',
    component:SponsorDashboard,
    path:'/sponsor-dashboard'
},
{
    name:'InfluencerDashboard',
    component:InfluencerDashboard,
    path:'/influencer-dashboard'
},
{
    name:'AdminDashboard',
    component:AdminDashboard,
    path:'/admin-dashboard'
},
{
    name: 'NewAdRequest',
    component: NewAdRequest,
    path: '/new-adrequest/:id'
},
{
    name: 'NewCampaign',
    component: NewCampaign,
    path: '/new-campaign'
},
{
    name: 'SponsorProfile',
    component: SponsorProfile,
    path: '/sponsor-profile'
},
{
    name: 'AdminStats',
    component: AdminStats,
    path: '/admin-stats'
},
{
    name: 'InfluencerProfile',
    component: InfluencerProfile,
    path: '/influencer-profile'
},
{
    name: 'InfluencerStats',
    component: InfluencerStats,
    path: '/influencer-stats'
},
{
    name: 'SponsorCampaignList',
    component: SponsorCampaignList,
    path: '/Sponsor-Campaign-list'
},
{   name:'UpdateCampaign',
    component: UpdateCampaign,
    path: '/update-campaign/:id' 
},
{   name:'UpdateSponsorProfile',
    component: UpdateSponsorProfile,
    path: '/update-sponsor-profile/:id' 
},
{   name:'UpdateInfluencerProfile',
    component: UpdateInfluencerProfile,
    path: '/update-influencer-profile/:id' 
},
{
    name: 'InfluencerDetail',
    component: InfluencerDetail,
    path: '/influencer-detail/:id'
},
{   name:'SponsorCampaignDetail',
    component: SponsorCampaignDetail,
    path: '/sponsor-campaign-detail/:id' 
},
{   name:'CampaignDetail',
    component: CampaignDetail,
    path: '/campaign-detail/:id' 
},
{   name:'SponsorAdRequestList',
    component: SponsorAdRequestList,
    path: '/sponsor-adrequest-list' 
},
{   name:'SponsorAdRequestDetail',
    component: SponsorAdRequestDetail,
    path: '/adrequest-detail/:id' 
},
{   name:'InfluencerDashboardSearchResult',
    component: InfluencerDashboardSearchResult,
    path: '/search-results' 
},
{   name:'SponsorSearchResult',
    component: SponsorSearchResult,
    path: '/inf-search-results' 
},
{   name:'InfluencerAdRequest',
    component: InfluencerAdrequest,
    path: '/influencer-adrequests' 
},{
    name: 'UpdateAdRequest',
    component: UpdateAdRequest,
    path: '/update-adrequest/:id'
},
{
    name: 'MessagesComp',
    component: MessagesComp,
    path: '/chat'
},
{
    name: 'MessageCompSponsor',
    component: MessageCompSponsor,
    path: '/chat-sponsor'
},
]

const router= createRouter({
    history: createWebHistory(),
    routes
})
export default router