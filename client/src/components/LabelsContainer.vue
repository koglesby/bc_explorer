<template>
  <div class="h-screen p-2 rounded">
    <div>
      <Favorites :page="currentPage"></Favorites>
    </div>
    <div>
      <AlbumRecs v-if="currentPage === 1 && !!sampleForRec" :sampleForRec="sampleForRec"></AlbumRecs>
    </div>
    <div v-for="(itemData) in orderedData" v-bind:key="itemData.url">
      <LabelReleases :label_name="itemData.name" :label_url="itemData.url" :itemtype="itemData.itemtype">
      </LabelReleases>
    </div>
    <b-pagination class="pagination_nav_bar" v-model="currentPage" :total-rows="rows" :per-page="perPage"
      aria-controls="labels_list"></b-pagination>
  </div>
</template>
<script>
import LabelReleases from './LabelReleases.vue';
import Favorites from './Favorites.vue'
import { store } from './store';
import { auth } from '../main';
import _ from 'lodash';
import AlbumRecs from './AlbumRecs.vue';
// import { useVirtualList } from '@vueuse/core'

export default {
  data() {
    return {
      // store,
      currentPage: 1,
      perPage: 5,
    };
  },
  computed: {
    orderedData() {
      // turns the firebaseLabelData into an array of objects, ordered aphabetically by the name property, excluding "The "
      const lodashOrdered = _.orderBy(store.firebaseLabelData, item => item.name.toLowerCase().replace(/^the /, ""));
      // return lodashOrdered;
      return lodashOrdered.slice((this.currentPage - 1) * this.perPage, this.currentPage * this.perPage);
    },
    rows() {
      return Object.keys(store.firebaseLabelData).length
    },
    // faves() {
    //   return _.toArray(store.firebaseFavorites);
    // },
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
    })

    // const { list, containerProps, wrapperProps } = useVirtualList(this.orderedData, {
    //   itemHeight: 96,
    // });

  },
  components: { LabelReleases, Favorites, AlbumRecs }
}
</script>

<style>
.pagination_nav_bar {
  justify-content: center;
}
</style>
