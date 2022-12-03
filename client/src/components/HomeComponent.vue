<template>
  <div class="main-container">
    <SearchBar></SearchBar>
    <LabelsContainer></LabelsContainer>
  </div>
</template>

<script>
import SearchBar from './SearchBar.vue';
import LabelsContainer from './LabelsContainer.vue';

export default {
  data() {
    return {};
  },
  components: { LabelsContainer, SearchBar },
  methods: {
    clickHello() {
      this.$router.push('/dashboard')
    }
  },
};
</script>

<style>
.card-img-top {
  height: 150px;
  width: 150px;
  object-fit: cover;
}

.main-container {
  margin-top: 100px;
}

.card-body {
  padding-left: 0;
}
</style>
