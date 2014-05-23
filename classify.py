#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Classification tools.  
Functions from here will be invoked by the webserver,
in order to classify data.
'''

import json
from sklearn import svm
from sklearn.neighbors.nearest_centroid import NearestCentroid

# Load data from a file
def load_data_from_file(classification):
    data = []
    file_path = 'example_data/%s.json' % classification
    with open(file_path, 'r') as f:
        for line in f:
            data = json.loads(line)
    return data

# Find the maximium distance for a set of button data
def find_max_distance(button_data):
    max_distance = 0 
    max_x = 0
    max_y = 0
    
    for i, button in enumerate(button_data):
        for j, other_button in enumerate(button_data):
            x_distance = button_data[i]['location']['x'] - button_data[j]['location']['x']
            y_distance = button_data[i]['location']['y'] - button_data[j]['location']['y']
            if max_x < abs(x_distance):
                max_x = x_distance
            if max_y < abs(y_distance):
                max_y = y_distance

    return max(max_x, max_y), max_x, max_y

# This is me flailing around trying to find a dimensionally consistant feature set
# Not going so well.
def generate_features(button_data):
    # Sort
    button_data = sorted(button_data, key=lambda b: b['location']['x'])
    button_data = sorted(button_data, key=lambda b: b['location']['y'], reverse=True)

    # number of buttons, mean x / y, x_max, y_max, num_rows, num_cols, 
    num_buttons = len(button_data)

    # Mean distances, from linear button steps
    x_dists = []
    y_dists = []
    for i, button in enumerate(button_data[0:-1]):
        x_dists.append(button_data[i]['location']['x'] - button_data[i + 1]['location']['x'])
        y_dists.append(button_data[i]['location']['y'] - button_data[i + 1]['location']['y'])
    x_mean = sum(x_dists) / float(len(x_dists))
    y_mean = sum(y_dists) / float(len(y_dists))

    max_distance, max_x, max_y = find_max_distance(button_data)

    x_mean = x_mean / float(max_distance)
    y_mean = y_mean / float(max_distance)

    return [num_buttons, x_mean, y_mean, max_x, max_y]


# This one returns the normalized distances with no repetition
# So it is not 1 to all, 2 to all, but 1 to all, 2 to all but 1, etc
# We also pad with zeros in the right places!
def subtract_data_better(button_data, max_button_length):
    # First we sort.
    button_data = sorted(button_data, key=lambda b: b['location']['x'])
    button_data = sorted(button_data, key=lambda b: b['location']['y'], reverse=True)

    # Then we find the max distance
    max_distance, max_x, max_y = find_max_distance(button_data)

    # We actually do the subtraction
    distances = []
    for index, button in enumerate(button_data):
        for other_button in button_data[index + 1:]:
            x_distance = button['location']['x'] - other_button['location']['x']
            y_distance = button['location']['y'] - other_button['location']['y']

            distances.append(x_distance)
            distances.append(y_distance)

        # This bit pads things in place, as it were, 
        # rather than stacking all the zeros at the end, 
        # and screwing the indicies up
        if len(button_data) < max_button_length:
            distances.extend([0] * (2 * (max_button_length - len(button_data))))

    # Final padding
    if len(button_data) < max_button_length:
        final_padding_count = max_button_length * (max_button_length - 1) - len(distances)
        distances.extend([0] * final_padding_count)

    # Divide it out
    distances = [d / float(max_distance) for d in distances]

    return distances


# Translate giant dict / json to scikit-style giant list
def translate_data_to_scikit(data, max_button_length):
    all_data = []
    for raw_example in data:
        example_data = subtract_data_better(raw_example, max_button_length) # new magic!
        all_data.append(example_data)
    return all_data

def create_classifier_from_data(layout_list):
    collected_data = []
    collected_labels = []

    max_example_button_length = 0
    for data, category_name in layout_list:
        for example in data:
            if max_example_button_length < len(example):
                max_example_button_length = len(example)

    for data, category_name in layout_list:
        res = translate_data_to_scikit(data, max_example_button_length)
        collected_data.extend(res)
        collected_labels.extend([category_name] * len(res))

    classifier = NearestCentroid()
    classifier.fit(collected_data, collected_labels)

    # Validate on training dataset
    validation_errors = 0
    for index, data in enumerate(collected_data):
        if collected_labels[index] != classifier.predict([data]):
            validation_errors +=1
            print '%s VALIDATION ERROR:  %d %s' % (collected_labels[index], index, classifier.predict([data]))

    if validation_errors != 0:
        print "PANIC!  There were %d validation_errors" % validation_errors

    return classifier, max_example_button_length
 