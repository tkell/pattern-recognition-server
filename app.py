#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Webserver.  This needs to take data from the mobile app, 
classify it, and return a list of classifications.
It will be the mobile app's responsibility to do 
mapping based on the classifications (piano, grid, offset grid, ec)
'''

from flask import Flask
from flask import request
app = Flask(__name__)


def objects_from_image():
    pass

def data_from_objects():
    pass

def classification_from_data():
    pass


## We will eventually remove this GET thang.
@app.route("/analysis", methods=['GET', 'POST'])
def analyze_data():
    print request.json


    res = classification_from_data()
    return "We have, in theory, parsed the data and returned JSON"

@app.route("/image", methods=['POST'])
def analyze_image():
    return "We have, in theory, parsed the image and returned JSON"


if __name__ == "__main__":
    app.run(debug=True)