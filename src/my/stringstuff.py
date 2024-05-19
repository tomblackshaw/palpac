'''
Created on May 19, 2024

@author: Tom Blackshaw

stringstuff
'''

import os
from parse import parse
import requests


def add_to_os_path(a_path):
    if os.path.exists(a_path):
        os.environ['PATH'] += os.pathsep + a_path


def get_random_zenquote():
    response = requests.get('https://zenquotes.io/api/random')
    data = response.json()[0]
    quote = data['q'] + ' - ' + data['a']
    return quote


def flatten(xss):
    return [x for xs in xss for x in xs]


def wind_direction_str(degrees):
    degrees = degrees % 360
    winddirection_lst = ['North', 'North North East', 'Northeast', 'East Northeast', 'East', 'East Southeast', 'Southeast', 'South Southeast',
                         'South', 'South Southwest', 'Southwest', 'West Southwest', 'West', 'West Northwest', 'Northwest', 'North Northwest']
    degrees_entry = int(degrees / 22.5)
    if 0 <= degrees_entry < len(winddirection_lst):
        return winddirection_lst[degrees_entry]
    else:
        return "unknown"

