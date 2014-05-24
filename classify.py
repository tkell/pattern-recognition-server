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

def get_slope(button_data):
    y_dist = button_data[0]['location']['y'] - button_data[-1]['location']['y']
    x_dist = button_data[0]['location']['x'] - button_data[-1]['location']['x']
    
    if x_dist == 0:
        x_dist = 1
    return y_dist / float(x_dist)


def get_rows_and_cols(button_data):
    rows = []
    cols = []

    # Define how fuzzy we can get
    max_radius = max([b['radius'] for b in button_data])
    max_radius = max_radius / 2

    rows.append(button_data[0]['location']['y'])
    cols.append(button_data[0]['location']['x'])

    for button in button_data[1:]:

        for row in rows:
            if button['location']['y'] > row - max_radius and button['location']['y'] < row + max_radius:
                rows.append(button['location']['y'])
                break
        for col in cols:
            if button['location']['x'] > col - max_radius and button['location']['x'] < col + max_radius:
                cols.append(button['location']['x'])
                break

    num_rows = len(rows)
    num_cols = len(cols)
    return num_rows, num_cols

# HMM.
def generate_features(button_data):
    # Sort
    button_data = sorted(button_data, key=lambda b: b['location']['x'])
    button_data = sorted(button_data, key=lambda b: b['location']['y'], reverse=True) 
    num_buttons = len(button_data)
    
    num_rows, num_cols = get_rows_and_cols(button_data)
    max_dist, max_x, max_y = find_max_distance(button_data)

    slope = get_slope(button_data)
    
    def line_eq(x):
        return slope * x + button_data[0]['location']['y']

    total_varience = 0
    for button in button_data:
        rel_x = button['location']['x'] - button_data[0]['location']['x']
        varience = abs(line_eq(rel_x) - button['location']['y'])
        total_varience = total_varience + varience / float(max_dist)
    mean_varience = total_varience / float(len(button_data))

    return [num_buttons, num_rows, num_cols, slope, mean_varience]

# This one returns the normalized distances with better padding
def generate_distance_features(button_data, max_button_length):
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
        example_data = generate_features(raw_example) # select your magic here
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

    classifier = svm.LinearSVC()
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
 