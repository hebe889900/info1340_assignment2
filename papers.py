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
        json_contents_input = json.loads(file_contents_input)

    with open(watchlist_file, "r") as file_reader_watchlist:
        file_contents_watchlist = file_reader_watchlist.read()
        json_contents_watchlist = json.loads(file_contents_watchlist)

    with open(countries_file, "r") as file_reader_countries:
        file_contents_countries = file_reader_countries.read()
        json_contents_countries = json.loads(file_contents_countries)


     #An entry should not be rejected if there is a mismatch between uppercase and lowercase. For example, the case of the country code and passport numbers should not matter.
    json_contents_input = [x.lower() for x in json_contents_input]
    json_contents_watchlist = [x.lower() for x in json_contents_watchlist]
    json_contents_countries = [dict((k.lower(), v.lower()) for k,v in json_contents_countries.iteritems())]

    # If the required information for an entry record is incomplete, the traveler must be rejected.
    for entry_dictionary in json_contents_input:
         #An entry should not be rejected if there is a mismatch between uppercase and lowercase. For example, the case of the country code and passport numbers should not matter.
        entry_dictionary = [dict((k.lower(), v.lower()) for k,v in entry_dictionary.iteritems())]

        if set(["passport","first_name","last_name","birth_date","home","from","entry_reason"]).issubset(entry_dictionary)is False:
                return ["Reject"]

            # Assign the string to each key.
        key_passport = "passport"
        key_first_name = "first_name"
        key_last_name = "last name"
        key_birth_date = "birth_date"
        key_home = "home"
        key_from = "from"
        key_entry_reason = "entry_reason"
        key_via = "via"
        key_visa = "visa"
        key_visa_date = "date"
        key_country = "country"
        key_medical_advisory = "medical_advisory"
        key_visitor_visa_required = "visitor_visa_required"
        key_transit_visa_required = "transit_visa_required"


    #A traveller who is returning and home country is ”KAN” will be accepted, unless some other condition holds.

        if key_home in file_contents_input:
            if key_entry_reason in file_contents_input:
                if "kan" in entry_dictionary[key_home]:
                    if "returning" in entry_dictionary[key_entry_reason]:
                        return ["Accept"]

    #If the traveller has a name or passport on the watch list, she or he must be sent to secondary processing.
        for watchlist_dictionary in file_contents_watchlist:
            #ignore cases
            watchlist_dictionary = [dict((k.lower(), v.lower()) for k,v in watchlist_dictionary.iteritems())]
            if entry_dictionary[key_passport] in watchlist_dictionary:
                return ["Secondary"]

            if entry_dictionary[key_last_name] in watchlist_dictionary:
                if entry_dictionary[key_first_name] in watchlist_dictionary:
                    return ["Secondary"]

    #If the traveler is coming from or via a country that has a medical advisory, he or she must be send to quarantine.
        for countries_dictionary in file_contents_countries:
            #ignore cases
            countries_dictionary = [dict((k.lower(), v.lower()) for k,v in countries_dictionary.iteritems())]
            if countries_dictionary[entry_dictionary[key_from][key_country]][key_medical_advisory].isspace is False:
                return ["Quarantine"]

            if key_via in entry_dictionary:
                if countries_dictionary[entry_dictionary[key_via][key_country]][key_medical_advisory].isspace is False:
                    return ["Quarantine"]

    #If the reason for entry is to visit and the visitor has a passport from a country from which a visitor visa is required,
    # the traveller must have a valid visa. A valid visa is one that is less than two years old.
                if countries_dictionary[entry_dictionary[key_via][key_country]][key_visitor_visa_required] == 1:
                    if key_visa in entry_dictionary:
                        if entry_dictionary[key_visa][key_visa_date].date().day- datetime.datetime.now().day > 2*365:
                            return ["Reject"]

    #If the reason for entry is transit and the visitor has a passport from a country from which a transit visa is required,
    # the traveller must have a valid visa. A valid visa is one that is less than two years old.
                if countries_dictionary[entry_dictionary[key_via][key_country]][key_transit_visa_required] == 1:
                    if key_visa in entry_dictionary:
                        if entry_dictionary[key_visa][key_visa_date].date().day- datetime.datetime.now().day > 2*365:
                            return ["Reject"]

    #An entry should not be rejected if there is a mismatch between uppercase and lowercase. For example, the case of the country code and passport numbers should not matter.
    #If the reason for entry is returning home and the traveller’s home country is Kanadia (country code: KAN), the traveller will be accepted.







def valid_passport_format(passport_number):
    """
    Checks whether a pasport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_format = re.compile('.{5}-.{5}-.{5}-.{5}-.{5}')

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