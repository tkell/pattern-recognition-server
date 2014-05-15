#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Mapping functions for each prototype, hidden behind map_as.
'''

import random

# List of scales
chromatic = [1];

# Pentatonics
pentatonic_major = [2, 2, 3, 2, 3]

# Hexatonics
hexatonics = {'whole_tone': [2],
              'augmented': [3, 1],
              'prometheus' :[2, 2, 2, 3, 1, 2],
              'blues': [3, 2, 1, 1, 3, 2],
            }

# Octatonics
octatonic_one = [2, 1]
octatonic_two = [1, 2]

# Diatonics
diatonic_major = [2, 2, 1, 2, 2, 2, 1]
diatonic_minor = [2, 1, 2, 2, 1, 2, 2]
diatonic_both = [2, 1, 1, 1, 2, 2, 1, 1, 1] # has flat 3 and flat 7
diatonic_extra = [2, 1, 1, 1, 2, 1, 1, 1, 1, 1] # has flat 3, flat 6, and  flat 7

# Odd
trumpet = [1, 1, 1]


def midi_to_freq(midi_number):
    return 440 * (2 ** ((midi_number - 69) / 12.0))

# Help to map an ordered set of buttons to a given scale from a starting point
def map_ordered(button_data, the_scale, note_number):
    mapped_buttons = []
    first_button = button_data[0]
    first_button['noteFreq'] = midi_to_freq(note_number)
    mapped_buttons.append(first_button)
    for index, button in enumerate(button_data[1:]):
        scale_index = index % len(the_scale);
        note_number = note_number + the_scale[scale_index];
        button['noteFreq'] = midi_to_freq(note_number)
        button['noteMIDI'] = note_number
        mapped_buttons.append(button)
    return mapped_buttons

def map_equal_tempered(button_data, note_number):
    mapped_buttons = []
    start_button = button_data[0]['location']
    base_freq = midi_to_freq(note_number)
    for index, button in enumerate(button_data):
        freq = base_freq * (2 ** (index / len(button_data)))
        button['noteFreq'] = freq
        mapped_buttons.append(button)

    return mapped_buttons

def map_by_ratio(button_data, note_number):
    mapped_buttons = []
    start_button = button_data[0]['location']
    base_freq = midi_to_freq(note_number)

    max_distance = 0
    for button in button_data:
        distance = ((start_button['x'] - button['location']['x']) ** 2 + (start_button['y'] - button['location']['y']) ** 2) ** 0.5
        if distance > max_distance:
            max_distance = distance

    for button in button_data:
        distance = ((start_button['x'] - button['location']['x']) ** 2 + (start_button['y'] - button['location']['y']) ** 2) ** 0.5
        ratio = distance / float(max_distance) + 1
        freq = base_freq * ratio
        button['noteFreq'] = freq
        mapped_buttons.append(button)

    return mapped_buttons


# Master mapping function
def map_as(classification, button_data, adventure):
    if classification == 'piano' or classification == 'big_piano':
        return map_as_piano(button_data, adventure)
    if classification == 'xylophone':
        return map_as_xylo(button_data, adventure)
    if classification == 'piano_roll':
        return map_as_piano_roll(button_data, adventure)
    if classification == 'zither':
        return map_as_zither(button_data, adventure)
    if classification == 'small_grid':
        return map_as_small_grid(button_data, adventure)
    if classification == 'large_grid':
        return map_as_large_grid(button_data, adventure)


# Piano:  a chromatic scale, from left to right
def map_as_piano(button_data, adventure):
    button_data = sorted(button_data, key=lambda b: b['location']['x'])
    if adventure < 4:
        mapped_buttons = map_ordered(button_data, chromatic, 60)
    if adventure == 4:
        mapped_buttons = map_by_ratio(button_data, 60)
    return mapped_buttons

# Xylophone
def map_as_xylo(button_data, adventure):
    button_data = sorted(button_data, key=lambda b: b['location']['x'])
    button_length = len(button_data)

    if adventure == 0:
        mapped_buttons = map_ordered(button_data, diatonic_major, 60)
    elif adventure == 1:
        if button_length <= 8:
            if random.random() > 0.5:
                the_scale = diatonic_minor
            else:
                the_scale = diatonic_major
        elif button_length == 9 or button_length == 10:
            the_scale = diatonic_both
        elif button_length == 11:
            the_scale = diatonic_extra
        elif button_length == 12 or button_length == 13:
            the_scale = chromatic
        mapped_buttons = map_ordered(button_data, the_scale, 60)

    elif adventure == 2:
        if button_length == 7: #hexatonics
            the_scale = hexatonics[random.choice(hexatonics.keys())]
        elif button_length == 8 or button_length == 9: #octatonics
            if random.random() > 0.5:
                the_scale = octatonic_one
            else:
                the_scale = octatonic_two
        elif button_length == 10:
            the_scale = diatonic_both
        elif button_length == 11:
            the_scale = diatonic_extra
        elif button_length == 12 or button_length == 13:
            the_scale = chromatic
        mapped_buttons = map_ordered(button_data, the_scale, 60)

    elif adventure == 3:
        map_equal_tempered(button_data, 60)

    elif adventure == 4:
        mapped_buttons = map_by_ratio(button_data, 60)

    return mapped_buttons

# Piano roll:  a chromatic scale, from bottom to top
def map_as_piano_roll(button_data, adventure):
    button_data = sorted(button_data, key=lambda b: b['location']['y'], reverse=True)
    mapped_buttons = map_ordered(button_data, chromatic, 60)
    return mapped_buttons

# Zither:  a diatonic major scale, from bottom to top
def map_as_zither(button_data, adventure):
    button_data = sorted(button_data, key=lambda b: b['location']['y'], reverse=True)
    mapped_buttons = map_ordered(button_data, diatonic_major, 60)
    return mapped_buttons

# Small grid:  conditionals, then bottom-left to top-roight
def map_as_small_grid(button_data, adventure):
    # rows first, then columns
    button_data = sorted(button_data, key=lambda b: b['location']['x'])
    button_data = sorted(button_data, key=lambda b: b['location']['y'], reverse=True)
    if len(button_data) == 9 or len(button_data) == 10:
        the_scale = diatonic_both
    elif len(button_data) == 7 or len(button_data) == 8:
        the_scale = diatonic_major
    elif len(button_data) == 5 or len(button_data) == 6:
        the_scale = pentatonic_major
    elif len(button_data) == 3 or len(button_data) == 4:
        the_scale = trumpet

    mapped_buttons = map_ordered(button_data, the_scale, 60)
    return mapped_buttons


# Large grid:  needs work!
def map_as_large_grid(button_data, adventure):
    # rows first, then columns
    button_data = sorted(button_data, key=lambda b: b['location']['x'])
    button_data = sorted(button_data, key=lambda b: b['location']['y'], reverse=True)

    # Get the number of rows and columns
    rows = []
    cols = [] 
    for button in button_data:
        if button['location']['y'] not in rows:
            rows.append(button['location']['y'])
        if button['location']['x'] not in cols:
            cols.append(button['location']['x'])

    column_interval = 5  # will need to update this

    if len(cols) == 9 or len(cols) == 10:
        the_scale = diatonic_both
    elif len(cols) == 7 or len(cols) == 8:
        the_scale = diatonic_major
    elif len(cols) == 5 or len(cols) == 6:
        the_scale = pentatonic_major
    else:
        the_scale = chromatic

    mapped_buttons = []
    base_note_number = 60
    for i in range(len(rows)):
        starting_index = i * len(cols)
        ending_index = (i + 1) * len(cols)
        note_number = base_note_number + column_interval * i
        mapped_row = map_ordered(button_data[starting_index:ending_index], the_scale, note_number)
        mapped_buttons.extend(mapped_row)
    return mapped_buttons