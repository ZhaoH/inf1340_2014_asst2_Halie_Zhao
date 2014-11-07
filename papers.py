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

    try:
        with open(input_file) as file_reader:
            test_file = file_reader.read()
            test_file = json.loads(test_file)
            print(test_file)
            print(type(test_file))
        with open(watchlist_file) as file_reader:
            watchlist = file_reader.read()
            watchlist = json.loads(watchlist)
            print(watchlist)
            print(type(watchlist))
        with open(countries_file) as file_reader:
            country_list = file_reader.read()
            country_list = json.loads(country_list)
            print(country_list)
            print(type(country_list))
    except:
        print("File not found")
        raise FileNotFoundError

    for entry in test_file:
        # Check if the entry record is complete
        print(valid_date_format(entry["birth_date"]), valid_passport_format(
                entry["passport"]), valid_reason_format(entry[
                    "entry_reason"]), valid_location_format(entry["home"],
                                                               entry["from"]),
              valid_name_format(entry["first_name"], entry[
                    "last_name"]))
        if valid_date_format(entry["birth_date"]) and valid_passport_format(
                entry["passport"]) and valid_reason_format(entry[
                    "entry_reason"]) and valid_location_format(entry["home"],
                                                               entry["from"])\
                and valid_name_format(entry["first_name"], entry[
                    "last_name"]):

            # Check if entry record matches information in country_list
            for country_key, country_val in country_list.items():
                # Check if need quarantine
                if entry["from"]["country"].upper() == country_key and \
                        country_val["medical_advisory"]:
                    mark = ["Quarantine"]
                # Check if need a valid transit or visit visa
                elif entry["home"]["country"].upper() == country_key:
                    if country_val["visitor_visa_required"] == "1" and \
                            entry["entry_reason"] == "visit":
                        print("check visitor visa")
                    elif country_val["transit_visa_required"] == "1" and \
                            entry["entry_reason"] == "transit":
                        print("check transit visa")

            if mark != ["Quarantine"]:
                # Check to see if is a returning citizen
                if entry["entry_reason"] == "returning" and entry["home"][
                        "country"].upper() == "KAN":
                    mark = ["Accept"]

                # check to see if entry record is in watchlist
                for info in watchlist:
                    if entry["passport"].upper() == info["passport"].upper() \
                            or(entry["first_name"].upper() == info[
                                "first_name"].upper() and entry[
                                    "last_name"].upper() == info[
                                        "last_name"].upper()):
                        mark = ["Secondary"]

            result += mark
            mark = ""

        # return reject if entry record is not complete
        else:
            result += ["Reject"]

    print(result)
    return result


def valid_passport_format(passport_number):
    """
    Checks whether a passport number is five sets of
    five alpha-number characters separated by dashes
     :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_format = re.compile('.{5}-.{5}-.{5}-.{5}-.{5}')

    if passport_format.match(passport_number):
        return True
    else:
        print("Invalid passport format")
        return False


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
        return False


def valid_name_format(first_name, last_name):
    """
    Checks whether first name and last name are both complete strings and both use alphabetical characters
    :param first_name: alphabetical string
    :param last_name: alphabetical string
    :return: Boolean; True if valid, False otherwise
    """

    if first_name.isalpha() and last_name.isalpha():
        return True
    else:
        return False


def valid_location_format(home_location, from_location):
    """
    Checks whether home location and from location are on list of existing countries
    :param home_location: predetermined 3-letter country code
    :param from_location: predetermined 3-letter country code
    :return: Boolean; True if valid, False otherwise
    """

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

    reasons_for_entry = ("returning", "transit", "visit")
    if entry_reason in reasons_for_entry:
        return True
    else:
        return False
