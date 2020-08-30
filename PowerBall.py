#!/us/bin/env python
#===========================================================================================================================
# Powerball Frequency analyzer and quick pick
# basically a python re-write of https://github.com/toastyxen/Old_Perl_Projects/blob/master/lotto/pbhist00.pl
# with functionality of this https://github.com/toastyxen/Old_Perl_Projects/blob/master/lotto/powerballnew.pl
# Except powerball changed to 26 power ball numbers, as of April 2020 they used to do 35, while
# They increased the number of white balls from 59 to 69
# They also removed the winnums-text.txt and have a search fucntion, so we'll need to figure out how to get the history
# Author: Lloyd Turk Jr.
#===========================================================================================================================
# 

import random
import os
#import urllib
import urllib.request as ur
import json
#import time
from datetime import datetime, date
#from collections import defaultdict

import pandas as pd

#START_TIME = time.time()
SYSTEM_RANDOM = os.urandom
random.seed(SYSTEM_RANDOM)

def get_drawing_history():
    """Get the data from online"""
    url = "https://data.ny.gov/api/views/d6yy-54nr/rows.json" # It's on data.gov from NY
    response = ur.urlopen(url)
    json_data = json.loads(response.read())
    #print(json_data.keys())

    raw_data = json_data["data"]
    raw_list = [] #
    for i in raw_data:
        raw_list.extend((i[8], i[9]))

    chunked_data_list = []
    for i in range(0, len(raw_list), 2):
        chunk = raw_list[i:i + 2]
        chunked_data_list.append(chunk)

    final_data_list = []
    for i in chunked_data_list: # This works, it seems like it could still be more optimized though
        raw_date_time_str = i[0] # Raw date/time string from the json
        # Cleaned up date/time string
        date_time_str = datetime.strptime(raw_date_time_str, "%Y-%m-%dT%H:%M:%S")
        # Get rid of time part, we don't need it, I'm sure there is an easier/lighter way to do this
        # but this works for now
        date_str = date_time_str.strftime("%Y-%m-%d")

        final_data_list.append([date_str, i[1]])

    #print(final_data_list)
    return final_data_list

def quick_pick():
    """Quickpick function"""
    nums = []
    count = 1
    while count <= 5: # we need 5 numbers
        pick = random.randint(1, 69) # From 1 to 69
        # If pick isn't in the nums list, append the pick to the nums list,
        # it would return occasional dupes, this should fix that.
        if pick not in nums:
            nums.append(pick) # Append them to the list
            count = count+1
        else: # Don't add anything to count
            pass
    nums.sort() # Sort list for readability, makes it easier when filling out the number slips

    power_ball = random.randint(1, 26)

    print("========================================================================")
    print("Random quick pick numbers: " + str(nums) +" "+ str(power_ball))
    #print("========================================================================")

def frequency():
    """Analyze frequency of numbers"""
    data = get_drawing_history()

    # For custom date input
    #oldest_date = str(input("In put the oldest date in YYYY-MM-DD format: ")) 
    oldest_date = "2020-04-08" # This is the latest rule change
    #oldest_date = "2010-02-03" # The oldest date the data set goes back to

    today = date.today()

    dates = pd.date_range(start=oldest_date, end=today) # Get a date range using pandas

    # Converts the pandas date_range into a list. This might not be necessary?
    date_list = []
    for date_time_obj  in dates:
        date_str = date_time_obj.strftime("%Y-%m-%d")
        date_list.append(date_str)

    ball_list = [] # This is a list, of strings being "int int int int int int"
    for i in data:
        if i[0] in date_list:
            ball_list.append(i[1])
    # We split these strings into lists of strings ["int", "int", "int", "int", "int", "int"], [...]
    split_list = []
    for i in ball_list:
        split = i.split()
        split_list.append(split)
    #print(split_list)

    split_ball_list = [] # We turn this list of lists into a single list of strings
    for i in split_list:
        for j in i:
            split_ball_list.append(int(j))
            # We want the data in the list to be int, to use comparative operations later

    pb_list = split_ball_list[5::6] # Powerball is going to be every 6th entry in the list

    # To get white ball nums we now delete every 6th entry, which is the powerball
    del split_ball_list[5::6]

    white_ball_list = split_ball_list # Assign to a new list name, for ease of programming


    white_ball_list.sort() # Sort the list, this makes the dict we convert it to later more readable
    pb_list.sort() # Sort the list, this makes the dict we convert it to later more readable

    #unique_pb_list = list(set(pb_list))
    #unique_wb_list = list(set(white_ball_list))

    white_ball_dict = {i:white_ball_list.count(i) for i in white_ball_list}
    pb_dict = {i:pb_list.count(i) for i in pb_list}

    # Get powerball values and number of times they've been drawn
    pb_max_value = max(pb_dict.values()) # Find the most commonly drawn powerball number

    # Maximum secondary value for PB
    pb_max_secondary = 0
    for i in pb_dict.values(): # Find the second most commonly drawn powerball number
        if(i > pb_max_secondary and i < pb_max_value):
            pb_max_secondary = i

    print("========================================================================")
    print("All numbers drawn for PB with number of times drawn, in given date range")
    print("Number:Number of times drawn")
    print(pb_dict)
    #for key, value in pb_dict.items(): # Print all pb and number of times drawn
    #    print(str(key) + ":" + str(value))
    print("========================================================================")
    print("Most commonly drawn Powerball(s) since given date: ")
    print("Number:Number of times drawn")
    for key, value in pb_dict.items():
        if value == pb_max_value: # Print pb(s) with highest draw rate
            print(str(key) + ":" + str(value))
    print("========================================================================")
    print("Second most commonly drawn Powerball(s) since given date: ")
    print("Number:Number of times drawn")
    for key, value in pb_dict.items():
        if value == pb_max_secondary: # Print pb(s) with second highest draw rate
            print(str(key) + ":" + str(value))
    print("========================================================================")

    # Get white ball values and number of times they've been drawn
    wb_max_value = max(white_ball_dict.values())
    # Maximum secondary value for PB
    wb_max_secondary = 0
    for i in white_ball_dict.values(): # Find the second most commonly drawn powerball number
        if(i > wb_max_secondary and i < wb_max_value):
            wb_max_secondary = i
    print("All numbers drawn with number of times drawn, in given date range")
    print("Number:Number of times drawn")
    print(white_ball_dict)
    #for key, value in white_ball_dict.items(): # Print all pb and number of times drawn
    #    print(str(key) + ":" + str(value))
    print("========================================================================")
    print("Most commonly drawn number(s) since given date: ")
    print("Number:Number of times drawn")
    for key, value in white_ball_dict.items():
        if value == wb_max_value: # Print wb(s) with highest draw rate
            print(str(key) + ":" + str(value))
    print("========================================================================")
    print("Second most commonly drawn number(s) since given date: ")
    print("Number:Number of times drawn")
    for key, value in white_ball_dict.items():
        if value == wb_max_secondary: # Print wb(s) with second highest draw rate
            print(str(key) + ":" + str(value))
    print("========================================================================")
    print('This program is just for frequency analysis and a "Quick Pick" random'
          '\nnumber generator making no pretense at predictive accuracy')


quick_pick()
frequency()

# For debugging to make sure it didn't take too long to run
#print("--- %s seconds ---" % (time.time() - START_TIME)) 
