# Developing a Single Page App with Flask and Vue.js

### Want to learn how to build this?

Check out the [post](https://testdriven.io/developing-a-single-page-app-with-flask-and-vuejs).

## Want to use this project?

1. Fork/Clone

1. Run the server-side Flask app in one terminal window:

    ```sh
    $ cd server
    $ python3.9 -m venv env
    $ source env/bin/activate
    (env)$ pip install -r requirements.txt
    (env)$ python app.py
    ```

    Navigate to [http://localhost:5000](http://localhost:5000)

1. Configure Firebase, start emulators for development

    Add Firebase credentials to your environment
    ```
    // client/.env
    VUE_APP_FIREBASE_API_KEY=some-key-blah
    VUE_APP_FIREBASE_AUTH_DOMAIN=some-auth-domain
    VUE_APP_FIREBASE_PROJECT_ID=some-project-name
    VUE_APP_FIREBASE_STORAGE_BUCKET=storage-bucket-url
    VUE_APP_FIREBASE_MESSAGING_SENDER_ID=some-id-number
    VUE_APP_FIREBASE_APP_ID=some-app-id-number
    VUE_APP_FIREBASE_MEASUREMENT_ID=some-other-id
    ```

    Make sure you have firebase tools installed
    ```
    npm install -g firebase-tools
    ```
    or
    ```
    curl -sL firebase.tools | bash
    ```
    (side note) maybe firebase-tools should be added as a devDependency

    Start the emulators
    ```sh
    $ firebase emulators:start
    ```

1. Run the client-side Vue app in a different terminal window:

    ```sh
    $ cd client
    $ npm install
    $ npm run serve
    ```

    Navigate to [http://localhost:8080](http://localhost:8080)

