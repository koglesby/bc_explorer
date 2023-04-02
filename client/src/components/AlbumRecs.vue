<template>
  <div class="container" v-if="this.releases.length > 0">
    <div class="row wrapper">
      <div class="followed-name col-12">
        <h2>Based on liking {{ faveSample.title }} by {{ faveSample.artist }}</h2>
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

    <div :id="[this.elId]">
      <div v-for="release, idx in releases" :key="idx">
        <ReleaseCard :key="release.release_title" :url="release.go_to_album" :artist="release.by_artist"
          :cover="release.album_art" :title="release.release_title" fromItemtype="FAVES">
        </ReleaseCard>
      </div>
    </div>
  </div>
</template>

<script>
import ReleaseCard from './ReleaseCard.vue';
import { tns } from "tiny-slider";
import { store } from './store';
import _ from 'lodash';


export default {
  data() {
    return {
      releases: [],
      elId: ''
    };
  },
  computed: {
    faveSample() {
      return _.sample(_.toArray(store.firebaseFavorites));
    },
  },
  async created() {
    this.elId = `elId-${Date.now()}` + `${Math.floor(Math.random() * 100)}`;
  },
  updated() {
    const slider = tns({
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
    return slider;
  },
  watch: {
    faveSample() {
      const base_url = process.env.NODE_ENV === "development" ? 'http://127.0.0.1:5000/' : '';
      const url = base_url + "/get_recommended/";
      fetch(url, {
        method: 'POST',
        headers: new Headers({
          'Content-Type': 'application/json',
        }),
        body: JSON.stringify({
          url: this.faveSample.url
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
