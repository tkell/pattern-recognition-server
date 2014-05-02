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
            data.append(json.loads(line))
    return data

# Translate giant dict / json to scikit-style giant list
# The use of sorted() here scares me a little.
# If I am consistant with it, it should not be a problem, 
# but if I am not, I am going to ruin a ton of shit.
def translate_data_to_scikit(data):
    all_data = []
    for example in data:
        example_data = []
        buttons = sorted(example.keys())
        for button in buttons:
            other_buttons = sorted(example[button].keys())
            for other_button in other_buttons:
                difference_dict = example[button][other_button]
                difference_keys = sorted(difference_dict.keys())
                for difference_key in difference_keys:
                    data_point = difference_dict[difference_key]
                    # translate from True / False to 1 / 0
                    if difference_key == 'shape':
                        data_point = int(data_point)
                        example_data.append(data_point)
                    # translate from location dict to two entries
                    elif difference_key == 'location':
                        example_data.append(data_point['x'])
                        example_data.append(data_point['y'])
                    # default
                    else:
                         example_data.append(data_point)
        all_data.append(example_data)
    return all_data

def load_data(category_name, collected_data, collected_labels):
    category_data = load_data_from_file(category_name)
    res = translate_data_to_scikit(category_data)
    collected_data.extend(res)
    collected_labels.extend([category_name] * len(res))

    return collected_data, collected_labels

def pad_data(example_data, target_length):
    padding_length = target_length - len(example_data)
    example_data.extend([0] * padding_length)
    return example_data

def create_classifier(layout_list):
    collected_data = []
    collected_labels = []
    for layout in layout_list:
        load_data(layout, collected_data, collected_labels)

    max_length = max([len(example) for example in collected_data])

    padded_training_data = []
    for example_data in collected_data:
        padding_length = max_length - len(example_data)
        example_data.extend([0] * padding_length)
        padded_training_data.append(example_data)

    classifier = NearestCentroid()
    classifier.fit(padded_training_data, collected_labels)

    # Validate on training dataset
    validation_errors = 0
    for index, data in enumerate(padded_training_data):
        if collected_labels[index] != classifier.predict([data]):
            validation_errors +=1
            print '%s VALIDATION ERROR:  %d %s' % (collected_labels[index], index, classifier.predict([data]))

    if validation_errors != 0:
        print "PANIC!  There were %d validation_errors" % validation_errors

    return classifier, max_length
