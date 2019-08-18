import json
import random
from math import atan2
from collections import OrderedDict


# Tree classifier -----------------------
# unsure if the formatting is right!
def get_classification(data):
    num_buttons = data[0]
    num_rows = data[1]
    num_cols = data[2]
    slope = data[3]
    mean_var = data[4]
    std_dev_var = data[5]
    mean_x_var = data[6]
    std_dev_x_var = data[7]

    if num_rows <= 1.5:
        if mean_var <= 0.21650634706020355:
            return 'xylophone'
        else:  # if mean_var > 0.21650634706020355
            return 'circle'
    else:  # if num_rows > 1.5
        if num_cols <= 13.5:
            if num_cols <= 2.0:
                if num_buttons <= 6.5:
                    if std_dev_x_var <= 0.07486573606729507:
                        return 'small_grid'
                    else:  # if std_dev_x_var > 0.07486573606729507
                        return 'circle'
                else:  # if num_buttons > 6.5
                    if mean_x_var <= 0.16608050651848316:
                        return 'zither'
                    else:  # if mean_x_var > 0.16608050651848316
                        return 'circle'
            else:  # if num_cols > 2.0
                if std_dev_var <= 0.5679819285869598:
                    if std_dev_var <= 0.10309640690684319:
                        if num_rows <= 6.5:
                            if mean_x_var <= 0.31577572226524353:
                                return 'piano'
                            else:  # if mean_x_var > 0.31577572226524353
                                return 'small_grid'
                        else:  # if num_rows > 6.5
                            return 'small_grid'
                    else:  # if std_dev_var > 0.10309640690684319
                        if mean_x_var <= 0.30158163607120514:
                            if std_dev_var <= 0.10598976537585258:
                                return 'piano'
                            else:  # if std_dev_var > 0.10598976537585258
                                return 'small_grid'
                        else:  # if mean_x_var > 0.30158163607120514
                            if mean_var <= 0.3213394209742546:
                                return 'small_grid'
                            else:  # if mean_var > 0.3213394209742546
                                return 'circle'
                else:  # if std_dev_var > 0.5679819285869598
                    return 'piano_roll'
        else:  # if num_cols > 13.5
            if mean_var <= 0.5047118216753006:
                if mean_x_var <= 0.17323721945285797:
                    if num_rows <= 25.5:
                        if std_dev_var <= 0.3435194343328476:
                            if slope <= -1.6445452570915222:
                                if num_buttons <= 24.5:
                                    return 'large_grid'
                                else:  # if num_buttons > 24.5
                                    if num_buttons <= 26.5:
                                        return 'tonnetz'
                                    else:  # if num_buttons > 26.5
                                        return 'large_grid'
                            else:  # if slope > -1.6445452570915222
                                if slope <= -1.5641443729400635:
                                    return 'tonnetz'
                                else:  # if slope > -1.5641443729400635
                                    return 'large_grid'
                        else:  # if std_dev_var > 0.3435194343328476
                            return 'tonnetz'
                    else:  # if num_rows > 25.5
                        if mean_var <= 0.3418903797864914:
                            return 'large_grid'
                        else:  # if mean_var > 0.3418903797864914
                            return 'tonnetz'
                else:  # if mean_x_var > 0.17323721945285797
                    if mean_var <= 0.26044249534606934:
                        if std_dev_x_var <= 0.16096936911344528:
                            if num_rows <= 40.5:
                                return 'large_grid'
                            else:  # if num_rows > 40.5
                                return 'tonnetz'
                        else:  # if std_dev_x_var > 0.16096936911344528
                            return 'tonnetz'
                    else:  # if mean_var > 0.26044249534606934
                        if std_dev_x_var <= 0.10907256975769997:
                            if mean_var <= 0.36868488788604736:
                                if num_rows <= 39.0:
                                    return 'large_grid'
                                else:  # if num_rows > 39.0
                                    return 'tonnetz'
                            else:  # if mean_var > 0.36868488788604736
                                if mean_x_var <= 0.2271130010485649:
                                    return 'tonnetz'
                                else:  # if mean_x_var > 0.2271130010485649
                                    return 'large_grid'
                        else:  # if std_dev_x_var > 0.10907256975769997
                            if mean_var <= 0.3034055233001709:
                                if std_dev_x_var <= 0.13167573511600494:
                                    return 'large_grid'
                                else:  # if std_dev_x_var > 0.13167573511600494
                                    return 'tonnetz'
                            else:  # if mean_var > 0.3034055233001709
                                if num_buttons <= 15.5:
                                    return 'large_grid'
                                else:  # if num_buttons > 15.5
                                    if slope <= -1.5788135528564453:
                                        return 'large_grid'
                                    else:  # if slope > -1.5788135528564453
                                        if std_dev_x_var <= 0.11206164956092834:
                                            if slope <= -1.2089494466781616:
                                                return 'tonnetz'
                                            else:  # if slope > -1.2089494466781616
                                                return 'large_grid'
                                        else:  # if std_dev_x_var > 0.11206164956092834
                                            if slope <= -1.3813077211380005:
                                                if mean_var <= 0.36789606511592865:
                                                    return 'large_grid'
                                                else:  # if mean_var > 0.36789606511592865
                                                    return 'tonnetz'
                                            else:  # if slope > -1.3813077211380005
                                                return 'tonnetz'
            else:  # if mean_var > 0.5047118216753006
                return 'circle'


# Mapping scales and functions -------------

# List of scales
chromatic = [1]
fifths = [7]
fourths = [5]
minor_thirds = [3]
major_seconds = [2]

# Pentatonics.  I could use some more exciting things here
pentatonic_major = [2, 2, 3, 2, 3]
pentatonic_minor = [3, 2, 3, 2, 2]

# Hexatonics
hexatonic_dict = {
    'whole_tone': [2],
    'augmented': [3, 1],
    'prometheus': [2, 2, 2, 3, 1, 2],
    'blues': [3, 2, 1, 1, 3, 2],
}
hexatonics = [hexatonic_dict[k] for k in hexatonic_dict.keys()]


# Octatonics
octatonic_one = [2, 1]
octatonic_two = [1, 2]

# Diatonics
diatonic_major = [2, 2, 1, 2, 2, 2, 1]
diatonic_minor = [2, 1, 2, 2, 1, 2, 2]
diatonic_both = [2, 1, 1, 1, 2, 2, 1, 1, 1]  # has flat 3 and flat 7
diatonic_extra = [2, 1, 1, 1, 2, 1, 1, 1, 1, 1]  # has flat 3, flat 6, and  flat 7

# Odd
trumpet = [1, 1, 1]


def mapping_from_classification(classification, button_data, adventure, modifier):
    mapped_buttons = map_as(classification, button_data, adventure, modifier)
    return mapped_buttons


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
        scale_index = index % len(the_scale)
        note_number = note_number + the_scale[scale_index]

        if same_octave:
            note_number = note_number % 12 + first_button['noteMIDI']

        button['noteFreq'] = midi_to_freq(note_number)
        button['noteMIDI'] = note_number
        mapped_buttons.append(button)
    return mapped_buttons


def map_equal_tempered(button_data, note_number):
    mapped_buttons = []
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
        distance = (
            (start_button['x'] - button['location']['x']) ** 2
            + (start_button['y'] - button['location']['y']) ** 2
        ) ** 0.5
        if distance > max_distance:
            max_distance = distance

    for button in button_data:
        distance = (
            (start_button['x'] - button['location']['x']) ** 2
            + (start_button['y'] - button['location']['y']) ** 2
        ) ** 0.5
        ratio = distance / float(max_distance) + 1
        freq = base_freq * ratio
        button['noteFreq'] = freq
        mapped_buttons.append(button)

    return mapped_buttons


# Master mapping function
def map_as(classification, button_data, adventure, modifier):
    if classification == 'piano' or classification == 'big_piano':
        return map_as_piano(button_data, adventure)
    if classification == 'xylophone':
        return map_as_xylo(button_data, adventure, modifier)
    if classification == 'piano_roll':
        return map_as_piano_roll(button_data, adventure)
    if classification == 'zither':
        return map_as_zither(button_data, adventure, modifier)
    if classification == 'small_grid':
        return map_as_small_grid(button_data, adventure)
    if classification == 'large_grid':
        return map_as_large_grid(button_data, adventure)
    if classification == 'tonnetz':
        return map_as_tonnetz(button_data, adventure)
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
def map_as_xylo(button_data, adventure, modifier):
    if not modifier or modifier == 'negative':
        button_data = sorted(button_data, key=lambda b: b['location']['x'])
    elif modifier == 'positive':
        button_data = sorted(
            button_data, key=lambda b: b['location']['x'], reverse=True
        )

    elif modifier == 'kalimba':
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
            the_scale = find_scale(
                button_length,
                [
                    diatonic_major,
                    pentatonic_major,
                    diatonic_both,
                    diatonic_extra,
                    chromatic,
                ],
            )
        mapped_buttons = map_ordered(button_data, the_scale, 60)

    elif adventure == 2:
        if button_length <= 7:  # hexatonics
            the_scale = random.choice(hexatonics)
        elif button_length == 8 or button_length == 9:  # octatonics
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
            scale_list = [
                hexatonic_dict['blues'],
                octatonic_one,
                diatonic_both,
                diatonic_extra,
                chromatic,
            ]
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
def map_as_zither(button_data, adventure, modifier):
    # dodge for staff
    if modifier == 'staff' and adventure < 3:
        button_data = sorted(
            button_data, key=lambda b: b['location']['y'], reverse=True
        )
        offset_major = [1, 2, 2, 2, 1, 2, 2]
        mapped_buttons = map_ordered(button_data, offset_major, 64)
        return mapped_buttons

    if not modifier or modifier == 'positive':
        button_data = sorted(
            button_data, key=lambda b: b['location']['y'], reverse=True
        )
    elif modifier == 'negative':
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
            the_scale = find_scale(
                button_length, [diatonic_major, pentatonic_major, chromatic]
            )

        mapped_buttons = map_ordered(button_data, the_scale, 60)

    elif adventure == 2:
        if button_length == 7:  # hexatonics
            the_scale = hexatonics[random.choice(hexatonics.keys())]
        elif button_length == 8 or button_length == 9:  # octatonics
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
            scale_list = [
                hexatonic_dict['blues'],
                octatonic_one,
                diatonic_both,
                diatonic_extra,
                chromatic,
            ]
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

    button_data = sorted(
        button_data,
        key=lambda b: atan2(
            b['location']['x'] - center_x, b['location']['y'] - center_y
        ),
        reverse=True,
    )
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
            the_scale = random.choice(
                [fifths, chromatic, diatonic_major, diatonic_extra]
            )
        mapped_buttons = map_ordered(button_data, the_scale, 60, same_octave=True)

    elif adventure == 2:
        if button_length <= 7:  # hexatonics
            the_scale = hexatonics[random.choice(hexatonics.keys())]
        elif button_length == 8 or button_length == 9:  # octatonics
            the_scale = random.choice([fourths, octatonic_one, octatonic_two])
        elif button_length <= 11:
            the_scale = random.choice(
                [fourths, diatonic_both, diatonic_extra, octatonic_one, octatonic_two]
            )
        elif button_length >= 12:
            all_scales = hexatonics.extend(
                [fourths, chromatic, diatonic_extra, octatonic_one, octatonic_two]
            )
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

    # Fake radius if we don't have it
    if 'radius' not in button_data[0].keys():
        max_radius = 10
    else:
        # Define how fuzzy we can get
        max_radius = max([b['radius'] for b in button_data])
        max_radius = max_radius

    # Start the data
    rows = []
    rows.append([button_data[0]])

    # Try to put each button in a row
    for button in button_data[1:]:
        appended = False
        for row in rows:
            if appended:
                break
            for b in row:
                if (
                    button['location']['y'] > b['location']['y'] - max_radius
                    and button['location']['y'] < b['location']['y'] + max_radius
                ):
                    row.append(button)
                    appended = True
                    break
        if not appended:
            rows.append([button])

    # Sort each row by X value..
    rows = [sorted(row, key=lambda b: b['location']['x']) for row in rows]

    # make the new list!
    better_button_data = []
    for row in rows:
        better_button_data.extend(row)

    # Pick a mapping
    if adventure == 0:
        if button_length <= 6:
            the_scale = pentatonic_major
        elif button_length == 7 or button_length == 8:
            the_scale = diatonic_major
        elif button_length == 9 or button_length == 10:
            the_scale = diatonic_both
        else:
            the_scale = diatonic_major
        mapped_buttons = map_ordered(better_button_data, the_scale, 60)

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
            the_scale = find_scale(
                button_length, [diatonic_major, pentatonic_major, chromatic]
            )
        mapped_buttons = map_ordered(better_button_data, the_scale, 60)

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
            scale_list = [
                hexatonic_dict['blues'],
                octatonic_one,
                diatonic_both,
                diatonic_extra,
                chromatic,
            ]
            the_scale = find_scale(button_length, scale_list)

        mapped_buttons = map_ordered(better_button_data, the_scale, 60)

    elif adventure == 3:
        mapped_buttons = map_equal_tempered(better_button_data, 60)

    elif adventure == 4:
        mapped_buttons = map_by_ratio(better_button_data, 60)

    return mapped_buttons


def map_as_large_grid(button_data, adventure):
    # rows first, then columns
    button_data = sorted(button_data, key=lambda b: b['location']['x'])
    button_data = sorted(button_data, key=lambda b: b['location']['y'], reverse=True)

    # Get the number of rows and columns
    rows = OrderedDict()
    cols = OrderedDict()
    for button in button_data:
        if button['location']['y'] not in rows:
            rows[button['location']['y']] = []
            rows[button['location']['y']].append(button)
        else:
            rows[button['location']['y']].append(button)

        if button['location']['x'] not in cols:
            cols[button['location']['x']] = []
            cols[button['location']['x']].append(button)
        else:
            cols[button['location']['x']].append(button)
    num_rows = len(rows)
    num_cols = len(cols)

    # Figure out if we have more columns or rows.
    # This determines where we put the scales, and where we put the leaps
    if num_cols >= num_rows:
        large_dimension = num_cols
        short_dimension = num_rows
        short = rows
    else:
        large_dimension = num_rows
        short_dimension = num_cols
        short = cols

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
            the_scale = find_scale(
                large_dimension, [diatonic_major, pentatonic_major, chromatic]
            )

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
            the_scale = find_scale(
                large_dimension, [diatonic_minor, pentatonic_minor, chromatic]
            )

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
            scale_list = [
                hexatonic_dict['blues'],
                octatonic_one,
                diatonic_both,
                diatonic_extra,
                chromatic,
            ]
            the_scale = find_scale(large_dimension, scale_list)

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
    for i, loc in enumerate(short):
        temp_buttons = []
        for button in short[loc]:
            temp_buttons.append(button_data[button_data.index(button)])
        note_number = base_note_number + short_dimension_interval * i

        if adventure < 3:
            mapped_row = map_ordered(temp_buttons, the_scale, note_number)
            mapped_buttons.extend(mapped_row)
        if adventure == 3:
            mapped_row = map_equal_tempered(temp_buttons, note_number)
            mapped_buttons.extend(mapped_row)

    return mapped_buttons


def map_as_tonnetz(button_data, adventure):
    # rows first, then columns
    button_data = sorted(button_data, key=lambda b: b['location']['x'])
    button_data = sorted(button_data, key=lambda b: b['location']['y'], reverse=True)

    # Will need to get short / long here toooo
    # Get the number of rows and columns
    rows = OrderedDict()
    cols = OrderedDict()
    for button in button_data:
        if button['location']['y'] not in rows:
            rows[button['location']['y']] = []
            rows[button['location']['y']].append(button)
        else:
            rows[button['location']['y']].append(button)

        if button['location']['x'] not in cols:
            cols[button['location']['x']] = []
            cols[button['location']['x']].append(button)
        else:
            cols[button['location']['x']].append(button)
    num_rows = len(rows)
    num_cols = len(cols)

    # Figure out if we have more columns or rows.
    # This determines where we put the scales, and where we put the leaps
    if num_cols >= num_rows:
        axis = 'x'
        short = rows
    else:
        axis = 'y'
        short = cols

    if adventure == 0:  # the classical m3, M3, P5
        low_offset = -4
        high_offset = 3
        the_scale = fifths

    if adventure == 1:
        if random.random() > 0.5:
            low_offset = -4
            high_offset = 3
            the_scale = fifths
        else:
            low_offset = -3
            high_offset = 2
            the_scale = fourths

    if adventure == 2:
        if random.random() > 0.5:
            low_offset = -3
            high_offset = 2
            the_scale = fourths
        else:
            low_offset = -2
            high_offset = 1
            the_scale = minor_thirds

    if adventure == 3:
        low_offset = random.choice([-6, -5, -4, -3, -2])
        high_offset = random.choice([5, 4, 3, 2, 1])
        the_scale = random.choice([[5], [4], [3], [2], [1]])

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

    # map the first button
    # Find the buttons that are nearest to it

    first_buttons = []
    short_keys = sorted(short.keys())
    for i, key in enumerate(short_keys):
        if i == 0:
            first_buttons.append(short[key][0])
            temp_buttons = []
            for button in short[key]:
                temp_buttons.append(button_data[button_data.index(button)])
            note_number = base_note_number
        else:

            last_button = first_buttons[-1]
            # compare!
            if last_button['location'][axis] < short[key][0]['location'][axis]:
                offset = low_offset
            else:
                offset = high_offset

            temp_buttons = []
            for button in short[key]:
                temp_buttons.append(button_data[button_data.index(button)])
            note_number = note_number + offset

            first_buttons.append(short[key][0])

        if adventure < 4:
            mapped_row = map_ordered(temp_buttons, the_scale, note_number)
            mapped_buttons.extend(mapped_row)

    return mapped_buttons


# Modifier functions for mappings ----------------------
def check_size(button_data, axis):
    button_data = sorted(button_data, key=lambda b: b['location'][axis])
    positive_increase = True
    negative_increase = True

    for index, button in enumerate(button_data[0:-1]):
        if button_data[index]['radius'] < button_data[index + 1]['radius']:
            continue
        else:
            positive_increase = False
            break

    for index, button in enumerate(button_data[0:-1]):
        if button_data[index]['radius'] > button_data[index + 1]['radius']:
            continue
        else:
            negative_increase = False
            break

    if positive_increase:
        return 'positive'
    elif negative_increase:
        return 'negative'
    else:
        return None


# if the maximum is not at the far left and right,
# and things decrease from it, in both directions, it is a kalimba!
def check_basic_kalimba(button_data):
    max_size = 0
    max_size_index = 0
    for index, button in enumerate(button_data[1:-1]):
        if button['radius'] > max_size:
            max_size = button['radius']
            max_size_index = index + 1

    left_list = button_data[0:max_size_index]  # check to see if it increases!
    right_list = button_data[max_size_index + 1 :]  # check to see if it decreases!

    left_check = True
    for index, button in enumerate(left_list[0:-1]):
        if left_list[index]['radius'] < left_list[index + 1]['radius']:
            continue
        else:
            left_check = False
            break

    right_check = True
    for index, button in enumerate(right_list[0:-1]):
        if right_list[index]['radius'] > right_list[index + 1]['radius']:
            continue
        else:
            left_check = False
            break

    # if both of those are true, return true!
    if left_check and right_check:
        return 'kalimba'
    else:
        return None


def check_staff(button_data):
    button_data = sorted(button_data, key=lambda b: b['location']['y'])
    shapes = [button_data[0]['shape'], button_data[1]['shape']]
    is_staff = True
    for index, button in enumerate(button_data):
        if (
            button['shape'] != shapes[index % 2]
            or button['shape'] == shapes[(index % 2) - 1]
        ):
            is_staff = False
            break

    if is_staff:
        return 'staff'
    else:
        return None


# Translation functions for scikit --------------
def translate_data_to_scikit(data):
    all_data = []
    for raw_example in data:
        example_data = generate_features(raw_example)
        all_data.append(example_data)
    return all_data


def generate_features(button_data):
    button_data = sorted(button_data, key=lambda b: b['location']['x'])
    button_data = sorted(button_data, key=lambda b: b['location']['y'], reverse=True)
    num_buttons = len(button_data)

    num_rows, num_cols = get_rows_and_cols(button_data)

    slope = get_slope(button_data)

    def line_eq(x):
        return slope * x + button_data[0]['location']['y']

    # normalized mean and std dev from the line slope
    total_distance = get_euclidian_distance(button_data[0], button_data[-1])

    variences = []
    for button in button_data:
        rel_x = button['location']['x'] - button_data[0]['location']['x']
        varience = abs(line_eq(rel_x) - button['location']['y'])
        varience = varience / float(total_distance)
        variences.append(varience)

    mean_varience = get_mean(variences)
    std_dev_varience = get_standard_dev(variences)

    # normalized mean and std dev from the horiztonal center
    x_locs = [button['location']['x'] for button in button_data]
    mean_x = get_mean(x_locs)

    x_variences = []
    for x in x_locs:
        x_varience = abs(mean_x - x) / float(total_distance)
        x_variences.append(x_varience)

    mean_x_varience = get_mean(x_variences)
    std_dev_x_varience = get_standard_dev(x_variences)

    return [
        num_buttons,
        num_rows,
        num_cols,
        slope,
        mean_varience,
        std_dev_varience,
        mean_x_varience,
        std_dev_x_varience,
    ]


def get_mean(the_list):
    return sum(the_list) / float(len(the_list))


def get_standard_dev(the_list):
    mean = get_mean(the_list)
    squared_diffs = [(mean - num) ** 2 for num in the_list]
    standard_dev = get_mean(squared_diffs) ** 0.5
    return standard_dev


def get_euclidian_distance(button_1, button_2):
    x2 = (button_1['location']['x'] - button_2['location']['x']) ** 2
    y2 = (button_1['location']['y'] - button_2['location']['y']) ** 2
    return (x2 + y2) ** 0.5


def get_slope(button_data):
    x_button_data = sorted(button_data, key=lambda b: b['location']['x'])
    x_dist = x_button_data[0]['location']['x'] - x_button_data[-1]['location']['x']

    y_button_data = sorted(button_data, key=lambda b: b['location']['y'], reverse=True)
    y_dist = y_button_data[0]['location']['y'] - y_button_data[-1]['location']['y']

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
        max_radius = max_radius

    rows.append(button_data[0]['location']['y'])
    cols.append(button_data[0]['location']['x'])

    for button in button_data[1:]:
        for row in rows:
            if (
                button['location']['y'] < row - max_radius
                or button['location']['y'] > row + max_radius
            ):
                rows.append(button['location']['y'])
                break
        for col in cols:
            if (
                button['location']['x'] < col - max_radius
                or button['location']['x'] > col + max_radius
            ):
                cols.append(button['location']['x'])
                break

    num_rows = len(rows)
    num_cols = len(cols)
    return num_rows, num_cols


# Main classify and map function --------------
def classification_from_data(example_data):
    translated_data = generate_features(example_data)
    res = get_classification(translated_data)

    # For certain prototypes, check size patterns
    modifier = None
    if 'radius' in example_data[0]:
        if res == 'zither':
            modifier = check_size(example_data, 'y')
        elif res == 'xylophone':
            modifier = check_size(example_data, 'x')
            if not modifier:
                modifier = check_basic_kalimba(example_data)

    if not modifier and res == 'zither' and 'shape' in example_data[0]:
        modifier = check_staff(example_data)
    return res, modifier


# Main function
def analyze(event_body):
    button_data = json.loads(event_body)
    if 'adventure' in button_data:
        adventure = button_data['adventure']
    else:
        adventure = 0

    if 'buttonData' in button_data:
        button_data = button_data['buttonData']
    else:
        button_data = button_data

    classification, modifier = classification_from_data(button_data)
    mapping_data = mapping_from_classification(
        classification, button_data, adventure, modifier
    )
    return {'result': classification, 'mapping': mapping_data, 'modifier': modifier}


def lambda_handler(event, context):
    result = analyze(event['body'])
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json',
        },
        'body': json.dumps(result),
    }
