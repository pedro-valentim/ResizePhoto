# coding: utf-8
import os
import requests
import json
from PIL import Image
from pymongo import MongoClient
from StringIO import StringIO


FLASK_BIND_PORT = int(os.environ.get('FLASK_BIND_PORT', '5000'))

mongodb_host = os.environ.get('MONGODB_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGODB_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)
db = client.resizephoto_db

app_dir = os.path.dirname(os.path.abspath(__file__))
media_path = os.path.join(app_dir, 'images/')
WEBSERVICE_ENDPOINT = os.environ.get('WEBSERVICE_ENDPOINT')

SIZES = {
    'small': (320, 240),
    'medium': (384, 288),
    'large': (640, 480),
}


class Resizer(object):

    def __init__(self, webservice_endpoint=WEBSERVICE_ENDPOINT, json=None):
        self.webservice_endpoint = webservice_endpoint
        self.raw_json = json

    @classmethod
    def create_document(cls, img_url):
        # make a request to img's url in order to get its content later
        img_response = requests.get(img_url)
        # creates a PIL's Image object with response content
        opened_img = Image.open(StringIO(img_response.content))
        # get name and extension of the image
        name, ext = img_url.split('/')[-1].split('.')
        # create empty document for insertion in image collection
        img_document = {
            "image_url": img_url,
            "resized_images_dict": {}
        }
        # loop over sizes
        for label, size in SIZES.items():
            width, height = size
            new_img = opened_img.resize((width, height), Image.ANTIALIAS)
            filename = '{}_{}.{}'.format(name, label, ext)
            img_document['resized_images_dict'][label] = 'http://localhost:{}/images/{}'.format(
                FLASK_BIND_PORT,
                filename
            )
            new_img.save(os.path.join(media_path, filename))

        return db.image_collection.insert_one(img_document).inserted_id

    def resize_images(self):
        if self.raw_json is None:
            response = requests.get(self.webservice_endpoint)
            images = response.json()['images']
        else:
            images = json.loads(self.raw_json)['images']

        # loop over all images from specified endpoint
        for img in images:
            # get the image's url
            img_url = img['url']
            # search for already resized images with this url on MongoDB
            img_document = db.image_collection.find_one({u'image_url': img_url})

            # if nothing was found we should do the conversions and save at the end
            if img_document is None:
                inserted_id = Resizer.create_document(img_url)
                print('-------> Created a new document - {} (id)'.format(inserted_id))
            else:
                print('-------> Using existing document - {} (id)'.format(img_document['_id']))


if __name__ == '__main__':
    resizer = Resizer()
    resizer.resize_images()
