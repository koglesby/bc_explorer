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
  newlyAddedUrl : '',
  firebaseLabelData: {},
  firebaseFavorites: {},
  // AUTH -> state
  SET_USER(data) {
    this.user.data = data;
  },
  SET_LOGGED_IN(value) {
    this.user.loggedIn = value
  },
  async register({ email, password, name}){
      const response = await createUserWithEmailAndPassword(auth, email, password)
        .catch((error) => {
          const errorCode = error.code;

          if (errorCode === 'auth/email-already-in-use') {
            throw new Error('Unable to register user: Email already exists')
          }
          else {
            throw new Error('Unable to register user') 
          }
        })
      if (response) {
          await updateProfile(response.user, {displayName: name})
          this.SET_USER(response.user);
          // this would add user info to the RTDB, which may not be necessary
          // set(ref(db, 'users/' + response.user.uid), {
          //   username: name,
          //   email: email,
          // });
      }
      //else {
      //    throw new Error('Unable to register user')
      //}
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
        // const errorMessage = error.message;

        if (errorCode === 'auth/user-not-found') {
          throw new Error('Login failed: Username not found')
        }
        else if (errorCode === 'auth/wrong-password') {
          throw new Error('Login failed: Incorrect password') 
        }
        else {
          throw new Error('Login failed')
        }
      });
    if (response) {
      this.SET_USER(response.user);
    } 
    // else {
      // throw new Error('login failed') 
    // }
  },
  async logOut(){
    await signOut(auth)
    this.firebaseLabelData = {};
    this.SET_LOGGED_IN(false);
    this.SET_USER(null);
  },
  async fetchUser(user) {
    this.SET_LOGGED_IN(user !== null);
    if (user) {
      this.SET_USER({displayName: user.displayName, email: user.email})
    } else {
      this.SET_USER(null)
    }
  },
  // get the user's saved Artists/Labels and favorites
  getLabelData(user) {
    const myUserId = user.uid;
    const userItemRef =  query(ref(db, 'users/' + myUserId ));

    onValue(userItemRef, (snapshot) => {
      if (snapshot.exists()) {
        const userSnapData =  snapshot.val();

        this.firebaseLabelData = !!userSnapData.follows ?  userSnapData.follows : {};
        this.firebaseFavorites = !!userSnapData.favorites ? userSnapData.favorites: {};
      } 
    })
  },
  // Add artist or label for a user
  addNewLabel(name, url, itemtype) {
    const myUserId = auth.currentUser.uid;
    const userItemRef = query(ref(db, 'users/' + myUserId + '/follows'), orderByChild('url'), equalTo(url));
    // check the db to see if the current user has an item (artist or label) with the same url
    onValue(userItemRef, (snapshot) => {
      if (snapshot.exists()) {
        console.log("db entry already exists");
      } else {
        // if there isnt an entry with a matching url, add the data to db
        const itemData = {
          name,
          url,
          itemtype,
        };
        // Get a key for a new Item.
        const newItemKey = push(child(ref(db), 'users/' + myUserId + '/follows')).key;
  
        const updates = {};
        // we can add more updates and write them to the db simultaneously
        // (example) updates['/items/' + newItemKey] = itemData;
        updates['/users/' + myUserId + '/follows/' + newItemKey] = itemData;
        
        this.newlyAddedUrl = url;

        return update(ref(db), updates);
      }
    }, {
      onlyOnce: true
    });
  },
  addFavorite(url, artist, cover, title) {
    const myUserId = auth.currentUser.uid;
    const userItemRef = query(ref(db, 'users/' + myUserId + '/favorites'), orderByChild('url'), equalTo(url));

    onValue(userItemRef, (snapshot) => {
      if (snapshot.exists()) {
        console.log("db entry already exists")
      } else {
        const itemData = {
          title,
          artist,
          cover,
          url,
        };
        const newItemKey = push(child(ref(db), 'users/' + myUserId + '/favorites')).key;
        const updates = {};
        updates['/users/' + myUserId + '/favorites/' + newItemKey] = itemData;
  
        return update(ref(db), updates);
      }
    }, {
      onlyOnce: true
    });


  },
  unFavorite(url) {
    const myUserId = auth.currentUser.uid;
    const userItemRef = query(ref(db, 'users/' + myUserId + '/favorites'), orderByChild('url'), equalTo(url));

    onValue(userItemRef, (snapshot) => {
      if (snapshot.exists()) {
        const itemKey = Object.keys(snapshot.val())[0]
        const updates = {};
        updates['/users/' + myUserId + '/favorites/' + itemKey] = null;
        update(ref(db), updates);
      } else {
        console.log("no entry to delete")
      }
    }, {
      onlyOnce: true
    });
  },
  // DELETE delete a label/artist by url
  deleteLabel(url) {
    const myUserId = auth.currentUser.uid;

    const userItemRef = query(ref(db, 'users/' + myUserId + '/follows'), orderByChild('url'), equalTo(url));
    // check the db to see if the current user has an item (artist or label) with the same url
    onValue(userItemRef, (snapshot) => {
      if (snapshot.exists()) {
        const itemKey = Object.keys(snapshot.val())[0]

        // alternative way to delete the item
        // remove(ref(db, 'users/' + myUserId + '/' + itemKey))

        const updates = {};
        updates['/users/' + myUserId + '/follows/' + itemKey] = null;
        update(ref(db), updates);
      } else {
        console.log("no entry to delete")
      }
    }, {
      onlyOnce: true
    });
  }
})
