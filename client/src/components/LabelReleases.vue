<template>
  <div class="container">
    <div class="wrapper">
      <div class="followed-name">
        <a :href="label_url">
          <h2>{{ this.label_name }}</h2>
        </a>
        <span>
          <h6>{{ this.itemtype }}</h6>
        </span>
      </div>
      <b-button class="unfollow" variant="secondary" @click="delButton">Unfollow</b-button>
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
        <ReleaseCard :key="release.album_name" :url="release.album_url" :artist="release.artist_name"
          :cover="release.cover_img_url" :title="release.album_name">
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
  props: ['label_name', 'label_url', 'itemtype'],
  data() {
    return {
      releases: [],
      elId: '',
    };
  },
  async created() {
    this.elId = `elId-${Date.now()}`;

    const url = 'http://127.0.0.1:5000/get_releases/';
    fetch(url, {
      method: 'POST',
      headers: new Headers({
        'Content-Type': 'application/json',
      }),
      body: JSON.stringify({
        url: this.label_url
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
  updated() {
    tns({
      container: `#${this.elId}`,
      items: 4,
      gutter: 30,
      slideBy: 1,
      controlsPosition: 'bottom',
      navPosition: 'bottom',
      mouseDrag: true,
      autoplay: true,
      autoplayButtonOutput: false,
      controlsContainer: `#custom-control-${this.elId}`,
      responsive: {
        0: {
          items: 2,
          nav: false,
        },
        768: {
          items: 3,
          nav: true,
        },
        1440: {
          items: 4,
        },
      },
    });
  },
  methods: {
    delButton() {
      store.deleteLabel(this.label_url);
    }
  },
  components: { ReleaseCard },
};
</script>

<style>
.container {
  position: relative;
  margin-top: 3%;
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
