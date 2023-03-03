<template>
  <b-container fluid="sm" class="search-enter">
    <b-row>
      <b-col>
        <div class="user-search-info">
          <p>Import your Bandcamp following list:</p>
        </div>
        <input type="search" class="nosubmit form-control" placeholder="Search for your user name on Bandcamp..."
          @keyup.enter="useSearchUser" v-model="enter_search_term">
        <div class="results-container">
          <div v-for='n in search_res_data' v-bind:key="n.id" class="search-result">
            <div @click="clickAddUser(n.url)" v-on-clickaway="away">
              <b-img thumbnail fluid left :src="n.img_src"></b-img>
              <div class="result-info">
                <div class="heading">
                  {{ n.name }}
                </div>
                <div class="genre">
                  Genre: {{ n.genre }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>
  
<script>
import { store } from './store'
import { mixin as clickaway } from 'vue-clickaway';

export default {
  data() {
    return {
      store,
      enter_search_term: "",
      search_res_data: [],
    };
  },
  // use clickaway to empty the search response data when user clicks away from component
  mixins: [clickaway],
  methods: {
    away() {
      this.search_res_data = [];
    },

    useSearchUser() {
      const base_url = process.env.NODE_ENV === "development" ? 'http://127.0.0.1:5000/' : '';

      const url = base_url + "/search_user/";

      fetch(url, {
        method: "POST",
        headers: new Headers({
          "Content-Type": "application/json",
        }),
        body: JSON.stringify({
          search_term: this.enter_search_term,
        }),
      })
        .then((response) => {
          if (!response.ok)
            throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          this.search_res_data = data.search_res;
          this.enter_search_term = "";
        })
        .catch((error) => console.log(error));
    },

    clickAddUser(labelUrl) {
      // this.store.addNewLabel(name, labelUrl, itemtype);
      const url = "http://127.0.0.1:5000/get_following/";
      fetch(url, {
        method: "POST",
        headers: new Headers({
          "Content-Type": "application/json",
        }),
        body: JSON.stringify({
          url: labelUrl,
        }),
      })
        .then((response) => {
          if (!response.ok)
            throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          data['labels'].forEach((label_info) => {
            console.log(label_info);
            this.store.addNewLabel(label_info['label_name'], label_info['label_url'], 'LABEL') // item type hard-coded to label for now
          });
        })
        .catch((error) => console.log(error));
      this.search_res_data = [];
    },
  },
  components: {}
}
</script>
  
<style>
.itemtype {
  font-size: 10px;
  color: #999;
  margin-bottom: 0.5em;
}

.heading {
  font-size: 16px;
  margin-bottom: 0.1em;
}

.search-enter {
  margin-top: 3%;
  margin-bottom: 3%;
}

.user-search-info {
  font-weight: bold;
}

input.nosubmit {
  display: block;
  padding: 9px 4px 9px 40px;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' class='bi bi-search' viewBox='0 0 16 16'%3E%3Cpath d='M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z'%3E%3C/path%3E%3C/svg%3E") no-repeat 13px center;
  background-color: rgba(255, 255, 255, 0.902);

  /* offset-x | offset-y | blur-radius | spread-radius | color */
  box-shadow: 0px 0px 3px 2px rgba(0, 0, 0, 0.1);
}

.results-container {
  max-height: 400px;
  overflow: scroll;
  overflow-y: auto;
  overflow-x: hidden;

  /* offset-x | offset-y | blur-radius | spread-radius | color */
  box-shadow: 0px 2px 6px 4px rgba(0, 0, 0, 0.1);
}

.result-info {
  color: #595959;
  vertical-align: top;
  margin-left: 1.3em;
  line-height: 1em;
}

.search-result:hover {
  background-color: rgba(212, 248, 255, 0.97);
}

.search-result {
  cursor: pointer;
  height: 80px;
  background-color: rgba(255, 235, 253, 0.97);
  border-bottom: 1px solid #e1d4d4;
}

.search-result img {
  object-fit: cover;
  width: 80px;
  height: 80px;
  margin-right: 15px;
}
</style>
  