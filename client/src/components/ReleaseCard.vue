<template>
  <div class="card bg-light mb-3" style="height:max-content; border: 0px">
    <a :href="url">
      <img class="img-fluid tns-lazy-img" :data-src="cover" alt="Cover image cap">
      <div class="card-body">
        <h5 class="card-title text-truncate" style="color: black">{{ artist }}</h5>
        <p class="card-text text-truncate" style="color: black">{{ title }}</p>
        <p class="card-text text-truncate" style="color: black">{{ releaseDate }}</p>
      </div>
    </a>
    <b-button @click="getReleaseDetails()">Get Details</b-button>
  </div>
</template>

<script>
import { store } from './store';
export default {
  props: ['url', 'artist', 'cover', 'title'],
  data() {
    return {
      store,
      releaseDate: ''
    };
  },
  methods: {
    getReleaseDetails() {
      const base_url = process.env.NODE_ENV === "development" ? 'http://127.0.0.1:5000/' : '';

      const url = base_url + "/get_release_details/";
      fetch(url, {
        method: 'POST',
        headers: new Headers({
          'Content-Type': 'application/json',
        }),
        body: JSON.stringify({
          url: this.url
        })
      })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          this.releaseDate = data.details
        })
        .catch((error) => console.log(error));

      this.store.addFavorite(this.url, this.artist, this.cover, this.title);

    }
  }
}
</script>

<style></style>
