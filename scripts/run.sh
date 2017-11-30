#!/bin/bash
set -e

echo -n "---> Waiting for MongoDB";
while ! nc -z $MONGODB_HOST $MONGODB_PORT;
do
	echo -n ".";
	sleep 1;
done;

echo "";
echo "---> Running Resizing"
python -u /app/resize.py

echo "---> Running Flask app"
python -u /app/app.py