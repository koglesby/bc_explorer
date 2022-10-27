Vue.component('labels_container', {
  data() {
    return {
      label_data: {},
    };
  },
  async created() {
    const url = 'http://127.0.0.1:5000/all_labels';

    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.label_data = data;
      })
      .catch((error) => console.log(error));
  },
  template: `
    <div class="labels_container">
      <div v-for="(label_url, label_name, index) in label_data">
        <label-releases :label_name="label_name" :label_url="label_url"></label-releases>
      </div>
    </div>
  `,
});

Vue.component('label-releases', {
  props: ['label_name', 'label_url'],
  data() {
    return {
      releases: [],
    };
  },
  async created() {
    const url =
      'http://127.0.0.1:5000/labels?label_name=' +
      this.label_name +
      '&album_num=10';

    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.releases = data;
      })
      .catch((error) => console.log(error));
  },
  updated() {
    tns({
      container: `.${this.label_name.replace(/ /g, '')}`,
      items: 3,
      gutter: 10,
      slideBy: 1,
      controlsPosition: 'bottom',
      navPosition: 'bottom',
      mouseDrag: true,
      autoplay: true,
      autoplayButtonOutput: false,
      controlsContainer: '.custom-control-' + this.label_name.replace(/ /g, ''),
      responsive: {
        0: {
          items: 1,
          nav: false,
        },
        768: {
          items: 3,
          nav: true,
        },
        1440: {
          items: 3,
        },
      },
    });
  },
  template: `
    <div class="container">
      <a :href="label_url">
        <h2>{{this.label_name}}</h2>
      </a>
      <ul class="control" :class="['custom-control-' + this.label_name.replace(/ /g, '')]" >
        <li class="prev">
          <i class="fas fa-angle-left fa-2x"></i>
        </li>
        <li class="next">
          <i class="fas fa-angle-right fa-2x"></i>
        </li>
      </ul>
      <div :class="[this.label_name.replace(/ /g, '')]">
        <div v-for="release, idx in releases" :key="idx">
          <release-card
              :key="release.album_name"
              :url="release.album_url"
              :artist="release.artist_name"
              :cover="release.cover_img_url"
              :title="release.album_name"
          >
          </release-card>
        </div>
      </div>
    </div>
  `,
});

Vue.component('release-card', {
  props: ['url', 'artist', 'cover', 'title'],
  data() {
    return {};
  },
  methods: {},
  template: `
        <a :href="url">
            <img class="img-fluid" :src="cover" alt="Cover image cap">
            <div class="card-body">
                <h5 class="card-title">{{artist}}</h5>
                <p>{{title}}</p>
            </div>
        </a>
    `,
});

Vue.component('search_bar', {
  data() {
    return {
      enter_search_term: '',
      search_res_data: [],
    };
  },
  template: `
  <div class="search_enter">
    <input class="form-control mr-sm-2" placeholder="Search" @keyup.enter="useSearch" v-model="enter_search_term">
    <button class="btn btn-outline-success my-2 my-sm-0" @click="useSearch">Search</button>
    <div v-for='n in search_res_data'>
    <a  href="/"  @click="clickAddLabel(n.name, n.url)">{{n.name}}</a>
    </div>
  </div>
  `,
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
          this.search_res_data = data;
        })
        .catch((error) => console.log(error));
    },
    clickAddLabel(name, label_url) {
      const url = 'http://127.0.0.1:5000/labels/';
      fetch(url, {
        method: 'POST',
        headers: new Headers({
          'Content-Type': 'application/json',
        }),
        body: JSON.stringify({
          label_name: name,
          label_url,
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
});

new Vue({
  el: '#app',
  // async created() {
  // const url = "http://127.0.0.1:5000/"
  // const response = await fetch(url)
  // const data = await response.json()
  // this.releases = data;
  // },
  data() {
    return {
      enter_label_name: '',
      enter_label_url: '',
      enter_search_term: 'search',
    };
  },
  methods: {
    addLabelURL() {
      console.log(
        'Adding label ' +
          this.enter_label_name +
          ' and url ' +
          this.enter_label_url
      );
      const url = 'http://127.0.0.1:5000/labels/';
      fetch(url, {
        method: 'POST',
        headers: new Headers({
          'Content-Type': 'application/json',
        }),
        body: JSON.stringify({
          label_name: this.enter_label_name,
          label_url: this.enter_label_url,
        }),
      })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {})
        .catch((error) => console.log(error));

      this.enter_label_name = '';
      this.enter_label_url = '';
    },
  },
});
