#!/bin/bash
set -e

export MONGODB_HOST=db
export MONGODB_PORT=27017

echo "---> Waiting for MongoDB";
while ! nc -z $MONGODB_HOST $MONGODB_PORT;
do
	echo ".";
	sleep 2;
done;

echo "---> Running Resizing"
python -u /app/resize.py

echo "---> Running Flask app"
python -u /app/app.py