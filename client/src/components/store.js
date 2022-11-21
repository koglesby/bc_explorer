import { reactive } from 'vue'
import { createUserWithEmailAndPassword, signInWithEmailAndPassword, updateProfile, signOut, setPersistence, browserLocalPersistence } from "firebase/auth";
import { auth, db } from '../main';
import { ref, set, child, push, update, query, orderByChild, equalTo, onValue, remove } from "firebase/database";

// https://firebase.google.com/docs/database/web/read-and-write 
export const store = reactive({
  user: {
    loggedIn: null,
    data: null
  },
  firebaseLabelData: {},
  // AUTH -> state
  SET_USER(data) {
    this.user.data = data;
  },
  SET_LOGGED_IN(value) {
    this.user.loggedIn = value
  },
  async register({ email, password, name}){
      const response = await createUserWithEmailAndPassword(auth, email, password)
      if (response) {
          this.SET_USER(response.user);
          updateProfile(response.user, {displayName: name})
          set(ref(db, 'users/' + userId), {
            username: name,
            email: email,
          });
      } else {
          throw new Error('Unable to register user')
      }
  },    
  // Existing and future Auth states are persisted after closing browser window
  async logIn({ email, password }){    
    const response = await setPersistence(auth, browserLocalPersistence)
      .then(() => {
        return signInWithEmailAndPassword(auth, email, password);
      })
      .catch((error) => {
        // Handle Errors here.
        const errorCode = error.code;
        const errorMessage = error.message;
      });
    if (response) {
      this.SET_USER(response.user);
    } else {
        throw new Error('login failed')
    }
  },
  async logOut(){
    await signOut(auth)
    this.SET_USER(null)
  },
  async fetchUser(user) {
    this.SET_LOGGED_IN(user !== null);
    if (user) {
      this.SET_USER({displayName: user.displayName, email: user.email})
    } else {
      this.SET_USER(null)
    }
  },
  // get the user's saved Artists/Labels
  getLabelData(user) {
    const myUserId = user.uid;
    const userItemRef = query(ref(db, 'users/' + myUserId), orderByChild('url'));
    // check the db to see if the current user has an item (artist or label) with the same url
    onValue(userItemRef, (snapshot) => {
      if (snapshot.exists()) {

        const userSnapData =  snapshot.val();
        // create an object identical to userSnapData, but with username and email removed
        const {username, email, ...userSavedItems} = userSnapData;

        this.firebaseLabelData = userSavedItems; 
      } else {
        this.firebaseLabelData = {}
      }
    })
  },
  // Add artist or label for a user
  addNewLabel(name, url, itemtype) {
    const myUserId = auth.currentUser.uid;
    const userItemRef = query(ref(db, 'users/' + myUserId), orderByChild('url'), equalTo(url));
    // check the db to see if the current user has an item (artist or label) with the same url
    onValue(userItemRef, (snapshot) => {
      if (snapshot.exists()) {
        console.log("db entry already exists")
      } else {
        // if there isnt an entry with a matching url, add the data to db
        const itemData = {
          name,
          url,
          itemtype,
        };
        // Get a key for a new Item.
        const newItemKey = push(child(ref(db), 'users')).key;
  
        const updates = {};
        // we can add more updates and write them to the db simultaneously
        // (example) updates['/items/' + newItemKey] = itemData;
        updates['/users/' + myUserId + '/' + newItemKey] = itemData;
  
        return update(ref(db), updates);
      }
    }, {
      onlyOnce: true
    });
  },
  // DELETE delete a label/artist by url
  deleteLabel(url) {
    const myUserId = auth.currentUser.uid;

    const userItemRef = query(ref(db, 'users/' + myUserId), orderByChild('url'), equalTo(url));
    // check the db to see if the current user has an item (artist or label) with the same url
    onValue(userItemRef, (snapshot) => {
      if (snapshot.exists()) {
        const itemKey = Object.keys(snapshot.val())[0]

        // alternative way to delete the item
        // remove(ref(db, 'users/' + myUserId + '/' + itemKey))

        const updates = {};
        updates['/users/' + myUserId + '/' + itemKey] = null;
        update(ref(db), updates);
      } else {
        console.log("no entry to delete")
      }
    }, {
      onlyOnce: true
    });
  }
})
