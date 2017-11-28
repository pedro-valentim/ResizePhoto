# coding: utf-8
import requests
import os
from PIL import Image
from pymongo import MongoClient
from StringIO import StringIO

client = MongoClient('localhost', 27017)
db = client.resizephoto_db

app_dir = os.path.dirname(os.path.abspath(__file__))
media_path = os.path.join(app_dir, 'images/')
url = u'http://54.152.221.29/images.json'
sizes = {
    'small': (320, 240),
    'medium': (384, 288),
    'large': (640, 480),
}


def resize_images():
    response = requests.get(url)
    images = response.json()['images']

    # loop over all images from specified endpoint
    for img in images:
        # get the image's url
        img_url = img['url']
        # search for already resized images with this url on MongoDB
        img_document = db.image_collection.find_one({u'image_url': img_url})
        # if nothing was found we should do the conversions and save at the end
        if img_document is None:
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
            for label, size in sizes.items():
                width, height = size
                new_img = opened_img.resize((width, height), Image.ANTIALIAS)
                filename = '{}_{}.{}'.format(name, label, ext)
                img_document['resized_images_dict'][label] = 'http://localhost:5000/images/{}'.format(filename)
                new_img.save(os.path.join(media_path, filename))

            db.image_collection.insert_one(img_document)


if __name__ == '__main__':
    resize_images()
