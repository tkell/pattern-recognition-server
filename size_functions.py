#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Tools for figuring out button size things.
Is it a kalimba or not, which way do the buttons go, etc?
'''

# Checks to see which direction the size changes in, if any
# axis is 'x' or 'y'
def check_size(button_data, axis):
    print "about to sort data"
    button_data = sorted(button_data, key=lambda b: b['location'][axis])

    positive_increase = True
    negative_increase = True

    print "checking for + increase"
    for index, button in button_data[0:-1]:
        if button_data[index]['radius'][axis] > button_data[index + 1]['radius'][axis]:
            continue
        else:
            positive_increase = False
            break

    button_data.reverse()

    print "checking for - increase"
    for index, button in button_data[0:-1]:
        if button_data[index]['radius'][axis]  > button_data[index + 1]['radius'][axis]:
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
        if button['size'] > max_size:
            max_size = button['size']
            max_size_index = index

    left_list = button_data[0:max_size_index] # check to see if it increases!
    right_list = button_data[max_size_index + 1:] # check to see if it decreases!

    # if both of those are true, return true!