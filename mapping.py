#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Mapping functions for each prototype, hidden behind map_as.
'''

import random
from math import atan2

# List of scales
chromatic = [1]
fifths = [7]
fourths = [5]

# Pentatonics.  I could use some more exciting things here
pentatonic_major = [2, 2, 3, 2, 3]
pentatonic_minor = [3, 2, 3, 2, 2]

# Hexatonics
hexatonic_dict = {'whole_tone': [2],
              'augmented': [3, 1],
              'prometheus' :[2, 2, 2, 3, 1, 2],
              'blues': [3, 2, 1, 1, 3, 2],
            }
hexatonics = [hexatonic_dict[k] for k in hexatonic_dict.keys()]


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

# Helper to find the 'best' scale from a list
def find_scale(button_length, list_of_scales):
    the_scale = None
    for scale in list_of_scales:
        if button_length % len(scale) == 0 or button_length % len(scale) == 1:
            the_scale = scale
            break

    if not the_scale:
        for scale in list_of_scales:
            if button_length % len(scale) == -1:
                the_scale = scale
                break
    
    if not the_scale:
        the_scale = chromatic

    return the_scale

# Helper to map an ordered set of buttons to a given scale from a starting point
def map_ordered(button_data, the_scale, note_number, same_octave=False):
    mapped_buttons = []
    
    first_button = button_data[0]
    first_button['noteFreq'] = midi_to_freq(note_number)
    first_button['noteMIDI'] = note_number
    mapped_buttons.append(first_button)

    for index, button in enumerate(button_data[1:]):
        scale_index = index % len(the_scale);
        note_number = note_number + the_scale[scale_index];

        if same_octave:
            note_number = note_number % 12 + first_button['noteMIDI']

        button['noteFreq'] = midi_to_freq(note_number)
        button['noteMIDI'] = note_number
        mapped_buttons.append(button)
    return mapped_buttons

def map_equal_tempered(button_data, note_number):
    mapped_buttons = []
    start_button = button_data[0]['location']
    temperment = float(len(button_data) - 1)
    base_freq = midi_to_freq(note_number)
    for index, button in enumerate(button_data):
        freq = base_freq * (2 ** (index / temperment))
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
def map_as(classification, button_data, adventure, increase_direction):
    if classification == 'piano' or classification == 'big_piano':
        return map_as_piano(button_data, adventure)
    if classification == 'xylophone':
        return map_as_xylo(button_data, adventure, increase_direction)
    if classification == 'piano_roll':
        return map_as_piano_roll(button_data, adventure)
    if classification == 'zither':
        return map_as_zither(button_data, adventure, increase_direction)
    if classification == 'small_grid':
        return map_as_small_grid(button_data, adventure)
    if classification == 'large_grid':
        return map_as_large_grid(button_data, adventure)
    if classification == 'circle':
        return map_as_circle(button_data, adventure)


# Piano:  a chromatic scale, from left to right
def map_as_piano(button_data, adventure):
    button_data = sorted(button_data, key=lambda b: b['location']['x'])
    if adventure < 4:
        mapped_buttons = map_ordered(button_data, chromatic, 60)
    if adventure == 4:
        mapped_buttons = map_by_ratio(button_data, 60)
    return mapped_buttons

# Xylophone
def map_as_xylo(button_data, adventure, increase_direction):
    if not increase_direction or increase_direction == 'negative':
        button_data = sorted(button_data, key=lambda b: b['location']['x'])
    elif increase_direction == 'positive':
        button_data = sorted(button_data, key=lambda b: b['location']['x'], reverse=True)

    # not sure if this is right
    elif increase_direction == 'kalimba':
        button_data = sorted(button_data, key=lambda b: b['location']['x'])
        button_data = sorted(button_data, key=lambda b: b['radius'], reverse=True)

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
        else:
            the_scale = find_scale(button_length, [diatonic_major, pentatonic_major, diatonic_both, diatonic_extra, chromatic])
        mapped_buttons = map_ordered(button_data, the_scale, 60)

    elif adventure == 2:
        if button_length <= 7: #hexatonics
            the_scale = random.choice(hexatonics)
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
        else:
            scale_list = [hexatonic_dict['blues'], octatonic_one, diatonic_both, diatonic_extra, chromatic]
            the_scale = find_scale(button_length, scale_list)

        mapped_buttons = map_ordered(button_data, the_scale, 60)

    elif adventure == 3:
        mapped_buttons = map_equal_tempered(button_data, 60)

    elif adventure == 4:
        mapped_buttons = map_by_ratio(button_data, 60)

    return mapped_buttons

# Piano roll:  a chromatic scale, from bottom to top
def map_as_piano_roll(button_data, adventure):
    button_data = sorted(button_data, key=lambda b: b['location']['y'], reverse=True)
    if adventure < 4:
        mapped_buttons = map_ordered(button_data, chromatic, 60)
    if adventure == 4:
        mapped_buttons = map_by_ratio(button_data, 60)
    return mapped_buttons

# Zither
def map_as_zither(button_data, adventure, increase_direction):
    # dodge for staff
    if increase_direction == 'staff' and adventure < 3:
        button_data = sorted(button_data, key=lambda b: b['location']['y'], reverse=True)
        offset_major = [1, 2, 2, 2, 1, 2, 2]
        mapped_buttons = map_ordered(button_data, offset_major, 64)
        return mapped_buttons

    if not increase_direction or increase_direction == 'positive':
        button_data = sorted(button_data, key=lambda b: b['location']['y'], reverse=True)
    elif increase_direction == 'negative':
        button_data = sorted(button_data, key=lambda b: b['location']['y'])
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
        else:
            the_scale = find_scale(button_length, [diatonic_major, pentatonic_major, chromatic])

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
        else:
            scale_list = [hexatonic_dict['blues'], octatonic_one, diatonic_both, diatonic_extra, chromatic]
            the_scale = find_scale(button_length, scale_list)
        mapped_buttons = map_ordered(button_data, the_scale, 60)

    elif adventure == 3:
        mapped_buttons = map_equal_tempered(button_data, 60)

    elif adventure == 4:
        mapped_buttons = map_by_ratio(button_data, 60)

    return mapped_buttons

def map_as_circle(button_data, adventure):
    # sort clockwise
    center_x = sum([b['location']['x'] for b in button_data]) / len(button_data)
    center_y = sum([b['location']['y'] for b in button_data]) / len(button_data)

    button_data = sorted(button_data, key=lambda b: atan2(b['location']['x'] - center_x, b['location']['y'] - center_y), reverse=True)
    button_length = len(button_data)

    if adventure == 0:
        the_scale = random.choice([fifths, fifths, pentatonic_major, diatonic_major])
        mapped_buttons = map_ordered(button_data, fifths, 60, same_octave=True)

    elif adventure == 1:
        if button_length <= 6:
            if random.random() > 0.5:
                the_scale = pentatonic_minor
            else:
                the_scale = pentatonic_major
        elif button_length <= 11:
            the_scale = random.choice([fifths, fifths, diatonic_major, diatonic_both])
        elif button_length >= 12:
            the_scale = random.choice([fifths, chromatic, diatonic_major, diatonic_extra])
        mapped_buttons = map_ordered(button_data, the_scale, 60, same_octave=True)

    elif adventure == 2:
        if button_length <= 7: #hexatonics
            the_scale = hexatonics[random.choice(hexatonics.keys())]
        elif button_length == 8 or button_length == 9: #octatonics
            the_scale = random.choice([fourths, octatonic_one, octatonic_two])
        elif button_length <= 11:
            the_scale = random.choice([fourths, diatonic_both, diatonic_extra, octatonic_one, octatonic_two])
        elif button_length >= 12:
            all_scales = hexatonics.extend([fourths, chromatic, diatonic_extra, octatonic_one, octatonic_two])
            the_scale = random.choice(all_scales)

        mapped_buttons = map_ordered(button_data, the_scale, 60)

    elif adventure == 3:
        mapped_buttons = map_equal_tempered(button_data, 60)

    elif adventure == 4:
        mapped_buttons = map_by_ratio(button_data, 60)

    return mapped_buttons

# Small grid:  conditionals, then bottom-left to top-right
def map_as_small_grid(button_data, adventure):
    # rows first, then columns
    button_data = sorted(button_data, key=lambda b: b['location']['x'])
    button_data = sorted(button_data, key=lambda b: b['location']['y'], reverse=True)
    button_length = len(button_data)

    if adventure == 0:
        if button_length <= 6:
            the_scale = pentatonic_major
        elif button_length == 7 or button_length == 8:
            the_scale = diatonic_major
        elif button_length == 9 or button_length == 10:
            the_scale = diatonic_both
        else:
            the_scale = diatonic_major
        mapped_buttons = map_ordered(button_data, the_scale, 60)

    elif adventure == 1:
        if button_length <= 6:
            if random.random() > 0.5:
                the_scale = pentatonic_minor
            else:
                the_scale = pentatonic_major
        elif button_length == 7 or button_length == 8:
            if random.random() > 0.5:
                the_scale = diatonic_minor
            else:
                the_scale = diatonic_major
        elif button_length == 9 or button_length == 10:
            the_scale = diatonic_both
        else:
            the_scale = find_scale(button_length, [diatonic_major, pentatonic_major, chromatic])
        mapped_buttons = map_ordered(button_data, the_scale, 60)

    elif adventure == 2:
        if button_length == 3 or button_length == 4:
            the_scale = trumpet
        elif button_length == 5:  
            the_scale = pentatonic_minor
        elif button_length == 6 or button_length == 7:
            the_scale = hexatonics[random.choice(hexatonics.keys())]
        elif button_length == 8 or button_length == 9:
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
        else:
            scale_list = [hexatonic_dict['blues'], octatonic_one, diatonic_both, diatonic_extra, chromatic]
            the_scale = find_scale(button_length, scale_list)

        mapped_buttons = map_ordered(button_data, the_scale, 60)

    elif adventure == 3:
        mapped_buttons = map_equal_tempered(button_data, 60)

    elif adventure == 4:
        mapped_buttons = map_by_ratio(button_data, 60)

    return mapped_buttons


def map_as_large_grid(button_data, adventure):

    print "in map as large_grid"
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
    num_rows = len(rows)
    num_cols = len(cols)


    # Figure out if we have more columns or rows.
    # This determines where we put the scales, and where we put the leaps
    if num_cols >= num_rows:
        large_dimension = num_cols
        short_dimension = num_rows
    else:
        large_dimension = num_rows
        short_dimension = num_cols

    print large_dimension, short_dimension

    if short_dimension == 2:
        short_dimension_interval = 7
    elif short_dimension == 3:
        short_dimension_interval = 5
    elif short_dimension == 4:
        short_dimension_interval = 4
    elif short_dimension == 5:
        short_dimension_interval = 3
    elif short_dimension >= 6:
        short_dimension_interval = 2

    # Set the scale
    if adventure == 0:
        if large_dimension == 3 or large_dimension == 4:
            the_scale = trumpet
        elif large_dimension == 5 or large_dimension == 6:
            the_scale = pentatonic_major
        elif large_dimension == 7 or large_dimension == 8:
            the_scale = diatonic_major
        elif large_dimension == 9 or large_dimension == 10:
            the_scale = diatonic_both
        elif large_dimension == 11:
            the_scale = diatonic_extra
        elif large_dimension == 12 or large_dimension == 13:
            the_scale = chromatic
        else:
            the_scale = find_scale(large_dimension, [diatonic_major, pentatonic_major, chromatic])

    if adventure == 1:
        if large_dimension == 3 or large_dimension == 4:
            the_scale = trumpet
        elif large_dimension == 5 or large_dimension == 6:
            if random.random() > 0.5:
                the_scale = pentatonic_minor
            else:
                the_scale = pentatonic_major
        elif large_dimension == 7 or large_dimension == 8:
            if random.random() > 0.5:
                the_scale = diatonic_minor
            else:
                the_scale = diatonic_major
        elif large_dimension == 9 or large_dimension == 10:
            the_scale = diatonic_both
        elif large_dimension == 11:
            the_scale = diatonic_extra
        elif large_dimension == 12 or large_dimension == 13:
            the_scale = chromatic
        else:
            the_scale = find_scale(large_dimension, [diatonic_minor, pentatonic_minor, chromatic])

    if adventure == 2:
        if large_dimension == 3 or large_dimension == 4:
            the_scale = trumpet
        elif large_dimension == 5:
            the_scale = pentatonic_minor
        elif large_dimension == 6 or large_dimension == 7:
            the_scale = hexatonics[random.choice(hexatonics.keys())]
        elif large_dimension == 8 or large_dimension == 9:
            if random.random() > 0.5:
                the_scale = octatonic_one
            else:
                the_scale = octatonic_two
        elif large_dimension == 10:
             the_scale = diatonic_both
        elif large_dimension == 11:
            the_scale = diatonic_extra
        elif large_dimension == 12 or large_dimension == 13:
            the_scale = chromatic
        else: 
            scale_list = [hexatonic_dict['blues'], octatonic_one, diatonic_both, diatonic_extra, chromatic]
            the_scale = find_scale(large_dimension, scale_list)

    elif adventure == 3:
        mapped_buttons = map_equal_tempered(button_data, 60)

    elif adventure == 4:
        return map_by_ratio(button_data, 60)

    # Lower notes for bigger grids
    if len(button_data) < 24:
        base_note_number = 60
    elif len(button_data) < 48:
        base_note_number = 48
    else:
        base_note_number = 36

    mapped_buttons = []
    for i in range(short_dimension):
        starting_index = i * large_dimension
        ending_index = (i + 1) * large_dimension
        note_number = base_note_number + short_dimension_interval * i

        if adventure < 3:
            mapped_row = map_ordered(button_data[starting_index:ending_index], the_scale, note_number)
            mapped_buttons.extend(mapped_row)
        if adventure == 3:
            mapped_row = map_equal_tempered(button_data[starting_index:ending_index], note_number)
            mapped_buttons.extend(mapped_row)

    return mapped_buttons