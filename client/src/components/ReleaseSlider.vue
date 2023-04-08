<template>
  <div class="container" :key="componentKey"
    v-if="this.page === 1 || this.itemtype === 'ARTIST' || this.itemtype === 'LABEL'">
    <div class="row wrapper">
      <!-- Switch the header part of the component based on its type -->
      <!-- Favorites -->
      <div class="followed-name col-12" v-if="itemtype === 'FAVES' && this.releases.length > 0">
        <h2>Favorites</h2>
      </div>
      <!-- Recommendations -->
      <div class="followed-name col-12" v-if="this.itemtype === 'RECS'">
        <h2>Based on <i>{{ this.albumName }}</i> by {{ this.artistName }}</h2>
      </div>
      <!-- Artist or Label (an item the user is following) -->
      <Fragment v-if="itemtype === 'ARTIST' || itemtype === 'LABEL'">
        <div class="followed-name col-5">
          <div>
            <a :href="followUrl">
              <h2>{{ this.followName }}</h2>
            </a>
            <span>
              <h6>{{ this.itemtype }}</h6>
            </span>
          </div>
        </div>
        <div class="col-2 offset-5 float-right">
          <b-button class="unfollow btn-lg float-right" variant="secondary" @click="delButton">Unfollow</b-button>
        </div>
      </Fragment>
    </div>
    <ul class="control" :id="['custom-control-' + this.elId]">
      <li class="prev">
        <i class="fas fa-angle-left fa-2x"></i>
      </li>
      <li class="next">
        <i class="fas fa-angle-right fa-2x"></i>
      </li>
    </ul>
    <div :id="[this.elId]">
      <div v-for="release, idx in releases" :key="idx">
        <ReleaseCard :key="release.album_name" :url="release.album_url"
          :artist="itemtype === 'ARTIST' ? followName : release.artist_name" :cover="release.cover_img_url"
          :title="release.album_name" :fromItemtype="itemtype">
        </ReleaseCard>
      </div>
    </div>
  </div>
</template>

<script>
import ReleaseCard from './ReleaseCard.vue';
import { tns } from "../../node_modules/tiny-slider/src/tiny-slider";
import { store } from './store';
import { Fragment } from 'vue-fragment'

export default {
  props: ['followName', 'followUrl', 'itemtype', 'faveData', 'page', 'sampleForRec'],
  data() {
    return {
      releases: [],
      albumName: '',
      artistName: '',
      elId: `elId-${Date.now()}` + `${Math.floor(Math.random() * 100)}`,
      componentKey: Math.floor(Math.random() * 100) + Date.now()
    };
  },
  async created() {
    // Load the releases in the slider
    if (this.itemtype === 'LABEL' || this.itemtype === 'ARTIST') {
      this.getReleases(this.followUrl);
    }
    if (this.itemtype === 'RECS') {
      this.getRecommendations(this.sampleForRec.album_url);
    }
  },
  mounted() {
    // Check whether the label/artist was recently added, and scroll there if so
    if (
      store.newlyAddedUrl === this.followUrl && this.itemtype === 'ARTIST' ||
      store.newlyAddedUrl === this.followUrl && this.itemtype === 'LABEL'
    ) {
      const el = document.querySelector(`#${this.elId}`);
      const y = el.getBoundingClientRect().top + window.pageYOffset - 150;
      window.scrollTo({ top: y, behavior: 'smooth' });
    }
  },
  updated() {
    // Call tiny-slider for Favorites and Recommendations on page 1 only
    if (this.page === 1 || this.itemtype === 'ARTIST' || this.itemtype === 'LABEL') {
      tns({
        container: `#${this.elId}`,
        lazyload: true,
        items: 4,
        gutter: 10,
        slideBy: "page",
        controlsPosition: 'bottom',
        navPosition: 'bottom',
        mouseDrag: true,
        autoplay: false,
        autoplayButtonOutput: false,
        controlsContainer: `#custom-control-${this.elId}`,
        speed: 800,
        loop: false,
        nav: false,
        responsive: {
          0: {
            items: 2,
            nav: false,
          },
          768: {
            items: 3,
            nav: false,
          },
          1440: {
            items: 5,
            slideBy: 5,
            nav: false,
          },
        },
      });
    }
  },
  watch: {
    faveData() {
      // when the favorites data changes, re-render the component for it
      this.releases = this.faveData;
      this.componentKey = Math.floor(Math.random() * 100) + Date.now();
    },
  },
  methods: {
    delButton() {
      store.deleteLabel(this.followUrl);
    },
    getReleases(followedUrl) {
      const base_url = process.env.NODE_ENV === "development" ? 'http://127.0.0.1:5000/' : '';
      const url = base_url + "/get_releases/";
      fetch(url, {
        method: 'POST',
        headers: new Headers({
          'Content-Type': 'application/json',
        }),
        body: JSON.stringify({
          url: followedUrl
        })
      })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          this.releases = data.releases;
        })
        .catch((error) => console.log(error));
    },
    getRecommendations(sampleUrl) {
      const base_url = process.env.NODE_ENV === "development" ? 'http://127.0.0.1:5000/' : '';
      const url = base_url + "/get_recommended/";
      fetch(url, {
        method: 'POST',
        headers: new Headers({
          'Content-Type': 'application/json',
        }),
        body: JSON.stringify({
          url: sampleUrl
        })
      })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          this.releases = data.details;
          this.albumName = this.sampleForRec.album_name;
          this.artistName = this.sampleForRec.artist_name;
        })
        .catch((error) => console.log(error));
    }
  },
  components: { ReleaseCard, Fragment },
};
</script>

<style>
.container {
  position: relative;
  margin-top: 2%;
  margin-bottom: 2%;
  padding: 0 !important;
}

h1 {
  text-align: center;
  padding-bottom: 15px;
  font-family: Montserrat;
}

.control {
  list-style: none;
}

.control li {
  position: absolute;
  z-index: 99;
  top: 50%;
  transform: translateY(-50%);
  color: white;
  background: rgba(0, 0, 0, 0.5);
  padding: 12px 20px;
  border-radius: 50%;
  cursor: pointer;
}

.control li:hover {
  background: #000;
}

.control li.prev {
  left: 20px;
}

.control li.next {
  right: 20px;
}

.tns-nav {
  text-align: center;
  margin-top: 15px;
  margin-bottom: 15px;
}

.tns-nav button {
  height: 13px;
  width: 8px;
  background-color: #a5a5a5;
  border: none;
  margin-left: 7px;
  border-radius: 50%;
}

.tns-nav .tns-nav-active {
  background-color: black;
}

.followed-name {
  vertical-align: baseline;
  padding-right: 2em;
}
</style>
