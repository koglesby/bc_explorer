<template>
  <div class="labels_container">
    <div v-for="(itemData, itemId) in store.firebaseLabelData" v-bind:key="itemId">
      <LabelReleases :label_name="itemData.name" :label_url="itemData.url" :itemtype="itemData.itemtype">
      </LabelReleases>
    </div>
  </div>
</template>
<script>
import LabelReleases from './LabelReleases.vue';
import { store } from './store';
import { auth } from '../main';

export default {
  data() {
    return {
      store,
    };
  },
  async created() {
    auth.onAuthStateChanged(user => {
      if (!!user) {
        this.store.getLabelData(user);
        this.store.fetchUser(user);
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
