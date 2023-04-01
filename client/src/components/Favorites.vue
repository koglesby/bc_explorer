<template>
  <div class="container" :key="componentKey">
    <div class="row wrapper">
      <div class="followed-name col-5">
        <h2>Faves</h2>
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
      <div v-for="release, idx in orderedData" :key="idx">
        <ReleaseCard :key="release.title" :url="release.url" :artist="release.artist" :cover="release.cover"
          :title="release.title" fromItemtype="FAVES">
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
  // props: ['label_name', 'label_url', 'itemtype'],
  data() {
    return {
      releases: [],
      elId: '',
      componentKey: 0,

    };
  },

  computed: {
    orderedData() {
      // turns the firebaseFavorites into an array of objects, ordered aphabetically by the name property, excluding "The "
      // const lodashOrdered = _.orderBy(store.firebaseFavorites, item => item.title.toLowerCase().replace(/^the /, ""));
      // // return lodashOrdered;
      // return lodashOrdered;
      return _.toArray(store.firebaseFavorites);
    },
  },
  async created() {
    this.elId = `elId-${Date.now()}` + `${Math.floor(Math.random() * 100)}`;

    // console.log("FB faves", store.firebaseFavorites)

    // const lodashOrdered = _.orderBy(store.firebaseFavorites, item => item.artist.toLowerCase().replace(/^the /, ""));
    // // return lodashOrdered;

    // this.releases = lodashOrdered;

    // console.log("ordered??", lodashOrdered)


    // const faveObj = _.find(this.store.firebaseFavorites, { 'url': this.url });

    // const base_url = process.env.NODE_ENV === "development" ? 'http://127.0.0.1:5000/' : '';

    // const url = base_url + "/get_releases/";

    // fetch(url, {
    //   method: 'POST',
    //   headers: new Headers({
    //     'Content-Type': 'application/json',
    //   }),
    //   body: JSON.stringify({
    //     url: this.label_url
    //   })
    // })
    //   .then((response) => {
    //     if (!response.ok) throw Error(response.statusText);
    //     return response.json();
    //   })
    //   .then((data) => {
    //     this.releases = data.releases;
    //   })
    //   .catch((error) => console.log(error));
  },
  mounted() {
    // Check whether the label/artist was recently added, and scroll there if so
    // if (store.newlyAddedUrl === this.label_url) {
    // const el = document.querySelector(`#${this.elId}`);
    // const y = el.getBoundingClientRect().top + window.pageYOffset - 150;
    // window.scrollTo({ top: y, behavior: 'smooth' });

    // could put this function in a utils.js file if we need to reuse it
    //
    // function _scrollTo(selector, yOffset = 0){
    //   const el = document.querySelector(selector);
    //   const y = el.getBoundingClientRect().top + window.pageYOffset + yOffset;
    //   window.scrollTo({top: y, behavior: 'smooth'});
    // }
    // }
  },
  updated() {
    // console.log("faves updated", this.componentKey)

    // const dataLength = this.orderedData.length;

    // if (this.componentKey !== 2) {
    //   console.log("componentKeyyy", this.componentKey);
    //   this.componentKey++;
    // }

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
    orderedData() {
      this.componentKey += 1;
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
