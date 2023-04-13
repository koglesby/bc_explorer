<template>
  <div class="h-screen p-2 rounded" v-if="this.loggedIn">
    <div v-if="faves.length !== 0 && currentPage === 1">
      <ReleaseSlider :page="currentPage" :faveData="faves" itemtype="FAVES">
      </ReleaseSlider>
    </div>

    <div v-if="recReleases.length > 0 && currentPage === 1">
      <ReleaseSlider :recReleases="this.recReleases" :page="currentPage" :sampleForRec="sampleForRec" itemtype="RECS">
      </ReleaseSlider>
    </div>

    <div v-for="(followData) in orderedData" v-bind:key="followData.url">
      <ReleaseSlider :followName="followData.follow_name" :followUrl="followData.url" :itemtype="followData.itemtype">
      </ReleaseSlider>
    </div>

    <b-pagination class="pagination_nav_bar" v-model="currentPage" :total-rows="rows" :per-page="perPage"
      aria-controls="labels_list"></b-pagination>
  </div>
</template>
<script>

import { store } from './store';
import { auth } from '../main';
import _ from 'lodash';
import ReleaseSlider from './ReleaseSlider.vue';
// import { useVirtualList } from '@vueuse/core'

export default {
  data() {
    return {
      currentPage: 1,
      perPage: 5,
      compKey: 0,
      loggedIn: null,
      displayFaves: false,
      recReleases: [],
    };
  },
  computed: {
    orderedData() {
      // turns the firebaseLabelData into an array of objects, ordered aphabetically by the follow_name property, excluding "The "
      const lodashOrdered = _.orderBy(store.firebaseLabelData, item => item.follow_name.toLowerCase().replace(/^the /, ""));

      return lodashOrdered.slice((this.currentPage - 1) * this.perPage, this.currentPage * this.perPage);
    },
    rows() {
      return Object.keys(store.firebaseLabelData).length
    },
    faves() {
      return _.reverse(_.toArray(store.firebaseFavorites));
    },
    sampleForRec() {
      return _.sample(_.toArray(store.firebaseFavorites));
    }
  },
  async created() {
    auth.onAuthStateChanged(user => {
      if (!!user) {
        store.getLabelData(user);
        store.fetchUser(user);
      }
      this.loggedIn = store.user.loggedIn;
    })
    this.loggedIn = store.user.loggedIn;

    // const { list, containerProps, wrapperProps } = useVirtualList(this.orderedData, {
    //   itemHeight: 96,
    // });
  },
  mounted() {

  },
  watch: {
    faves() {
      this.displayFaves = this.faves.length !== 0;
    },
    sampleForRec() {
      if (this.recReleases.length === 0) {
        this.getRecommendations(this.sampleForRec.album_url);
      }
    }
  },
  methods: {
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
          this.recReleases = data.details;
        })
        .catch((error) => console.log(error));
    }
  },
  components: { ReleaseSlider }
}
</script>

<style>
.pagination_nav_bar {
  justify-content: center;
}
</style>
