#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Webserver.  This needs to take data from the mobile app, 
classify it, and return a list of classifications.
'''

from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify

from requests import get

from classify import create_classifier_from_data
from classify import load_data_from_file
from classify import translate_data_to_scikit
from classify import pad_data
from cross_domain import crossdomain


# Create small classifier
piano_data = get('http://www.tide-pool.ca/pattern-recognition/example-data/piano.json').json()
xylophone_data = get('http://www.tide-pool.ca/pattern-recognition/example-data/xylophone.json').json()
small_grid_data = get('http://www.tide-pool.ca/pattern-recognition/example-data/small_grid.json').json()
piano_roll_data = get('http://www.tide-pool.ca/pattern-recognition/example-data/piano_roll.json').json()
zither_data = get('http://www.tide-pool.ca/pattern-recognition/example-data/zither.json').json()
small_classifier, small_max_length = create_classifier_from_data([(piano_data, 'piano'), 
                                                                (xylophone_data, 'xylophone'),
                                                                (small_grid_data, 'small grid'),
                                                                (piano_roll_data, 'piano roll'),
                                                                (zither_data, 'zither'),
                                                                ])
# Create large classifier
big_piano_data = get('http://www.tide-pool.ca/pattern-recognition/example-data/big_piano.json').json()
large_grid_data = get('http://www.tide-pool.ca/pattern-recognition/example-data/large_grid.json').json()
large_classifier, large_max_length = create_classifier_from_data([(big_piano_data, 'big_piano'), 
                                                                (large_grid_data, 'large_grid'),
                                                                ])

app = Flask(__name__)

def objects_from_image():
    pass

def data_from_objects():
    pass

def classification_from_data(example_data):
    if len(example_data) < small_max_length:
        example_data = pad_data(example_data, small_max_length)
        res = small_classifier.predict([example_data])

        return res

@app.route("/analysis", methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers=['Content-Type'])
def analyze_data():
    raw_data = translate_data_to_scikit([request.json])
    raw_example = raw_data[0]
    res = classification_from_data(raw_example)
    
    # debugz
    print res[0]

    return_data = {'result': res[0]}

    # Ugly.  I appear to need both these AND the @crossdomain decorator.
    # Must be fixed, but not now.
    resp = make_response(jsonify(**return_data))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST'
    resp.headers['Access-Control-Max-Age'] = 54000
    return resp

@app.route("/image", methods=['POST'])
def analyze_image():
    return "We have, in theory, parsed the image and returned JSON"


# Test to make sure that we are loading and anaylzing data correctly
@app.route("/test_analysis", methods=['GET'])
def fake_analysis():
    piano_data = get('http://www.tide-pool.ca/pattern-recognition/example-data/piano.json').json()
    raw_data = translate_data_to_scikit(piano_data)
    raw_example = raw_data[0]

    res = classification_from_data(raw_example)
    return "Hello, we have just done a test classification:  %s" % res[0]


# Test to make sure that the server is up
@app.route("/hello", methods=['GET'])
def hello():
    return "Hello, I am a Flask server"

if __name__ == "__main__":
    app.run(debug=True)