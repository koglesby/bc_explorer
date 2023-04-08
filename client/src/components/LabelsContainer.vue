<template>
  <div class="h-screen p-2 rounded">
    <div>
      <ReleaseSlider :page="currentPage" v-if="!!faves" :faveData="faves" itemtype="FAVES">
      </ReleaseSlider>
    </div>
    <div>
      <ReleaseSlider :page="currentPage" v-if="!!sampleForRec" :sampleForRec="sampleForRec" itemtype="RECS">
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
      componentKey: 0,
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
  watch: {
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
  components: { ReleaseSlider }
}
</script>

<style>
.pagination_nav_bar {
  justify-content: center;
}
</style>
