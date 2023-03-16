<template>
  <div id="label_cont_id" class="h-screen p-2 rounded">
    <div v-for="(itemData) in orderedData" v-bind:key="itemData.url">
      <LabelReleases :label_name="itemData.name" :label_url="itemData.url" :itemtype="itemData.itemtype">
      </LabelReleases>
    </div>
    <b-pagination class="pagination_nav_bar" v-model="currentPage" :total-rows="rows" :per-page="perPage"
      aria-controls="labels_list"></b-pagination>
    <!-- <ul id="labels_list">
        <li v-for="(itemData) in orderedData" v-bind:key="itemData.url">
          <LabelReleases :label_name="itemData.name" :label_url="itemData.url" :itemtype="itemData.itemtype">
          </LabelReleases> 
        </li>
      </ul> -->
    <!-- <b-pagination-nav :link-gen="linkGen" :number-of-pages="numPages" v-model="currentPage"></b-pagination-nav> -->
  </div>
</template>
<script>
import LabelReleases from './LabelReleases.vue';
import { store } from './store';
import { auth } from '../main';
import _ from 'lodash';
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
  components: { LabelReleases }
}
</script>

<style>
.pagination_nav_bar {
  justify-content: center;
}
</style>
