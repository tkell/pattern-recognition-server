#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Tools for figuring out button size things.
Is it a kalimba or not, which way do the buttons go, etc?
'''

# Checks to see which direction the size changes in, if any
# axis is 'x' or 'y'
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
    for index, button in button_data[1:-1]:
        if button['radius'] > max_size:
            max_size = button['radius']
            max_size_index = index

    left_list = button_data[0:max_size_index] # check to see if it increases!
    right_list = button_data[max_size_index + 1:] # check to see if it decreases!

    print "about to check lists"
    left_check = True
    for index, button in enumerate(left_list[0:-1]):
        if button_data[index]['radius'] < button_data[index + 1]['radius']:
            continue
        else:
            left_check = False
            break

    right_check = True
    for index, button in enumerate(right_list[0:-1]):
        if button_data[index]['radius'] > button_data[index + 1]['radius']:
            continue
        else:
            left_check = False
            break

    # if both of those are true, return true!
    if left_check and right_check:
        return 'kalimba'
    else:
        return None