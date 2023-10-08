import os
import ast
import numpy as np
import logging
from dotenv import load_dotenv

# Initial
load_dotenv()
PNAME = os.getenv('PNAME')
APOLLO_RECORD_FILE_INDEX = os.getenv('APOLLO_RECORD_FILE_INDEX')
CANBUS_FOLDER_PATH = os.getenv('CANBUS_FOLDER_PATH').replace("_PXX_", PNAME)
RGB_FOLDER_PATH = os.getenv('RGB_FOLDER_PATH').replace("_PXX_", PNAME)
RGB_BASELINE_FOLDER_PATH = RGB_FOLDER_PATH + 'Baseline/'
RGB_DRIVER1_FOLDER_PATH = RGB_FOLDER_PATH + 'Driver1/'
RGB_DRIVER2_FOLDER_PATH = RGB_FOLDER_PATH + 'Driver2/'
RGB_DRIVER3_FOLDER_PATH = RGB_FOLDER_PATH + 'Driver3/'
RGB_PASSENGER1_FOLDER_PATH = RGB_FOLDER_PATH + 'Passenger1/'
RGB_PASSENGER2_FOLDER_PATH = RGB_FOLDER_PATH + 'Passenger2/'

MARKER_TIME_EEG = os.getenv('MARKER_TIME_EEG')
STANDARD_TIME_EEG = float(os.getenv('STANDARD_TIME_EEG'))

ADJUST_BEFORE_SECONDS = float(os.getenv('ADJUST_BEFORE_SECONDS'))
ADJUST_AFTER_SECONDS = float(os.getenv('ADJUST_AFTER_SECONDS'))

