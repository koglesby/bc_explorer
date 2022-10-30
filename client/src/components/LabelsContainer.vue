<template>
  <div class="labels_container">
    <div v-for="(label_url, label_name) in label_data" v-bind:key="label_name">
      <LabelReleases :label_name="label_name" :label_url="label_url"></LabelReleases>
    </div>
  </div>
</template>
<script>
import LabelReleases from './LabelReleases.vue';
export default {
  data() {
    return {
      label_data: {},
    };
  },
  async created() {
    const url = "http://127.0.0.1:5000/all_labels";
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok)
          throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.label_data = data;
      })
      .catch((error) => console.log(error));
  },
  components: { LabelReleases }
}
</script>

<style>

</style>
