#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Test script for the classification data
'''

from requests import get

from classify import create_classifier
from classify import create_classifier_from_data
from classify import load_data_from_file
from classify import translate_data_to_scikit
from classify import pad_data


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

# Load test data
test_data = load_data_from_file('test_data')
test_data = translate_data_to_scikit(test_data)

# Pad, segment, and classify the test data
padded_test_data = []
for example_data in test_data:
    if len(example_data) <= small_max_length:
        example_data = pad_data(example_data, small_max_length)
        print small_classifier.predict([example_data])
    elif len(example_data) > 1000:
        example_data = pad_data(example_data, large_max_length)
        print large_classifier.predict([example_data])
