#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Test script for the classification data
'''

from classify import create_classifier
from classify import load_data_from_file
from classify import translate_data_to_scikit
from classify import pad_data

# Create pair of classifiers
small_classifier, small_max_length = create_classifier(['piano', 'small_grid', 'xylophone', 'piano_roll', 'zither'])
large_classifier, large_max_length = create_classifier(['big_piano', 'large_grid'])

# Load test data
test_data = load_data_from_file('test_data')
test_data = translate_data_to_scikit(test_data)

padded_test_data = []
for example_data in test_data:
    if len(example_data) <= small_max_length:
        example_data = pad_data(example_data, small_max_length)
        print small_classifier.predict([example_data])
    elif len(example_data) > 1000:
        example_data = pad_data(example_data, large_max_length)
        print large_classifier.predict([example_data])
