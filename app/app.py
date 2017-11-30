# coding: utf-8
import os
from pymongo import MongoClient
from flask import Flask, jsonify, send_from_directory, redirect, url_for
from werkzeug.contrib.cache import MemcachedCache

FLASK_BIND_PORT = int(os.environ.get('FLASK_BIND_PORT', '5000'))

app = Flask(__name__)
cache = MemcachedCache(['memcached:11211'])

mongodb_host = os.environ.get('MONGODB_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGODB_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)
db = client.resizephoto_db


def get_files_list():
    return list(db.image_collection.find({}, {'_id': False, 'image_url': False}).sort("_id", 1))


@app.route('/')
def index():
    return redirect(url_for('list_images'))


@app.route('/result.json')
def list_images():
    files = get_files_list()
    return jsonify({"images": [file['resized_images_dict'] for file in files]})


@app.route('/images/<path:path>')
def images(path):
    return send_from_directory('images/', path)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=FLASK_BIND_PORT)
