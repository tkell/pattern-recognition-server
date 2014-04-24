#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

'''
Classification tools.  Functions from here will be invoked by the webserver
in order to classify data.
'''

def load_data_from_file(classification):
    data = []
    file_path = 'example_data/%s.json' % classification
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data