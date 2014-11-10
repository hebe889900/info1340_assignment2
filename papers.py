#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """

__author__ = 'Susan Sim'
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
    with open(input_file, "r") as file_reader_input:
        file_contents_input = file_reader_input.read()
        json_contents_input_in_list = json.loads(file_contents_input)

    with open(watchlist_file, "r") as file_reader_watchlist:
        file_contents_watchlist = file_reader_watchlist.read()
        json_contents_watchlist_in_list = json.loads(file_contents_watchlist)

    with open(countries_file, "r") as file_reader_countries:
        file_contents_countries = file_reader_countries.read()
        json_contents_countries_in_dictionary = json.loads(file_contents_countries)

    string_result = [] #Create an empty string list to store the different output results.


    # If the required information for an entry record is incomplete, the traveler must be rejected.
    for entry_dictionary in json_contents_input_in_list:
        if set(["passport","first_name","last_name","birth_date","home","from","entry_reason"]).issubset(entry_dictionary)is False:
                return ["Reject"]


        year = datetime.timedelta(days=365)
        two_years = 2*year



        home_dictionary = entry_dictionary["home"]

        home_dictionary = dict((k.lower(), v.lower()) for k, v in home_dictionary.iteritems())# Make the home dictionary inside the whole dictionary to lowercase



    #If the reason for entry is to visit and the visitor has a passport from a country from which a visitor visa is required,
    # the traveller must have a valid visa. A valid visa is one that is less than two years old.
        if json_contents_countries_in_dictionary[entry_dictionary["from"]["country"]]["visitor_visa_required"] == "1":
            if "visa" in entry_dictionary.keys():
                if datetime.datetime.now() - datetime.datetime.strptime(entry_dictionary["visa"]["visa_date"], '%Y-%m-%d')  >=  two_years:
                    string_result.append("Reject")
                    continue

    #If the reason for entry is transit and the visitor has a passport from a country from which a transit visa is required,
    # the traveller must have a valid visa. A valid visa is one that is less than two years old.
        if json_contents_countries_in_dictionary[entry_dictionary["from"]["country"]]["transit_visa_required"] == "1":
            if "visa" in entry_dictionary.keys():
                if  datetime.datetime.now() - datetime.datetime.strptime(entry_dictionary["visa"]["visa_date"], '%Y-%m-%d')  >=  two_years:
                    string_result.append("Reject")
                    continue

    #If the traveler is coming from or via a country that has a medical advisory, he or she must be send to quarantine.
        for countries_dictionary in json_contents_countries_in_dictionary:
            key_code_country = entry_dictionary["from"]["country"]
            if (json_contents_countries_in_dictionary[key_code_country]["medical_advisory"] == "") is False:
                string_result.append("Quarantine")
                break

            if "via" in entry_dictionary:
                if (json_contents_countries_in_dictionary[entry_dictionary["via"]["country"]]["medical_advisory"] == "" )is False:
                    string_result.append("Quarantine")
                    break
            continue
    #If the traveller has a name or passport on the watch list, she or he must be sent to secondary processing.

        for watchlist_dictionary in json_contents_watchlist_in_list:
            #ignore cases
            entry_dictionary["passport"] = entry_dictionary["passport"].lower();
            entry_dictionary["last_name"] = entry_dictionary["last_name"].lower();
            entry_dictionary["first_name"] = entry_dictionary["first_name"].lower();
            watchlist_dictionary = dict((k.lower(), v.lower()) for k,v in watchlist_dictionary.iteritems())# Make each item in watchlist to lowercase
            if entry_dictionary["passport"] == watchlist_dictionary["passport"]:
                string_result.append("Secondary")
                continue

            if entry_dictionary["last_name"] == watchlist_dictionary["last_name"]:
                if entry_dictionary["first_name"] == watchlist_dictionary["first_name"]:
                    string_result.append("Secondary")
                    continue

            continue
        continue

        if home_dictionary["country"] == "kan":
            if entry_dictionary["entry_reason"] == "returning":
                string_result.append("Accept")
                continue

        string_result.append("Reject")
        continue
    return string_result





def valid_passport_format(passport_number):
    """
    Checks whether a pasport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_format =  re.compile('^\w{5}-\w{5}$')

    if passport_format.match(passport_number):
        return True
    else:
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


