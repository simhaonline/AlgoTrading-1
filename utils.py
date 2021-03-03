"""
This file houses all utils that are used across files.

Created By:     Brandon Jinright
Created On:     02/12/2021
Last Updated:   02/12/2021
"""

import time
import datetime as dt


def get_time():
    return dt.datetime.today().strftime("%m/%d/%Y_%H:%M:%S:%f")
