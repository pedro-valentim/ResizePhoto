# ResizePhoto

This repo is for solving the problem below.

Given a Webservice endpoint(http://54.152.221.29/images.json), that returns a JSON of
ten photos, consume it and generate three different photo formats for each one, that must
be small (320x240), medium (384x288) and large (640x480).

Finally, write a Webservice endpoint, which should use a non-relational
database(MongoDB preferred) and list (in JSON format) all ten photos with their
respective formats, providing their URLs.

Steps to build/run app
--------------------

- First of all, install [docker](https://docs.docker.com/engine/installation/) and [docker-compose](https://docs.docker.com/compose/install/).

- Download or clone this repo, then enter dir to build/run docker containers.
```
git clone https://github.com/pedro-valentim/ResizePhoto.git
cd ResizePhoto
docker-compose up --build -d
```

Application now should be up and running on *localhost:5000*

- In order to know if app is already up and running, this is the command:

```
docker logs -f `docker ps | grep "resizephoto_web:latest" | awk '{ print $1 }'`
```
