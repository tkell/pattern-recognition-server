#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Test script for the classification data
'''

from requests import get

from classify import create_classifier_from_data
from classify import load_data_from_file
from classify import translate_data_to_scikit

# Create small classifier
print "Downloading classifier data.."
piano_data = get('http://www.tide-pool.ca/pattern-recognition/example-data/piano.json').json()
xylophone_data = get('http://www.tide-pool.ca/pattern-recognition/example-data/xylophone.json').json()
small_grid_data = get('http://www.tide-pool.ca/pattern-recognition/example-data/small_grid.json').json()
piano_roll_data = get('http://www.tide-pool.ca/pattern-recognition/example-data/piano_roll.json').json()
zither_data = get('http://www.tide-pool.ca/pattern-recognition/example-data/zither.json').json()
circle_data = get('http://www.tide-pool.ca/pattern-recognition/example-data/circle.json').json()
large_grid_data = get('http://www.tide-pool.ca/pattern-recognition/example-data/large_grid.json').json()
classifier = create_classifier_from_data([(piano_data, 'piano'), 
                                        (xylophone_data, 'xylophone'),
                                        (small_grid_data, 'small_grid'),
                                        (piano_roll_data, 'piano_roll'),
                                        (zither_data, 'zither'),
                                        (circle_data, 'circle'),
                                        (large_grid_data, 'large_grid')
                                        ])


# Load test data
print "Loading test data.."
test_data = load_data_from_file('test_data')

# Translate and classify the test data
for example_data in test_data:
    translated_data = translate_data_to_scikit([example_data])
    print classifier.predict(translated_data)
   
