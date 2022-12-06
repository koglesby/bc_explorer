<template>
  <div class="card bg-light mb-3" style='height:max-content; border: 0px'>
    <a :href="url">
      <img class="card-img-top img-fluid" :src="cover" alt="Cover image cap">
      <div class="card-body">
        <h5 class="card-title text-truncate" style="color: black">{{ artist }}</h5>
        <p class="card-text text-truncate" style="color: black">{{ title }}</p>
      </div>
    </a>
  </div>
  
</template>

<script>
export default {
  props: ['url', 'artist', 'cover', 'title'],
  data() {
    return {};
  },
  methods: {}
}
</script>

<style>

</style>
