<template>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div v-if="user.loggedIn">
                        <div class="card-header">Welcome, {{ user.data.displayName }}</div>
                        <div class="card-body">
                            <div class="alert alert-success" role="alert">
                                You are logged in!
                                <div class="my-4">
                                    <button @click.prevent="signOut" class="btn btn-primary">Log Out</button>
                                </div>
                            </div>
                            <RouterLink to="/">back to home</RouterLink>
                        </div>
                        <SearchUser></SearchUser>
                    </div>
                    <div v-if="user.loggedIn === false">
                        <div class="card-body">
                            <div class="alert alert-danger" role="alert">
                                You are not logged in!
                                <div class="my-4">
                                    <RouterLink to="/login"><button class="btn btn-primary">Log In</button></RouterLink>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script>
import { RouterLink } from "vue-router";
import { store } from "./store";
import SearchUser from './SearchUser.vue';

export default {
    data() {
        return {
            user: store.user,
        };
    },
    methods: {
        async signOut() {
            await store.logOut();
            this.$router.push("/");
        },
    },
    components: { RouterLink, SearchUser }
};
</script>