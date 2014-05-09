#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Mapping functions for each prototype, hidden behind map_as.
'''

# List of scales
chromatic = [1];
pentatonic = [2, 2, 3, 2, 3];
diatonic_major = [2, 2, 1, 2, 2, 2, 1];
diatonic_minor = [2, 1, 2, 2, 1, 2, 2];
diatonic_both = [2, 1, 1, 1, 2, 2, 1, 1]; # has flat 3 and flat 7
trumpetScale = [1, 1, 1];

# Help to map an ordered set of buttons to a given scale from a starting point
def map_ordered(button_data, the_scale, note_number):
    mapped_buttons = []
    first_button = button_data[0]
    first_button['noteNumber'] = note_number
    mapped_buttons.append(first_button)
    for index, button in enumerate(button_data[1:]):
        scale_index = index % len(the_scale);
        note_number = note_number + the_scale[scale_index];
        button['noteNumber'] = note_number
        mapped_buttons.append(button)
    return mapped_buttons

# Master mapping function
def map_as(classification, button_data):
    if classification == 'piano':
        return map_as_piano(button_data)
    if classification == 'xylophone':
        return map_as_xylo(button_data)
    if classification == 'piano_roll':
        return map_as_piano(button_data)
    if classification == 'zither':
        return map_as_xylo(button_data)

# Piano:  a chromatic scale, from left to right
def map_as_piano(button_data):
    button_data = sorted(button_data, key=lambda b: b['location']['x'])
    mapped_buttons = map_ordered(button_data, chromatic, 60)
    return mapped_buttons

# Xylophone:  a diatonic major scale, from left to right
def map_as_xylo(button_data):
    button_data = sorted(button_data, key=lambda b: b['location']['x'])
    mapped_buttons = map_ordered(button_data, diatonic_major, 60)
    return mapped_buttons

# Piano roll:  a chromatic scale, from bottom to top
def map_as_piano_roll(button_data):
    button_data = sorted(button_data, key=lambda b: b['location']['y'])
    mapped_buttons = map_ordered(button_data, chromatic, 60)
    return mapped_buttons

# Zither:  a diatonic major scale, from bottom to top
def map_as_piano_roll(button_data):
    button_data = sorted(button_data, key=lambda b: b['location']['y'])
    mapped_buttons = map_ordered(button_data, diatonic_major, 60)
    return mapped_buttons