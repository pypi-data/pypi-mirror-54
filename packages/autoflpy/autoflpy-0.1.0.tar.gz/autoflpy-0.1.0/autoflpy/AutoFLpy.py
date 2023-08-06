"""
This modules allows for the running of the log to xls converter and the
automatic flight log generator.
"""

__author__ = "Adrian Weishaeupl"

from log_to_xls import *
from flight_log_code import *

# Finds the file path from where this code is being run.
base_path = os.getcwd()
# Sets the seperators to be the same as in the format used below.
base_path.replace(os.sep, "/")

# Inputs information needed for the log to xls converter followed by the 
# automatic flight log generator. If no files are given, the latest files
# in the folders are assumed.
# NOTE: make the code input the latest files.
log_file_path = base_path + "/log flight data"
name_converter_file_path = base_path + \
    "/converter files/name converter list.txt"
data_sources_file_path = base_path + "/converter files/data sources.txt"
excel_data_file_path = base_path + "/xls flight data"


template_file_path = base_path + "/templates"
flight_data_file_path = base_path + "/xls flight data"
arduino_flight_data_file_path = base_path + "/arduino flight data"
checklist_data_file_path = base_path + "/checklists"
metar_file_path = base_path + "/metar file storage"
# RAF Fairford ICAO code as it is a large airfield with regular METAR reports
# close Draycott airfield.
icao_code = "EGVA"
flight_log_destination = base_path + "/flight logs generated"

log_to_xls_converter_interface(log_file_path,
                               name_converter_file_path,
                               data_sources_file_path,
                               excel_data_file_path)

flight_log_maker_interface(template_file_path,
                           flight_data_file_path,
                           arduino_flight_data_file_path,
                           checklist_data_file_path,
                           metar_file_path,
                           icao_code,
                           flight_log_destination)
