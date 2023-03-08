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

    Start the emulators in a different terminal window
    ```sh
    $ cd client
    $ firebase emulators:start
    ```

1. Run the client-side Vue app in a different (3rd) terminal window:

    ```sh
    $ cd client
    $ npm install
    $ npm run serve
    ```

    Navigate to [http://localhost:8080](http://localhost:8080)

## Building with Docker
The dockerization of this project used this [post](https://testdriven.io/blog/deploying-flask-to-heroku-with-docker-and-gitlab/) as a reference.

1. To run this project with Docker, first make sure you have docker installed (https://docs.docker.com/get-docker/) and running and your firebase credentials added to your environment as above.
1. You can build and run the project with a simple command:
```
docker-compose up --build
```
Navigate to [http://localhost:8007](http://localhost:8007).

Running the project this way will access the real firebase database, NOT an emulated database. Currently I don't recommend this approach for development due to the build times, but it can help make sure changes will work as expected when pushed to production.

You can remove containers when you're ready with the following command:
```
docker-compose down
```
