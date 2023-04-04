<template>
  <div class="container" :key="componentKey"
    v-if="this.page === 1 || this.itemtype === 'ARTIST' || this.itemtype === 'LABEL'">
    <div class="row wrapper">
      <div class="followed-name" :class="itemtype === 'RECOMMEND' ? 'col-12' : 'col-5'">
        <div v-if="itemtype === 'FAVES'">
          <h2>Favorites</h2>
        </div>
        <div v-if="itemtype === 'ARTIST' || itemtype === 'LABEL'">
          <a :href="label_url">
            <h2>{{ this.label_name }}</h2>
          </a>
          <span>
            <h6>{{ this.itemtype }}</h6>
          </span>
        </div>
        <div v-if="itemtype === 'RECOMMEND'">
          <h2>Based on liking <i>{{ this.label_name }}</i> by {{ this.sample_artist }}</h2>
        </div>
      </div>
      <div class="col-2 offset-5 float-right" v-if="itemtype === 'ARTIST' || itemtype === 'LABEL'">
        <b-button class="unfollow btn-lg float-right" variant="secondary" @click="delButton">Unfollow</b-button>
      </div>
    </div>
    <ul class="control" :id="['custom-control-' + this.elId]">
      <li class="prev">
        <i class="fas fa-angle-left fa-2x"></i>
      </li>
      <li class="next">
        <i class="fas fa-angle-right fa-2x"></i>
      </li>
    </ul>
    <div :id="[this.elId]" v-if="itemtype === 'FAVES'">
      <div v-for="release, idx in faveData" :key="idx">
        <ReleaseCard :key="release.title" :url="release.url" :artist="release.artist" :cover="release.cover"
          :title="release.title" fromItemtype="FAVES">
        </ReleaseCard>
      </div>
    </div>
    <div :id="[this.elId]" v-if="itemtype !== 'FAVES'">
      <div v-for="release, idx in releases" :key="idx">
        <ReleaseCard v-if="itemtype === 'ARTIST' || itemtype === 'LABEL'" :key="release.album_name"
          :url="release.album_url" :artist="itemtype === 'ARTIST' ? label_name : release.artist_name"
          :cover="release.cover_img_url" :title="release.album_name" :fromItemtype="itemtype">
        </ReleaseCard>
        <ReleaseCard v-if="itemtype === 'RECOMMEND'" :key="release.release_title" :url="release.go_to_album"
          :artist="release.by_artist" :cover="release.album_art" :title="release.release_title" fromItemtype="RECOMMEND">
        </ReleaseCard>
      </div>
    </div>
  </div>
</template>

<script>
import ReleaseCard from './ReleaseCard.vue';
import { tns } from "../../node_modules/tiny-slider/src/tiny-slider";
import { store } from './store';

export default {
  props: ['label_name', 'label_url', 'itemtype', 'faveData', 'sample_artist', 'page'],
  data() {
    return {
      releases: [],
      elId: `elId-${Date.now()}` + `${Math.floor(Math.random() * 100)}`,
      componentKey: Math.floor(Math.random() * 100) + Date.now()
    };
  },
  async created() {
    if (this.itemtype === 'LABEL' || this.itemtype === 'ARTIST') {
      this.getReleases(this.label_url);
    }
    if (this.itemtype === 'RECOMMEND') {
      this.getRecommendations(this.label_url);
    }
  },
  mounted() {
    // Check whether the label/artist was recently added, and scroll there if so
    if (
      store.newlyAddedUrl === this.label_url && this.itemtype === 'ARTIST' ||
      store.newlyAddedUrl === this.label_url && this.itemtype === 'LABEL'
    ) {
      const el = document.querySelector(`#${this.elId}`);
      const y = el.getBoundingClientRect().top + window.pageYOffset - 150;
      window.scrollTo({ top: y, behavior: 'smooth' });
    }
  },
  updated() {
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
      this.componentKey = Math.floor(Math.random() * 100) + Date.now();
    }
  },
  methods: {
    delButton() {
      store.deleteLabel(this.label_url);
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
        })
        .catch((error) => console.log(error));
    }
  },
  components: { ReleaseCard },
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
