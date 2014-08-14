#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Classification tools.  
Functions from here will be invoked by the webserver,
in order to classify data.
'''

import json
import math
from sklearn import svm
from sklearn.neighbors.nearest_centroid import NearestCentroid

def get_mean(the_list):
    return sum(the_list) / float(len(the_list))


def get_standard_dev(the_list):
    mean = get_mean(the_list)
    squared_diffs = [(mean - num) ** 2 for num in the_list]
    standard_dev = get_mean(squared_diffs) ** 0.5
    return standard_dev


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

    # Fake radius if we don't have it
    if 'radius' not in button_data[0].keys():
        max_radius = 10
    else:
        # Define how fuzzy we can get
        max_radius = max([b['radius'] for b in button_data])
        max_radius = max_radius / 8

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

# This is the current favorite
def generate_features(button_data):
    # Sort
    button_data = sorted(button_data, key=lambda b: b['location']['x'])
    button_data = sorted(button_data, key=lambda b: b['location']['y'], reverse=True) 
    num_buttons = len(button_data)
    
    num_rows, num_cols = get_rows_and_cols(button_data)

    slope = get_slope(button_data)
    def line_eq(x):
        return slope * x + button_data[0]['location']['y']

    # mean and std dev from the line slope
    variences = []
    for button in button_data:
        rel_x = button['location']['x'] - button_data[0]['location']['x']
        varience = abs(line_eq(rel_x) - button['location']['y'])
        variences.append(varience)

    mean_varience = get_mean(variences)
    std_dev_varience = get_standard_dev(variences)

    # mean and std dev from the horiztonal center
    x_locs = [button['location']['x'] for button in button_data]
    mean_x = get_mean(x_locs)
    
    x_variences = []
    for x in x_locs:
        x_variences.append(abs(mean_x - x))

    mean_x_varience = get_mean(x_variences)
    std_dev_x_varience = get_standard_dev(x_variences)

    # [num_buttons, num_rows, num_cols, slope, mean_varience, std_dev_varience, mean_x_varience, std_dev_x_varience]
    return [num_buttons, num_rows, num_cols, 
            slope, mean_varience, std_dev_varience, 
            mean_x_varience, std_dev_x_varience]

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
def translate_data_to_scikit(data):
    all_data = []
    for raw_example in data:
        example_data = generate_features(raw_example) # select your magic here
        all_data.append(example_data)
    return all_data

def create_classifier_from_data(layout_list):
    collected_data = []
    collected_labels = []

    for data, category_name in layout_list:
        res = translate_data_to_scikit(data)
        collected_data.extend(res)
        collected_labels.extend([category_name] * len(res))

    classifier = svm.LinearSVC(tol=0.01) 
    # nuSVC works on all validation, but gives lousy results in practice
    # LinearSVC fails many validations, but feels better in practice
    classifier.fit(collected_data, collected_labels)
    return classifier
 