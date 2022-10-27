from crypt import methods
from flask import Flask, jsonify, request, abort, Response, render_template
from flask_cors import CORS
from scraping import get_label_page, get_label_urls, scrape_search
from utils import save_label_url

app = Flask(__name__)
CORS(app)


@app.route("/")
def get_homepage():
    return render_template('index.html')


@app.route("/labels/", methods=['GET'])
def get_label_releases():
    """Get label releases based on label name."""
    try:
        label_name = request.args.get("label_name", default="", type=str)
        album_num = request.args.get("album_num", default=10, type=int)
    except:
        abort(400, "Cannot parse label name and album num from request.")

    try:
        releases = get_label_page(label_name=label_name, album_num=album_num)
    except (ValueError, KeyError) as vke:
        abort(400, str(vke))
    except Exception as e:
        abort(503, str(e))

    return jsonify(releases)


@app.route("/all_labels", methods=['GET'])
def get_all_labels():
    try:
        label_stuff = get_label_urls()
        label_data = jsonify(label_stuff)
    except (ValueError, KeyError) as vke:
        abort(400, str(vke))
    except Exception as e:
        abort(503, str(e))

    return label_data


@app.route("/labels/", methods=['POST'])
def enter_label_url():
    """Save a label and its url entered by user."""
    try:
        label_name = request.json['label_name']
        label_url = request.json['label_url']
    except:
        abort(400, "Cannot parse label name and url from request from.")

    try:
        save_label_url(label_name=label_name, url=label_url)
    except Exception as e:
        abort(503, str(e))

    resp_dict = {
        "label_name": label_name,
        "label_url": label_url,
    }
    return resp_dict, 200


@app.route("/search/", methods=['POST'])
def useSearch():
    """Search for a label or artist"""
    try:
        search_term = request.json['search_term']
    except:
        abort(400, "Cannot parse search term")

    try:
        search_res = scrape_search(search_term=search_term)
    except Exception as e:
        abort(503, str(e))

    return search_res, 200
