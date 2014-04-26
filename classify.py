#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from sklearn import svm

'''
Classification tools.  Functions from here will be invoked by the webserver
in order to classify data.
'''

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

# Load raw data
piano_data = load_data_from_file('piano')
small_grid_data = load_data_from_file('small_grid')
xylophone_data = load_data_from_file('xylophone')
piano_roll_data = load_data_from_file('piano_roll')

# Begin translation
collected_data = []
collected_labels = []

# Translate piano data
res = translate_data_to_scikit(piano_data)
collected_data.extend(res)
collected_labels.extend(['piano'] * len(res))

# Translate small grid data
res = translate_data_to_scikit(small_grid_data)
collected_data.extend(res)
collected_labels.extend(['small grid'] * len(res))

# Translate xylophone data
res = translate_data_to_scikit(xylophone_data)
collected_data.extend(res)
collected_labels.extend(['xylophone'] * len(res))

# Translate piano roll data
res = translate_data_to_scikit(piano_roll_data)
collected_data.extend(res)
collected_labels.extend(['piano roll'] * len(res))

## This pads the data - this maaay make things weird, but we'll see.
max_length = max([len(example) for example in collected_data])
padded_data = []
for example_data in collected_data:
    padding_length = max_length - len(example_data)
    example_data.extend([0] * padding_length)
    padded_data.append(example_data)

# Create classifier
classifier = svm.SVC()
classifier.fit(collected_data, collected_labels)

# Test on own dataset
print "Validation on training dataset"
for index, data in enumerate(padded_data):
    print collected_labels[index], classifier.predict([data])

# Load test data
test_data = load_data_from_file('test_data')
test_data = translate_data_to_scikit(test_data)
padded_test_data = []
for example_data in test_data:
    padding_length = max_length - len(example_data)
    example_data.extend([0] * padding_length)
    padded_test_data.append(example_data)

print "Test on new examples"
for data in padded_test_data:
    print classifier.predict([data])