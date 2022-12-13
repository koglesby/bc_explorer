<template>
  <div class="container">
    <div class="row wrapper">
      <div class="followed-name col-5">
        <a :href="label_url">
          <h2>{{ this.label_name }}</h2>
        </a>
        <span>
          <h6>{{ this.itemtype }}</h6>
        </span>
      </div>
      <div class="col-2 offset-5 float-right">
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
  mounted() {
    // Check whether the label/artist was recently added, and scroll there if so
    if (store.newlyAddedUrl === this.label_url) {
      const el = document.querySelector(`#${this.elId}`);
      const y = el.getBoundingClientRect().top + window.pageYOffset - 150;
      window.scrollTo({ top: y, behavior: 'smooth' });

      // could put this function in a utils.js file if we need to reuse it
      //
      // function _scrollTo(selector, yOffset = 0){
      //   const el = document.querySelector(selector);
      //   const y = el.getBoundingClientRect().top + window.pageYOffset + yOffset;
      //   window.scrollTo({top: y, behavior: 'smooth'});
      // }
    }
  },
  updated() {
    tns({
      container: `#${this.elId}`,
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
