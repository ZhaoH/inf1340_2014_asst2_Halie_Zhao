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


def decide(input_file, watchlist_file, countries_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains cases to decide
    :param watchlist_file: The name of a JSON formatted file that contains names and passport numbers on a watchlist
    :param countries_file: The name of a JSON formatted file that contains country data, such as whether
        an entry or transit visa is required, and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are: "Accept", "Reject", "Secondary", and "Quarantine"
    """

    mark = ""
    result = []

    #Read test_file, watchlist, country_list from JSON files
    try:
        with open(input_file) as file_reader:
            test_file = file_reader.read()
            test_file = json.loads(test_file)
        with open(watchlist_file) as file_reader:
            watchlist = file_reader.read()
            watchlist = json.loads(watchlist)
        with open(countries_file) as file_reader:
            country_list = file_reader.read()
            country_list = json.loads(country_list)
    except:
        print("File not found")
        raise FileNotFoundError

    for entry in test_file:
        # Check if the entry record is complete
        if valid_date_format(entry["birth_date"]) and \
                valid_passport_format(entry["passport"]) and \
                valid_reason_format(entry["entry_reason"]) and \
                valid_location_format(entry["home"], entry["from"])and \
                valid_name_format(entry["first_name"], entry["last_name"]):

            # Check if entry record matches information in country_list
            for country_key, country_val in country_list.items():
                # Check if need quarantine
                if entry["from"]["country"].upper() == country_key and \
                        country_val["medical_advisory"]:
                    mark = ["Quarantine"]

                # Check if traveller needs a valid transit or visit visa
                elif entry["home"]["country"].upper() == country_key:
                    if (country_val["visitor_visa_required"] == "1" and
                        entry["entry_reason"] == "visit") or (country_val[
                            "transit_visa_required"] == "1" and
                            entry["entry_reason"] == "transit"):
                        # Check if the visa is valid
                        if valid_visa(entry["visa"]):
                            mark = ["Accept"]
                        else:
                            mark = ["Reject"]
                    else:
                        mark = ["Accept"]

            if mark != ["Quarantine"]:
                # Check to see if traveller is a returning citizen
                if entry["entry_reason"] == "returning" and \
                                entry["home"]["country"].upper() == "KAN":
                    mark = ["Accept"]

                # Check to see if entry record is in watchlist
                for info in watchlist:
                    if entry["passport"].upper() == info["passport"].upper()\
                            or(entry["first_name"].upper() == info[
                                "first_name"].upper() and
                                entry["last_name"].upper() == info[
                            "last_name"].upper()):
                        mark = ["Secondary"]

            result += mark
            mark = ""

        # Return reject if entry record is not complete
        else:
            result += ["Reject"]

    return result


def valid_passport_format(passport_number):
    """
    Checks whether a passport number is five sets of
    five alpha-number characters separated by dashes
     :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    # Checks to see if passport number is correct format
    passport_format = re.compile('^\w{5}-\w{5}-\w{5}-\w{5}-\w{5}$')

    if passport_format.match(passport_number):
        return True
    else:
        return False


def valid_visa(visa):
    """
    Checks whether a visa data is two sets of five alpha-number characters
    separated by dashes and is less than two years old
     :param visa: alpha-numeric string
    :return: Boolean; True if the format is valid and not expired,
    False otherwise
    """
    # Checks to see if visa is correct format
    visa_format = re.compile('^\w{5}-\w{5}$')

    # Check if the visa is in valid format
    if visa_format.match(visa["code"]) and valid_date_format(visa["date"]):
        # Check if the visa is less than 2 years old
        if (datetime.datetime.today() - datetime.datetime.strptime(
                visa["date"], "%Y-%m-%d")) < datetime.timedelta(730):
            return True
        else:
            return False
    else:
        return False


def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """
    # Checks to see if date is in correct format
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def valid_name_format(first_name, last_name):
    """
    Checks whether first name and last name both use alphabetical characters
    :param first_name: alphabetical string
    :param last_name: alphabetical string
    :return: Boolean; True if valid, False otherwise
    """
    # Checks to see if first an last name are in correct alphabetical
    # character format
    if first_name.isalpha() and last_name.isalpha():
        return True
    else:
        return False


def valid_location_format(home_location, from_location):
    """
    Checks whether home location and from location are on list of existing
    countries
    :param home_location: predetermined 3-letter country code
    :param from_location: predetermined 3-letter country code
    :return: Boolean; True if valid, False otherwise
    """
    # Checks to see whether both the home country and from country are on the
    # preapproved list of countries
    preapproved_countries = ("ALB", "BRD", "CFR", "DSK", "ELE", "FRY", "GOR",
                             "HJR", "III", "JIK", "KAN", "KRA", "LUG")
    if home_location["country"].upper() in preapproved_countries and \
            from_location["country"].upper() in preapproved_countries:
        return True
    else:
        return False


def valid_reason_format(entry_reason):
    """
    Checks whether reason for entry either returning, transit, or visa
    :param entry_reason: returning, transit, or visa
    :return: Boolean; True if valid, False otherwise
    """
    # Checks to see whether entry reason returning, transit, or visit
    reasons_for_entry = ("returning", "transit", "visit")
    if entry_reason in reasons_for_entry:
        return True
    else:
        return False
