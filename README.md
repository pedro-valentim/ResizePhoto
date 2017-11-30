# ResizePhoto

This repo is for solving the problem below.

Given a Webservice endpoint(http://54.152.221.29/images.json), that returns a JSON of
ten photos, consume it and generate three different photo formats for each one, that must
be small (320x240), medium (384x288) and large (640x480).

Finally, write a Webservice endpoint, which should use a non-relational
database(MongoDB preferred) and list (in JSON format) all ten photos with their
respective formats, providing their URLs.