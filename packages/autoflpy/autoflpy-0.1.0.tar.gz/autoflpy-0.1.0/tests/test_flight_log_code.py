# -*- coding: utf-8 -*-
"""
Unit tests for the flight_log_code.py and the log_to_xls.py
codes. *** WORK IN PROGRESS ***
No tests are currently written for the GUI.

@author Adrian Weishaeupl (aw6g15@soton.ac.uk)
"""

import unittest
import flight_log_code
import os
from datetime import datetime


class Test_flight_log_code(unittest.TestCase):

    def setUp(self):
        # Sets up all of the test variables and locations to be used
        # throughout.
        self.base_path = os.getcwd() + "\\test_files\\"
        self.template_file_path = self.base_path  # NOTE Replace this with only
        # the file name for a reduced workload on the user.
        self.template_file_name = "test_template.ipynb"
        self.flight_log_file_path = self.base_path
        self.flight_data_file_path = self.base_path
        self.flight_data_file_name = "test_xls.xls"
        self.arduino_flight_data_file_path = self.base_path
        self.arduino_flight_data_name = "test_arduino_2.csv"
        self.flight_date = 20191203
        self.flight_number = 2
        self.flight_log_file_name_header = "test_generated_flight_log"
        self.checklist_file_path = self.base_path
        self.log_code_version = "flight_log_code"
        self.ICAO_airfield = "EGHI"
        self.start_time_hours = "9"
        self.end_time_hours = "10"
        self.metar_file_path = self.base_path

    def test_flight_log_maker(self):
        flight_log_code.flight_log_maker(self.template_file_path,
                                         self.template_file_name,
                                         self.flight_log_file_path,
                                         self.flight_data_file_path,
                                         self.flight_data_file_name,
                                         self.arduino_flight_data_file_path,
                                         self.arduino_flight_data_name,
                                         self.flight_date,
                                         self.flight_number,
                                         self.flight_log_file_name_header,
                                         self.checklist_file_path,
                                         self.log_code_version,
                                         self.ICAO_airfield,
                                         self.start_time_hours,
                                         self.end_time_hours,
                                         self.metar_file_path)
        # This code tests the flight_log_maker function.
        # First, check that a file has been created.
        test_flight_log_file_path = self.base_path + \
            'test_generated_flight_log20191203 2.ipynb'
        if os.path.exists(test_flight_log_file_path) is True:
            file_exists = True
        self.assertTrue(file_exists)
        # Checks that the file was recently created.
        filetime = os.stat(test_flight_log_file_path)
        # Finds the time since the file has been created.
        time_diff = datetime.fromtimestamp(filetime.st_mtime) - datetime.now()
        # Checks that the time difference is less than 0.01 seconds
        time_diff_negligible = time_diff.seconds < 0.01
        self.assertTrue(time_diff_negligible)

    def test_flight_data(self):
        # Tests the flight data code.
        frame_list = flight_log_code.flight_data(
                self.flight_data_file_path,
                self.flight_data_file_name)
        # Checks that the expected frame dimensions are the correct size.
        frame_dimensions = [17693, 102030, 21784, 24498, 61218, 47614, 61218,
                            20406]
        if len(frame_list) == 8:
            for frame in range(len(frame_list)):
                self.assertEqual(frame_list[frame].size,
                                 frame_dimensions[frame])
        else:
            # Raises a fault if the length of the frame_list is not as
            # expected.
            self.assertEqual(1, 2)

    def test_checklist_finder(self):
        


if __name__ == '__main__':
    unittest.main()
