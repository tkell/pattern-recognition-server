#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Webserver.  This needs to take data from the mobile app, 
classify it, and return a list of classifications.
'''

from collections import OrderedDict

from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
from flask import render_template

from requests import get

from classify import create_classifier_from_data
from classify import load_data_from_file
from classify import translate_data_to_scikit
from cross_domain import crossdomain
from mapping import map_as
from modifier_functions import check_size, check_basic_kalimba, check_staff


# ['piano', 'xylophone','piano_roll', 'zither', 'small_grid', 'large_grid', 'tonnetz','circle']
ALL_CLASSIFICATIONS = ['piano', 'xylophone','piano_roll', 'zither',
                       'small_grid', 'large_grid', 'tonnetz','circle']

classification_list = []
for classification in ALL_CLASSIFICATIONS:
    data = get('http://www.tide-pool.ca/pattern-recognition/example-data/%s.json' % classification).json()
    classification_list.append((data, classification))

classifier = create_classifier_from_data(classification_list)

app = Flask(__name__)

# this will be were we talk to the image api stuf
def objects_from_image():
    #image_to_button_data
    pass

def mapping_from_classification(classification, button_data, adventure, modifier):
    mapped_buttons = map_as(classification, button_data, adventure, modifier)
    return mapped_buttons

def classification_from_data(example_data):
    translated_data = translate_data_to_scikit([example_data])
    res =  classifier.predict(translated_data)

    # For certain prototypes, check size patterns
    modifier = None
    if 'radius' in example_data[0]:
        if res[0] == 'zither':
            modifier = check_size(example_data, 'y')
        elif res[0] == 'xylophone':
            modifier = check_size(example_data, 'x')
            if not modifier:
                modifier = check_basic_kalimba(example_data)

    if not modifier and res[0] == 'zither' and 'shape' in example_data[0]:
        modifier = check_staff(example_data)

    return res, modifier

@app.route("/analysis", methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers=['Content-Type'])
def analyze_data():
    # Transform the data, get a classification
    button_data = request.json
    if 'adventure' in button_data:
        adventure = button_data['adventure']
    else:
        adventure = 0

    if 'buttonData' in button_data:
        button_data = button_data['buttonData']
    else:
        button_data = button_data

    res, modifier = classification_from_data(button_data)
    classification = res[0]
    # Create mapping, return mapping and the classification
    mapping_data = mapping_from_classification(classification, button_data, 
            adventure, modifier)
    return_data = {'result': classification, 'mapping': mapping_data, 'modifier': modifier}

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


@app.route("/validate/<layout_type>", methods=['GET'])
def validate(layout_type):
    if layout_type == 'all':
        classifications = ALL_CLASSIFICATIONS
    else:
        classifications = [layout_type]

    results = OrderedDict()
    for classification in classifications:
        results[classification] = (0, 0, {})
        data_url = 'http://www.tide-pool.ca/pattern-recognition/example-data/%s.json' % classification
        example_data = get(data_url).json()

        correct = 0
        incorrect = 0
        incorrect_details = {}
        for example in example_data:
            res, modifier = classification_from_data(example)
            if res[0] == classification:
                correct += 1
            else:
                if res[0] not in incorrect_details:
                    incorrect_details[res[0]] = 1
                else:
                    incorrect_details[res[0]] += 1
                incorrect += 1

        incorrect_string = ''
        for bad_classification in incorrect_details:
            incorrect_string = incorrect_string + \
            '%s:  %d.  ' % (bad_classification, incorrect_details[bad_classification])

        results[classification] = (correct, incorrect, incorrect_string)
    
    return render_template('validate.html', classification=layout_type, results=results)

# Test to make sure that we are loading and anaylzing data correctly
@app.route("/test_analysis", methods=['GET'])
def fake_analysis():
    piano_data = get('http://www.tide-pool.ca/pattern-recognition/example-data/piano.json').json()
    res, modifier = classification_from_data(piano_data[0])
    classification = res[0]
    return "Hello, we have just done a test classification:  %s" % classification

# Test to make sure that the server is up
@app.route("/hello", methods=['GET'])
def hello():
    return "Hello there, the server is up."

if __name__ == "__main__":
    app.run()
