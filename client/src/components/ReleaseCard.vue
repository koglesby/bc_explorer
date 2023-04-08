<template>
  <div class="card bg-light mb-3" style="height:max-content; border: 0px">
    <a :href="url" target="_blank">
      <img class="img-fluid tns-lazy-img" style="width: 100%;" :data-src="cover" alt="Cover image cap">
      <div class="card-body">
        <h5 v-if="fromItemtype !== 'ARTIST'" class="card-title text-truncate" style="color: black">{{ artist }}</h5>
        <p class="card-text text-truncate" style="color: black">{{ title }}</p>
        <p v-if="openDetails && !loadingDetails" class="card-text text-truncate" style="color: black">{{ releaseDate }}
        </p>
      </div>
    </a>
    <div style="display: flex; justify-content: space-around">
      <i v-if="!openDetails && !loadingDetails" class="fas fa-caret-down info-icon" @click="getReleaseDetails()"></i>
      <i v-if="openDetails && !loadingDetails" class="fas fa-caret-up info-icon" @click="showLess()"></i>
      <i v-if="loadingDetails" class="fas fa-spinner fa-spin"></i>
      <i class="fas fa-thumbs-up info-icon" :class="{ thummy: isFavorite }" @click="faveToggle()"></i>
    </div>
  </div>
</template>

<script>
import { store } from './store';
import _ from 'lodash';

export default {
  props: ['url', 'artist', 'cover', 'title', 'fromItemtype'],
  data() {
    return {
      store,
      releaseDate: '',
      openDetails: false,
      loadingDetails: false
    };
  },
  computed: {
    isFavorite() {
      const faveObj = _.find(this.store.firebaseFavorites, { 'album_url': this.url });
      return !!faveObj;
    }
  },
  methods: {
    showLess() {
      this.openDetails = false;
    },
    getReleaseDetails() {
      if (this.releaseDate === '') {
        const base_url = process.env.NODE_ENV === "development" ? 'http://127.0.0.1:5000/' : '';
        this.loadingDetails = true;
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
            this.releaseDate = data.details;
            this.loadingDetails = false;
          })
          .catch((error) => console.log(error));
      }
      this.openDetails = true;
    },
    faveToggle() {
      if (this.isFavorite) {
        this.store.unFavorite(this.url);
      } else {
        this.store.addFavorite(this.url, this.artist, this.cover, this.title);
      }
    }
  }
}
</script>

<style>
.thummy {
  color: fuchsia !important;
}

.info-icon {
  cursor: pointer;
  color: #474747;
}

.info-icon:hover {
  transform: scale(1.1);
  color: black;
}
</style>
