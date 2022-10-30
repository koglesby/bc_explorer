<template>
  <div class="search_enter">
    <input class="form-control mr-sm-2" placeholder="Search" @keyup.enter="useSearch" v-model="enter_search_term">
    <button class="btn btn-outline-success my-2 my-sm-0" @click="useSearch">Search</button>
    <div v-for='n in search_res_data'  v-bind:key="n.id">
    <a href="/" @click="clickAddLabel(n.name, n.url)">{{n.name}}</a>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      enter_search_term: '',
      search_res_data: [],
    };
  },
  methods: {
    useSearch() {
      const url = 'http://127.0.0.1:5000/search/';
      fetch(url, {
        method: 'POST',
        headers: new Headers({
          'Content-Type': 'application/json',
        }),
        body: JSON.stringify({
          search_term: this.enter_search_term,
        }),
      })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          this.search_res_data = data.search_res;
        })
        .catch((error) => console.log(error));
    },
    clickAddLabel(name, labelUrl) {
      const url = 'http://127.0.0.1:5000/labels/';
      fetch(url, {
        method: 'POST',
        headers: new Headers({
          'Content-Type': 'application/json',
        }),
        body: JSON.stringify({
          label_name: name,
          label_url: labelUrl,
        }),
      })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {})
        .catch((error) => console.log(error));
    },
  },
}
</script>

<style>
</style>
