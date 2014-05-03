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

from requests import get

from classify import create_classifier
from classify import load_data_from_file
from classify import translate_data_to_scikit
from classify import pad_data

test_data = get('http://www.tide-pool.ca/pattern-recognition/example_data/test-data.json')

app = Flask(__name__)

#small_classifier, small_max_length = create_classifier(['piano', 'small_grid', 'xylophone', 'piano_roll', 'zither'])
small_classifier, small_max_length = ('', '')
def objects_from_image():
    pass

def data_from_objects():
    pass

def classification_from_data(example_data):
    if len(example_data) < small_max_length:
        example_data = pad_data(example_data, small_max_length)
        res = small_classifier.predict([example_data])

        return res


## We will eventually remove this GET thang.
@app.route("/analysis", methods=['GET', 'POST'])
def analyze_data():
    print request.json
    raw_data = translate_data_to_scikit(raw_data)
    res = classification_from_data(raw_data)
    return "We have, in theory, parsed the data and returned JSON"

@app.route("/image", methods=['POST'])
def analyze_image():
    return "We have, in theory, parsed the image and returned JSON"


# Test to make sure that we are loading and anaylzing data correctly
@app.route("/test_analysis", methods=['GET'])
def fake_analysis():
    raw_data = load_data_from_file('test_data')
    raw_data = translate_data_to_scikit(raw_data)
    raw_example = raw_data[0]

    res = classification_from_data(raw_example)
    return "Hello, we have just done a test classification:  %s" % res[0]


# Test to make sure that the server is up
@app.route("/hello", methods=['GET'])
def hello():
    return "Hello, I am a Flask server:  %s" % test_data.json()

if __name__ == "__main__":
    app.run(debug=True)