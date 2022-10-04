from flask import Flask, jsonify
from flask_cors import CORS
from scraping import get_label_page
import json

app = Flask(__name__)
CORS(app)

# def load_data(filename):
# 	with open(filename, 'r') as f:
# 		return json.load(f)

# def load_dicts():
# 	return load_data('images.json'), load_data('quotes.json')

# def clear_nulls():
# 	images, quotes = load_dicts()
# 	new_images = {}
# 	new_quotes = {}
# 	for author in images.keys():
# 		if images[author]:
# 			new_images[author] = images[author]
# 			new_quotes[author] = quotes[author]
# 	return new_images, new_quotes

# def create_authors_list(authors):
# 	step = 3
# 	return [authors[i:i+step] for i in range(0, len(authors), step)]

@app.route("/")
def get_label_releases():
	return jsonify(get_label_page("SVBKVLT", album_num=20))