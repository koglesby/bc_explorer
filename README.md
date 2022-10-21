How I got it to run

(created vitual environment)
$ python3 -m venv venv

(activate virtual environment)
$ source venv/bin/activate

(venv) $ pip install -r requirements.txt

maybe need to add more to the requirements.txt?
(venv) $ pip install Flask
(venv) $ pip install Flask-Cors

(start the app at localhost:5000)
flask run

Add the labels that are currently hardcoded

// data/label_urls.json
{"GD4YA": "https://gd4ya.bandcamp.com", "SVBKVLT": "https://svbkvlt.bandcamp.com", "The Flenser": "https://theflenser.bandcamp.com"}

reload the page
