<template>
  <a :href="url">
    <img class="img-fluid" :src="cover" alt="Cover image cap">
    <div class="card-body">
        <h5 class="card-title">{{artist}}</h5>
        <p>{{title}}</p>
    </div>
  </a>
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

<style></style>
