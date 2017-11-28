# coding: utf-8
from pymongo import MongoClient
from flask import Flask, jsonify, send_from_directory, redirect, url_for

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.resizephoto_db


@app.route('/')
def index():
    return redirect(url_for('list_images'))


@app.route('/result.json')
def list_images():
    files = list(db.image_collection.find({}, {'_id': False, 'image_url': False}).sort("_id", 1))
    return jsonify({"images": [file['resized_images_dict'] for file in files]})


@app.route('/images/<path:path>')
def images(path):
    return send_from_directory('images/', path)


if __name__ == '__main__':
    # resize_images()
    app.run(debug=True, host='0.0.0.0')
