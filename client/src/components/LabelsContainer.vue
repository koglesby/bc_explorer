<template>
  <div id="label_cont_id" v-bind="containerProps" class="h-screen p-2 rounded" >
    <div v-bind="wrapperProps">
      <div v-for="(itemData) in orderedData" v-bind:key="itemData.url">
        <LabelReleases :label_name="itemData.name" :label_url="itemData.url" :itemtype="itemData.itemtype">
        </LabelReleases>
      </div>
      <!-- <div v-for="{ itemData } in list" :key="itemData.url" class="rounded-lg h-[80px] mb-4">
        <LabelReleases :label_name="itemData.name" :label_url="itemData.url" :itemtype="itemData.itemtype">
        </LabelReleases>
      </div> -->
    </div>
  </div>
</template>
<script>
import LabelReleases from './LabelReleases.vue';
import { store } from './store';
import { auth } from '../main';
import _ from 'lodash';
import { useVirtualList } from '@vueuse/core'


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

    const { list, containerProps, wrapperProps } = useVirtualList(this.orderedData, {
      itemHeight: 96,
    }); 

  },
  components: { LabelReleases }
}
</script>

<style>
</style>
