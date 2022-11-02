import { reactive } from 'vue'

export const store = reactive({
  labelData: {},
//   loadLabels(data) {
//     this.labelData = data;
//   },
//   addNewLabel(newData) {
//     this.labelData = { 
//         ...this.labelData, 
//         [newData.label_name]: newData.label_url
//     }
//   },
  getLabelData() {
  const url = "http://127.0.0.1:5000/all_labels";
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok)
          throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.labelData = data;
      })
      .catch((error) => console.log(error));
  },
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
        this.labelData = { 
            ...this.labelData, 
            [newData.label_name]: newData.label_url
        }
      })
      .catch((error) => console.log(error));
  },
})
