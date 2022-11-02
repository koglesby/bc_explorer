<template>
  <div class="labels_container">
    <div v-for="(label_url, label_name) in store.labelData" v-bind:key="label_name">
      <LabelReleases :label_name="label_name" :label_url="label_url"></LabelReleases>
    </div>
  </div>
</template>
<script>
import LabelReleases from './LabelReleases.vue';
import { store } from './store';

export default {
  data() {
    return {
      store,
    };
  },
  async created() {
    this.store.getLabelData();
  },
  components: { LabelReleases }
}
</script>

<style>

</style>
