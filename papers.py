#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """

__author__ = 'Susan Sim'
__author__ = 'Zhao'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"


# imports one per line
import re
import datetime
import json

#test

def decide(input_file, watchlist_file, countries_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains cases to decide
    :param watchlist_file: The name of a JSON formatted file that contains names and passport numbers on a watchlist
    :param countries_file: The name of a JSON formatted file that contains country data, such as whether
        an entry or transit visa is required, and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are: "Accept", "Reject", "Secondary", and "Quarantine"
    """
    return ["Reject"]

def passport_attributes_complete(valid_passport_format, valid_date_format, valid_name_format, valid_location_format, valid_entry_format):
    """

    :param valid_passport_format:
    :param valid_date_format:
    :param valid_name_format:
    :param valid_location_format:
    :param valid_entry_format:
    :return:
    """
    # Determines whether all attributes (First Name, Last Name, Birth Date, Passport Number, Home Location, From Location, Reason for Entry)
    # are complete, returns True
    # call valid_date_format and valid_passport_format

def valid_passport_format(passport_number):
    """
    Checks whether a passport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_format = re.compile('.{5}-.{5}-.{5}-.{5}-.{5}')

    if passport_format.match(passport_number):
        return True
    else:
        return False
  # if type(passport_number) is not str:
    #    raise TypeError("Invalid Type")
    # if len(passport_number) != 25:
     #   raise ValueError("Incorrect length")

def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        if type(date_string) is not str:
            raise TypeError("Invalid Type")
        if len(date_string) != 8:
            raise ValueError("Incorrect length")
        return False


def valid_name_format(first_name, last_name):
    """
    Checks whether first name and last name are both complete strings and both use alphabetical characters
    :param first_name: alphabetical string
    :param last_name: alphabetical string
    :return: Boolean; True if valid, False otherwise
    """

    if (len(first_name), len(last_name)) > 1 and (type(first_name), type(last_name)) = (str, str) and (first_name.isalpha()) and (last_name.isalpha()):
        return True
    else:
        return False

       # raise TypeError("Invalid Type: Names must be strings")

def valid_location_format(home_location, from_location):
    """
    Checks whether home location and from location are on list of existing countries
    :param home_location: predetermined 3-letter country code
    :param from_location: predetermined 3-letter country code
    :return: Boolean; True if valid, False otherwise
    """

    preapproved_countries = ("ALB", "BRD", "CFR", "DSK", "ELE", "FRY", "GOR", "HJR",\
                 "III", "JIK", "KAN", "KRA", "LUG")
    if home_location in preapproved_countries and from_location in preapproved_countries:
        return True
    else:
        return False

def valid_entry_format(entry_reason):
    """
    Checks whether reason for entry either returning, transit, or visa
    :param entry_reason: returning, transit, or visa
    :return: Boolean; True if valid, False otherwise
    """

    reasons_for_entry = ("returning", "transit", "visa")
    if entry_reason in reasons_for_entry:
        return True
    else:
        return False
