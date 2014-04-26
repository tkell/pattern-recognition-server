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

def load_data(category_name):
    category_data = load_data_from_file(category_name)
    res = translate_data_to_scikit(category_data)
    collected_data.extend(res)
    collected_labels.extend([category_name] * len(res))

# Load data
collected_data = []
collected_labels = []

load_data('piano')
load_data('small_grid')
load_data('xylophone')
load_data('piano_roll')
load_data('zither')


# Load test data
test_data = load_data_from_file('test_data')
test_data = translate_data_to_scikit(test_data)

## This pads the data - this maaay make things weird, but we'll see.
max_length = max([len(example) for example in collected_data])
test_max_length = max([len(example) for example in test_data])
max_length = max(max_length, test_max_length)

padded_training_data = []
for example_data in collected_data:
    padding_length = max_length - len(example_data)
    example_data.extend([0] * padding_length)
    padded_training_data.append(example_data)

padded_test_data = []
for example_data in test_data:
    padding_length = max_length - len(example_data)
    example_data.extend([0] * padding_length)
    padded_test_data.append(example_data)

# Create classifier
classifier = svm.SVC()
classifier.fit(padded_training_data, collected_labels)

# Test on own dataset
validation_errors = 0
print "Validation on training dataset..."
for index, data in enumerate(padded_training_data):
    if collected_labels[index] != classifier.predict([data]):
        validation_errors +=1
        print '%s VALIDATION ERROR:  %d %s' % (collected_labels[index], index, classifier.predict([data]))

if validation_errors != 0:
    print "There were %d validation_errors" % validation_errors
else:
    print "Validation passed" 

print '\n'

print "Testing on new examples..."
for data in padded_test_data:
    print classifier.predict([data])