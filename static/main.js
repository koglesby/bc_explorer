Vue.component('label-releases', {
  props: ['label_name'],
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
      <h2>{{this.label_name}}</h2>
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
