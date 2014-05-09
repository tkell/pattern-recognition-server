#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Mapping functions for each prototype, hidden behind map_as.
'''

# List of scales
chromatic_scale = [1];

def map_ordered(button_data, the_scale, note_number):
    mapped_buttons = []
    for index, button in enumerate(button_data):
        scale_index = index % the_scale.length;
        note_number = note_number + the_scale[scale_index];
        button['noteNumber'] = note_number
        mapped_buttons.append(button)
    return mapped_buttons

# Master mapping function
def map_as(classification, button_data):
    if classification == 'piano':
        return map_as_piano(button_data)

# Piano:  a chromatic scale, from left to right
def map_as_piano(button_data):
    button_data = sorted(button_data, key=lambda b: b['location']['x'])
    mapped_buttons = map_ordered(button_data, chromatic_scale, 60)

    return mapped_buttons
