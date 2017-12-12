# coding: utf-8
import os
from pymongo import MongoClient
from flask import Flask, send_from_directory, redirect, url_for
# import the flask extension
from flask.ext.cache import Cache
from resize import Resizer

FLASK_BIND_PORT = int(os.environ.get('FLASK_BIND_PORT', '5000'))

app = Flask(__name__)

# setting cache on Flask app
app.config["CACHE_TYPE"] = "memcached"
app.cache = Cache(app)

mongodb_host = os.environ.get('MONGODB_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGODB_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)
db = client.resizephoto_db


@app.route('/')
def index():
    return redirect(url_for('list_images'))


@app.route('/result.json')
def list_images():
    return Resizer().get_json()


@app.route('/images/<path:path>')
def images(path):
    return send_from_directory('images/', path)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=FLASK_BIND_PORT)
