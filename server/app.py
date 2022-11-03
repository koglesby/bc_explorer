import uuid
from flask import Flask, jsonify, request, abort, Response, render_template
from flask_cors import CORS

from crypt import methods
from scraping import get_label_page, get_label_urls, scrape_search
from utils import save_label_url, deleteArtLab

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


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
        label_urls = get_label_urls()
        label_data = jsonify(label_urls)
    except (ValueError, KeyError) as vke:
        abort(400, str(vke))
    except Exception as e:
        abort(503, str(e))

    return label_data


@app.route("/labels/", methods=['POST', 'DELETE'])
def enter_label_url():
    """Save a label and its url entered by user."""
    if request.method == 'POST':
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
    if request.method == 'DELETE':
        try:
            label_name = request.json['label_name']
            label_urls_obj = deleteArtLab(label_name)
        except Exception as e:
            abort(503, str(e))

        resp_dict = {
            "label_urls": label_urls_obj
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

    resp_dict = {
        "search_res": search_res
    }
    return resp_dict, 200


if __name__ == '__main__':
    app.run()
