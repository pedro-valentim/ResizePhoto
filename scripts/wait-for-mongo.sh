#!/bin/bash
# wait-for-mongo.sh

set -e
cmd="$@"

until python -c "from pymongo import MongoClient ; MongoClient('db').resizephoto_db.image_collection"; do
  >&2 echo "MongoDB is unavailable - sleeping 10s"
  sleep 10
done

>&2 echo "MongoDB is up - continuing"
exec $cmd