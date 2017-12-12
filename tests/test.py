import os
from resize import Resizer
from pymongo import MongoClient


mongodb_host = os.environ.get('MONGODB_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGODB_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)
db = client.resizephoto_test_db


def tests_json_with_one_image():
    img_url = 'http://via.placeholder.com/640x480/fcfcfc/400.jpg'
    resizer = Resizer(json='''{
      "images": [
        {
          "url": "%s"
        }
      ]
    }''' % img_url)

    resizer.resize_images()

    new_document = db.image_collection.find_one({u'image_url': img_url})

    assert new_document is not None


def tests_creation_skip_with_repeated_url():
    img_url = 'http://via.placeholder.com/640x480/fcfcfc/400.jpg'
    document = db.image_collection.find_one({u'image_url': img_url})

    resizer = Resizer(json='''{
      "images": [
        {
          "url": "%s"
        }
      ]
    }''' % img_url)

    resizer.resize_images()

    filtered_documents = list(db.image_collection.find({u'image_url': img_url}))

    assert len(filtered_documents) == 1 and filtered_documents[0]['_id'] == document_id
