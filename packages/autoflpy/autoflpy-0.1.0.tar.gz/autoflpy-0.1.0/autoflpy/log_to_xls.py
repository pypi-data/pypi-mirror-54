# -*- coding: utf-8 -*-

import xlwt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import datetime

"""
This code converts a .log file (generated using mission planner from a .bin
file) into a .xls document to be used with the automated flight log creator.
@author: Adrian Weishaeupl
aw6g15@soton.ac.uk 2019

Based on work done by Samuel Pearson (sp1g18@soton.ac.uk) (06-08/2019)
"""


def log_to_xls_converter_interface(log_file_path="Data",
                                   name_converter_file_path="Data",
                                   data_sources_file_path="Data",
                                   excel_data_file_path="Data",
                                   excel_file_name="Data"):
    root = tk.Tk()
    # Changes the title bar
    root.title(".log to .xls converter")
    root.configure(background="#eeeeee")
    img = tk.Image("photo", file="images" + os.sep + "Plane.gif")
    root.tk.call("wm", "iconphoto", root._w, img)
    # Creates a title
    heading_label = tk.Label(root, text=".log to .xls converter",
                             bg="white", pady=25)
    heading_label.config(font=("Helvetica", 20))
    # Places the row label in the grid
    heading_label.grid(row=0, column=0, columnspan=8, sticky="ew")
    # Creates a subtitle
    subtitle_label = tk.Label(root, text="Please enter the required data" +
                              " below.")
    subtitle_label.config(font=("Helvetica", 11), pady=5)
    # Places the row label in the grid
    subtitle_label.grid(row=1, column=0, columnspan=8, sticky="ew")
    # Creates a label for the log_file_path row.
    log_file_path_label = tk.Label(root, text="File path of " +
                                   "the flight data log file*")
    # Places the row label in the grid
    log_file_path_label.grid(row=2, column=0, columnspan=2, sticky="nw")
    # This creates the text box for the file path
    log_file_path_text = tk.Text(root, height=2, width=50)
    log_file_path_text.insert(tk.END, "Data")
    log_file_path_text.grid(row=2, column=3, columnspan=3)
    # This function changes the data in the text box to match the data
    # selected.

    def log_file_path_text_function():
        text = filedialog.askopenfilename(initialdir=log_file_path)
        # If nothing entered, do not clear the text box.
        if text == "":
            return
        # Deletes text currently in box.
        log_file_path_text.delete("1.0", tk.END)
        # Inserts text from file selecter
        log_file_path_text.insert(tk.END, text)
    # This is the button for the log_file_path
    log_file_path_button = tk.Button(root, text="Select file",
                                     command=log_file_path_text_function,
                                     width="15", height="2", bg="#dddddd")
    # This places the log_file_path button in the grid
    log_file_path_button.grid(row=2, column=6, columnspan=2)
    # Creates a label for the flight data
    name_converter_label = tk.Label(root, text="File path of the name "
                                    "converter document*")
    # Places the row label in the grid
    name_converter_label.grid(row=3, column=0, columnspan=2, sticky="nw")
    # This creates the text box for the file path
    name_converter_text = tk.Text(root, height=2, width=50)
    name_converter_text.insert(tk.END, name_converter_file_path)
    name_converter_text.grid(row=3, column=3, columnspan=3)
    # This function changes the data in the text box to match the data
    # selected.

    def name_converter_file_path_text():
        # Removes file name from end of file path
        file_name = name_converter_file_path.replace("\\", "/").split("/")[-1]
        # Removes the file name and leaves the file path to get to that file
        text = filedialog.askopenfilename(
                initialdir=name_converter_file_path.replace(
                    "\\" + file_name, "").replace("/" + file_name, ""))
        # If nothing entered, do not clear the text box.
        if text == "":
            return
        # Deletes text currently in box.
        name_converter_text.delete("1.0", tk.END)
        # Inserts text from file selecter
        name_converter_text.insert(tk.END, text)
    # This is the button for the log_file_path
    name_converter_button = tk.Button(root, text="Select file",
                                      command=name_converter_file_path_text,
                                      width="15", height="2", bg="#dddddd")
    # This places the flight data button in the grid
    name_converter_button.grid(row=3, column=6, columnspan=2)
    # Creates a label for the flight data
    data_sources_label = tk.Label(root, text="File path of the data sources"
                                  " document*")
    # Places the row label in the grid
    data_sources_label.grid(row=4, column=0, columnspan=2, sticky="nw")
    # This creates the text box for the file path
    data_sources_text = tk.Text(root, height=2, width=50)
    data_sources_text.insert(tk.END, data_sources_file_path)
    data_sources_text.grid(row=4, column=3, columnspan=3)
    # This function changes the data in the text box to match the data
    # selected.

    def data_sources_file_path_text():
        # Removes file name from end of file path
        file_name = data_sources_file_path.replace("\\", "/").split("/")[-1]
        # Removes the file name and leaves the file path to get to that file
        text = filedialog.askopenfilename(
                initialdir=data_sources_file_path.replace(
                    "\\" + file_name, "").replace("/" + file_name, ""))
        # If nothing entered, do not clear the text box.
        if text == "":
            return
        # Deletes text currently in box.
        data_sources_text.delete("1.0", tk.END)
        # Inserts text from file selecter
        data_sources_text.insert(tk.END, text)
    # This is the button for the log_file_path
    data_sources_button = tk.Button(root, text="Select file",
                                    command=data_sources_file_path_text,
                                    width="15", height="2", bg="#dddddd")
    # This places the flight data button in the grid
    data_sources_button.grid(row=4, column=6, columnspan=2)
    # Creates a label for the arduino flight data
    excel_data_label = tk.Label(root, text="Destination file path for the " +
                                "excel document*")
    excel_data_label.grid(row=5, column=0, columnspan=2, sticky="nw")
    # This creates the text box for the file path
    excel_data_text = tk.Text(root, height=2, width=50)
    excel_data_text.insert(tk.END, excel_data_file_path)
    excel_data_text.grid(row=5, column=3, columnspan=3)
    # This function changes the data in the text box to match the data
    # selected.

    def excel_data_file_path_text():
        text = filedialog.askdirectory(initialdir=excel_data_file_path)
        # If nothing entered, do not clear the text box.
        if text == "":
            return
        # Deletes text currently in box.
        excel_data_text.delete("1.0", tk.END)
        # Inserts text from file selecter
        excel_data_text.insert(tk.END, text)
    # This is the button for the log_file_path
    excel_data_button =\
        tk.Button(root, text="Select folder",
                  command=excel_data_file_path_text, width="15",
                  height="2", bg="#dddddd")
    # This places the excel button in the grid.
    excel_data_button.grid(row=5, column=6, columnspan=2)
    # Creates a label for the excel file
    excel_file_name_label = tk.Label(root, text="Name of the new excel file*")
    excel_file_name_label.grid(row=9, column=0, columnspan=2, sticky="nw")
    # This creates the text box for the file path
    excel_file_name_text = tk.Text(root, height=1, width=25)
    excel_file_name_text.insert(tk.END, excel_file_name)
    excel_file_name_text.grid(row=9, column=3, columnspan=3)
    # This function changes the data in the text box to match the data
    # selected.

    def excel_file_name_updater():
        # Gets the flight date
        year = year_data_text.get()
        # Checks to see if the year data is in the right format
        try:
            int(year)
            year_available = True
        except ValueError:
            year_available = False
        # Appends result to check_data list
        month = month_data_text.get()
        # Checks to see if the month data is in the right format
        try:
            int(month)
            month_available = True
        except ValueError:
            month_available = False
        # Appends result to check_data list
        day = day_data_text.get()
        # Checks to see if the day data is in the right format
        try:
            int(day)
            day_available = True
        except ValueError:
            day_available = False
        # Appends result to check_data list
        # Puts the month in the correct format
        if len(month) < 2:
            month = "0" + month
        # Puts the day in the correct format
        if len(day) < 2:
            day = "0" + day
        # Ensures the year is returned in the correct format
        if len(year) < 4:
            year = "20" + year
        # Gets the flight date from the input data.
        flight_date = int((year + month + day).replace("\n", ""))
        # Gets the flight number from the input data.
        try:
            # Checks to see if the flight number is available
            flight_number = int(flight_number_text.get())
            flight_number_available = True
        except ValueError:
            # If it is not then the flight number is returned as False.
            flight_number_available = False
        # Checks to see if the flight date is available
        if (year_available and month_available and day_available) is True:
            text = str(flight_date) + "_Flight"
            # Checks to see if the flight number is available
            if flight_number_available is True:
                text += str(flight_number)
            else:
                # Error message popup explaining that data is required
                messagebox.showinfo("Error", "Flight number is required for"
                                    " the automatic generation of the excel"
                                    " file name.")
                # Sets textbox to be blank.
                text = ""
        else:
            messagebox.showinfo("Error", "The complete flight date is required"
                                " for the automatic generation of the excel"
                                " file name.")
            # Sets textbox to be blank.
            text = ""
        # If nothing entered, do not clear the text box.
        if text == "":
            return
        # Deletes text currently in box.
        excel_file_name_text.delete("1.0", tk.END)
        # Inserts text from file selecter
        excel_file_name_text.insert(tk.END, text)
    # This is the button for the log_file_path
    excel_file_name_button =\
        tk.Button(root, text="Update file name",
                  command=excel_file_name_updater, width="15", height="2",
                  bg="#dddddd")
    # This places the flight data button in the grid
    excel_file_name_button.grid(row=9, column=6, columnspan=2)

    # Based on: https://stackoverflow.com/questions/4140437/
    # interactively-validating-entry-widget-content-in-tkinter
    # Checks data entry has a length of 2 or less and is numeric.
    def two_length_and_numeric_check(entry):
        # Checks to see if the entered values are too long or not numeric.
        if (entry.isdigit() or entry == "") and len(entry) <= 2:
            # If they are too long it returns true
            return(True)
        # If not it returns false
        return(False)
    # Registers a TCL callback to python (from link above)
    two_callback = root.register(two_length_and_numeric_check)

    # Based on: https://stackoverflow.com/questions/4140437/
    # interactively-validating-entry-widget-content-in-tkinter
    # Checks data entry has a length of 4 or less and is numeric.
    def four_length_and_numeric_check(entry):
        # Checks to see if the entered values are too long or not numeric.
        if (entry.isdigit() or entry == "") and len(entry) <= 4:
            # If they are too long it returns true
            return(True)
        # If not it returns false
        return(False)
    four_callback = root.register(four_length_and_numeric_check)

    # Based on: https://stackoverflow.com/questions/4140437/
    # interactively-validating-entry-widget-content-in-tkinter
    # Checks data entry has a length of 4 or less and has alphabetic characters
    # only.
    def four_length_and_alpha_check(entry):
        # Checks to see if the entered values are too long or not numeric.
        if (entry.isalpha() or entry == "") and len(entry) <= 4:
            # If they are too long it returns true
            return(True)
        # If not it returns false
        return(False)
    # Creates a label for the year
    year_data_label = tk.Label(root, text="Full length year of the flight.*")
    # Places the row label in the grid
    year_data_label.grid(row=7, column=0, sticky="w", pady=10)
    # This creates the text box for the Year
    year_data_text = tk.Entry(root, width=10)
    # Inputs current year as date.
    year_data_text.insert(tk.END, str(datetime.date.today())[:4])
    # Checks data entry and ensures it is the correct format.
    year_data_text.configure(validate="key", validatecommand=(four_callback,
                                                              "%P"))
    year_data_text.grid(row=7, column=1)
    # Creates a label for the month
    month_data_label = tk.Label(root, text="Month of the flight.*")
    # Places the row label in the grid
    month_data_label.grid(row=7, column=3, sticky="w")
    # This creates the text box for the Year
    month_data_text = tk.Entry(root, width=10)
    # Inputs current month as the starting input.
    month_data_text.insert(tk.END, str(datetime.date.today())[5:7])
    # Checks data entry and ensures it is the correct format.
    month_data_text.configure(validate="key", validatecommand=(two_callback,
                                                               "%P"))
    month_data_text.grid(row=7, column=4)
    # Creates a label for the day
    day_data_label = tk.Label(root, text="Day" +
                              " of the flight.*")
    # Places the row label in the grid
    day_data_label.grid(row=7, column=5, sticky="w")
    # This creates the text box for the Year
    day_data_text = tk.Entry(root, width=10)
    # Inputs current month as the starting input.
    day_data_text.insert(tk.END, str(datetime.date.today())[8:10])
    # Checks data entry and ensures it is the correct format.
    day_data_text.configure(validate="key", validatecommand=(two_callback,
                                                             "%P"))
    day_data_text.grid(row=7, column=7, sticky="w")
    # Creates label for flight number
    flight_number_label = tk.Label(root, text="Flight number*")
    # Places the row label in the grid
    flight_number_label.grid(row=8, column=0, sticky="w", pady=5)
    # This creates the text box for the Year
    flight_number_text = tk.Entry(root, width=10)
    # Places the text Flight Number into the cell
    flight_number_text.insert(tk.END, "Flight No")
    # Checks data entry and ensures it is the correct format.
    flight_number_text.configure(validate="key",
                                 validatecommand=(four_callback, "%P"))
    flight_number_text.grid(row=8, column=3, sticky="w")

    def log_reader_input():
        # Specifies that indicator and indicator_text is defined outside of the
        # function.
        nonlocal indicator
        nonlocal indicator_text
        # Changes background colour of inidicator canvas
        indicator.config(background="#eeaa22")
        # Deletes old text
        indicator.delete(indicator_text)
        # Replaces text in indicator box
        indicator_text = indicator.create_text(100, 7.5, text="Loading")
        # Updates the indicator box
        indicator.update_idletasks()
        # Creates blank list for check of key data.
        check_data = []
        # This creates a list with removes any backslashes and replaces them
        # with forward slashes.
        link = log_file_path_text.get("1.0", tk.END).replace(
                "\\", "/").split("/")
        log_file_path = ""
        # Checks to see if the link is long enough to be valid.
        if len(link) >= 2:
            for location in link[:-1]:
                # Creates a string with seperators between each word in the
                # link.
                log_file_path += location + os.sep
            # Adds on the final word
            log_file_path += link[-1]
            log_file_path = log_file_path.replace("\n", "")
            log_file_path_available = True
        else:
            # Check to see if log_file_path is available.
            log_file_path_available = False
        # Appends result to check_data list
        check_data.append(log_file_path_available)
        # This creates a list with removes any backslashes and replaces them
        # with forward slashes.
        link = name_converter_text.get("1.0", tk.END).replace(
                "\\", "/").split("/")
        name_converter_file_path = ""
        # Checks to see if the link is long enough to be valid.
        if len(link) >= 2:
            for location in link[:-1]:
                # Creates a string with seperators between each word in the
                # link.
                name_converter_file_path += location + os.sep
            # Adds on the final word
            name_converter_file_path += link[-1]
            name_converter_file_path = name_converter_file_path.replace("\n",
                                                                        "")
            check_data.append(True)
        else:
            check_data.append(False)
        link = data_sources_text.get("1.0", tk.END).replace("\\",
                                                            "/").split("/")
        data_sources_file_path = ""
        # Checks to see if the link is long enough to be valid.
        if len(link) >= 2:
            for location in link[:-1]:
                # Creates a string with seperators between each word in the
                # link.
                data_sources_file_path += location + os.sep
            # Adds on the final word
            data_sources_file_path += link[-1]
            data_sources_file_path = data_sources_file_path.replace("\n", "")
            check_data.append(True)
        else:
            check_data.append(False)
        # This creates a list with removes any backslashes and replaces them
        # with forward slashes.
        link = excel_data_text.get("1.0", tk.END).replace(
            "\\", "/").split("/")
        excel_file_path = ""
        # Checks to see if the link is long enough to be valid.
        if len(link) >= 1:
            for location in link[:-1]:
                # Creates a string with seperators between each word in the
                # link.
                excel_file_path += location + os.sep
            # Adds on the final word
            excel_file_path += link[-1]
            excel_file_path = excel_file_path.replace("\n", "")
        # Gets file name directly and removes the new line from the end
        excel_file_name = excel_file_name_text.get("1.0", tk.END).replace("\n",
                                                                          "")
        # Checks to see if the link is long enough to be valid.
        if len(excel_file_name) == 0:
            # Appends False to the check data
            check_data.append(False)
        # Gets the flight date
        year = year_data_text.get()
        # Checks to see if the year data is in the right format
        try:
            int(year)
            year_available = True
        except ValueError:
            year_available = False
        # Appends result to check_data list
        check_data.append(year_available)
        month = month_data_text.get()
        # Checks to see if the month data is in the right format
        try:
            int(month)
            month_available = True
        except ValueError:
            month_available = False
        # Appends result to check_data list
        check_data.append(month_available)
        day = day_data_text.get()
        # Checks to see if the day data is in the right format
        try:
            int(day)
            day_available = True
        except ValueError:
            day_available = False
        # Appends result to check_data list
        check_data.append(day_available)
        # Puts the month in the correct format
        if len(month) < 2:
            month = "0" + month
        # Puts the day in the correct format
        if len(day) < 2:
            day = "0" + day
        # Ensures the year is returned in the correct format
        if len(year) < 4:
            year = "20" + year
        # Gets the flight date from the input data.
        flight_date = int((year + month + day).replace("\n", ""))
        # Gets the flight number from the input data.
        try:
            # Checks to see if the flight number is available
            flight_number = int(flight_number_text.get())
            flight_number_available = True
        except ValueError:
            # If it is not then the flight number is returned as False.
            flight_number_available = False
        check_data.append(flight_number_available)
        # Checks to see if all the data has been correctly entered.
        if not all(check_data) is True:
            # Changes background colour of inidicator canvas
            indicator.config(background="#ee2222")
            # Deletes old text
            indicator.delete(indicator_text)
            # Creates text stating that there was an error
            indicator_text = indicator.create_text(100, 7.5, text="Error")
            # creates a message box to state that there was a problem
            messagebox.showinfo("Error", "Data entered was not in correct " +
                                "format, Please check the data entered " +
                                "and try again.")
            # Changes background colour of inidicator canvas
            indicator.config(background="#22ee22")
            # Deletes old text
            indicator.delete(indicator_text)
            # Restored old text stating that the code is ready to generate
            # another report.
            indicator_text = indicator.create_text(100, 7.5, text="Ready")
            return
        # Runs log reader code
        try:
            log_reader(log_file_path, name_converter_file_path,
                       data_sources_file_path, excel_file_path,
                       excel_file_name, str(flight_date), str(flight_number))
        except PermissionError:
            # Changes background colour of inidicator canvas
            indicator.config(background="#ee2222")
            # Deletes old text
            indicator.delete(indicator_text)
            # Creates text stating that there was an error
            indicator_text = indicator.create_text(100, 7.5, text="Error")
            # creates a message box to state that there was a problem
            messagebox.showinfo("Permission Error", "Check that files "
                                "being opened by the code are not open in a"
                                " different program.")
            # Changes background colour of inidicator canvas
            indicator.config(background="#22ee22")
            # Deletes old text
            indicator.delete(indicator_text)
            # Restored old text stating that the code is ready to generate
            # another report.
            indicator_text = indicator.create_text(100, 7.5, text="Ready")
            return
        except UnicodeDecodeError:
            # Changes background colour of inidicator canvas
            indicator.config(background="#ee2222")
            # Deletes old text
            indicator.delete(indicator_text)
            # Creates text stating that there was an error
            indicator_text = indicator.create_text(100, 7.5, text="Error")
            # creates a message box to state that there was a problem
            messagebox.showinfo("Unicode Decode Error", "Check that the data "
                                "file selected is not a .bin file.")
            # Changes background colour of inidicator canvas
            indicator.config(background="#22ee22")
            # Deletes old text
            indicator.delete(indicator_text)
            # Restored old text stating that the code is ready to generate
            # another report.
            indicator_text = indicator.create_text(100, 7.5, text="Ready")
            return
        # Changes background colour of inidicator canvas back to its normal
        # colour.
        indicator.config(background="#22ee22")
        # Deletes old text
        indicator.delete(indicator_text)
        # States the codeis ready to generate another flight log
        indicator_text = indicator.create_text(100, 7.5, text="Ready")

    # Creates Status Box and sets defult background.
    indicator = tk.Canvas(root, height=15, width=200, bg="#22ee22")
    # Text states code is ready to generate a flight lof
    indicator_text = indicator.create_text(100, 7.5, text="Ready")
    # Places indicator display in the grid.
    indicator.grid(row=15, column=3, columnspan=3)
    # Final row in table for the generate and exit butttons
    generate_button = tk.Button(root, text="Generate .xls file",
                                command=log_reader_input, bg="#22ee22")
    generate_button.grid(row=15, column=0, columnspan=2)

    # Closes the tkinter window.
    def close():
        root.destroy()
    exit_button = tk.Button(root, text="Quit",
                            command=close, width="15", bg="#ee2222")
    exit_button.grid(row=15, column=6, columnspan=2)
    # Makes window size so that it is fixed.
    root.resizable(0, 0)
    root.mainloop()


def log_reader(log_file_path, name_converter_file_path, data_sources_path,
               excel_file_path, excel_file_name, flight_date, flight_number):
    """Creates a formated excell 95 file from a log file. """
    # Creates a new workbook
    workbook = xlwt.Workbook()
    # Opens log file
    log_opened = open(log_file_path, "r")
    # Reads contents
    log_contents_text = log_opened.read()
    # Closes file
    log_opened.close()
    # Opens file
    name_list_opened = open(name_converter_file_path, "r")
    # Reads contents
    name_list_text = name_list_opened.read()
    # Closes file
    name_list_opened.close()
    # Opens file
    data_sources_opened = open(data_sources_path, "r")
    # Reads contents
    data_sources_text = data_sources_opened.read()
    # Closes file
    data_sources_opened.close()
    # Splits text from data sources into individual lines
    data_sources = data_sources_text.split("\n")[1:]
    # splits name list into lines and ignored the first key line.
    name_list = name_list_text.split("\n")[1:]
    # splits log contents about each new line
    log_contents = log_contents_text.split("\n")
    # Goes through each line
    for line in log_contents:
        # Splits data into columns
        data = line.split(", ")
        if data[0] == "FMT":
            # Specifies wether data is available
            data_available = False
            # Checks to see if data was recorded for a particular heading.
            for check_line in log_contents:
                # splits data into lines
                check_line_list = check_line.split(", ")
                # Checks through all data to see if there was any data recorded
                # for a particular variable.
                if data[3] == check_line_list[0]:
                    # Specifies that data is available
                    data_available = True
                    # breaks from for loop
                    break
            if data[3] != "FMT" and data[3] != "UNIT" and data[3] != "FMTU" \
                    and data_available is True and data[3] in data_sources:
                # Creates a new worksheet for all of the data.
                worksheet = workbook.add_sheet(data[3])
                # Sets an index for the columns, starts at 0 and increments by
                # 1.
                column_index = 0
                # Excludes the first time column and puts it at the end.
                data_list_time_end = data[-1].split(",")[1:]
                # Appends time column at the end.
                data_list_time_end.append(data[-1].split(",")[0])
                # Creates the headings and appends the time column to the end
                # to match the format of the previous data sets.
                for heading_name in data_list_time_end:
                    # Code will be here to find the units
                    unit = "unavailable_"
                    # heading name check code will go here.
                    heading = heading_name
                    # Goes throught the names in the name_list to check the
                    # units
                    for name_data in name_list:
                        # splits name list
                        name_info = name_data.split(", ")
                        # Checks to see if the inforamtion in the list matches
                        # that being from the log file
                        if name_info[0] == data[3] and name_info[1] == \
                                heading_name:
                            # Sets heading name to be same as from name
                            heading = name_info[2]
                            # Checks to see if there were units
                            if unit == "no unit":
                                unit = ""
                            else:
                                # Sets unit to be that from name converter list
                                unit = name_info[3] + "_"
                            break
                    # Creates heading from data
                    heading = heading + "_" + unit + data[3] + "_" + \
                        flight_date + "_Flight" + flight_number
                    # writes to worksheet
                    worksheet.write(0, column_index, heading)
                    # Increments column index
                    column_index += 1
                    # Sets row index to 1
                    row_index = 1
                # Goes through all data searching for a match
                for lines in log_contents:
                    # Splits line data
                    line_data = lines.split(", ")
                    #  Checks to see if data name is the one being searched.
                    if line_data[0] == data[3]:
                        # Resets column index to 0
                        column_index = 0
                        # Goes through all data in line, starting from the
                        # column after the time column
                        for recorded_data in line_data[2:]:
                            # Adds data to worksheet
                            worksheet.write(row_index, column_index,
                                            recorded_data)
                            # Increments column index
                            column_index += 1
                        # appends time column to end of list
                        worksheet.write(row_index, column_index, line_data[1])
                        # Increments row index
                        row_index += 1
        else:
            # Ends for loop and so saves code
            break
    # Saves file
    workbook.save(excel_file_path + os.sep + excel_file_name + ".xls")
