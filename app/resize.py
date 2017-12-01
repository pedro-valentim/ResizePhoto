# coding: utf-8
import os
import requests
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
url = os.environ.get('WEBSERVICE_ENDPOINT')

SIZES = {
    'small': (320, 240),
    'medium': (384, 288),
    'large': (640, 480),
}


class Resizer(object):

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

    @classmethod
    def resize_images(cls):
        response = requests.get(url)
        images = response.json()['images']

        # loop over all images from specified endpoint
        for img in images:
            # get the image's url
            img_url = img['url']
            # search for already resized images with this url on MongoDB
            img_document = db.image_collection.find_one({u'image_url': img_url})
            print('-------> Using existing document - {} (id)'.format(img_document['_id']))
            # if nothing was found we should do the conversions and save at the end
            if img_document is None:
                inserted_id = cls.create_document(img_url)
                print('-------> Created a new document - {} (id)'.format(inserted_id))


if __name__ == '__main__':
    Resizer.resize_images()
