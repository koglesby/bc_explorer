import { reactive } from 'vue'

export const store = reactive({
  labelData: {},
  loadLabels(data) {
    this.labelData = data;
  },
//   addNewLabel(newData) {
//     this.labelData = { 
//         ...this.labelData, 
//         [newData.label_name]: newData.label_url
//     }
//   },

  // GET label data
  getLabelData() {
  const url = "http://127.0.0.1:5000/all_labels";
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok)
          throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // use the returned data to update state
        this.loadLabels(data);
      })
      .catch((error) => console.log(error));
  },
  // POST add a new label/artist
  addNewLabel(name, labelUrl) {
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
      .then((newData) => {
        // add the recently saved data to the existing state
        this.labelData = { 
            ...this.labelData, 
            [newData.label_name]: newData.label_url
        }
      })
      .catch((error) => console.log(error));
  },
  // DELETE delete a label/artist by name
  deleteLabel(label_name) {
    const url = 'http://127.0.0.1:5000/labels/';
    fetch(url, {
      method: 'DELETE',
      headers: new Headers({
        'Content-Type': 'application/json',
      }),
      body: JSON.stringify({
        label_name: label_name,
      }),
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // get back data for the remaining entries
        // use that data to update the state
        this.loadLabels(data.label_urls);
      })
      .catch((error) => console.log(error));
  }
})
