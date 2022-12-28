<template>
  <div class="labels_container" id="label_cont_id">
    <div v-for="(itemData) in orderedData" v-bind:key="itemData.url">
      <LabelReleases :label_name="itemData.name" :label_url="itemData.url" :itemtype="itemData.itemtype">
      </LabelReleases>
    </div>
  </div>
</template>
<script>
import LabelReleases from './LabelReleases.vue';
import { store } from './store';
import { auth } from '../main';
import _ from 'lodash';

export default {
  data() {
    return {
      // store,
    };
  },
  computed: {
    orderedData() {
      // turns the firebaseLabelData into an array of objects, ordered aphabetically by the name property, excluding "The "
      const lodashOrdered = _.orderBy(store.firebaseLabelData, item => item.name.toLowerCase().replace(/^the /, ""));
      return lodashOrdered;
    }
  },
  async created() {
    auth.onAuthStateChanged(user => {
      if (!!user) {
        store.getLabelData(user);
        store.fetchUser(user);
      }
    })

  },
  components: { LabelReleases }
}
</script>

<style>
.labels_container {
  margin-top: 10%;
}
</style>
