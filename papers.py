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
    #json.contents.input contains the list of travelers attempting to enter Kanadia's border
    with open(input_file, "r") as file_reader_input:
        file_contents_input = file_reader_input.read()
        json_contents_input_in_list = json.loads(file_contents_input)
    #json.contents.watchlist contains all travelers on the watchlist which means they can go to "secondary"
    with open(watchlist_file, "r") as file_reader_watchlist:
        file_contents_watchlist = file_reader_watchlist.read()
        json_contents_watchlist_in_list = json.loads(file_contents_watchlist)
    #jason.contents_countries contains list of countries in the game
    #all the possible countries visitors can be from and traveling from
    with open(countries_file, "r") as file_reader_countries:
        file_contents_countries = file_reader_countries.read()
        json_contents_countries_in_dictionary = json.loads(file_contents_countries)


     #An entry should not be rejected if there is a mismatch between uppercase and lowercase.
     # the case of the country code and passport numbers should not matter
     # For example, "ELE" and "ele" treated as identical values
     # Thus all values are alphabetical converted to lowercase to prevent lowercase and uppercase differentiation
    for value_in_input in json_contents_input_in_list:
        if isinstance(value_in_input,str):
            value_in_input = value_in_input.lower()
            #converts every string in the list to lowercase;
    for value_in_watchlist in json_contents_watchlist_in_list:
        if isinstance(value_in_watchlist,str):
            value_in_watchlist = value_in_watchlist.lower()
            #converts every string in the list to lowercase;
    for key_in_countries in json_contents_countries_in_dictionary.keys():
        key_in_countries = key_in_countries.lower();
        #converts every string key in the dictionary to lowercase;
    for value_in_countries in json_contents_countries_in_dictionary.values():
        if isinstance(value_in_countries,str):
            value_in_countries = value_in_countries.lower();
            #converts every string value in the dictionary to lowercase;

    #If the required information for an entry record is incomplete, the traveler must be rejected.
    #If passport number is missing, then traveler must be rejected regardless of whether he or she met other conditions
    #converting string,string key to lowercase prevents differentiation between lowercase and uppercase
    #for example: "first_name": "vanessa" and "first_name": "VANESSA" are the same
    for entry_dictionary in json_contents_input_in_list:
        for key_in_entry_dictionary in entry_dictionary.keys():
            key_in_entry_dictionary = key_in_entry_dictionary.lower();
            #converts every string key in the dictionary to lowercase;
        for value_in_entry_dictionary in entry_dictionary.values():
            if isinstance(value_in_entry_dictionary,str):
                value_in_entry_dictionary = value_in_entry_dictionary.lower();
                #converts every string in the sub-dictionary of the entry record to lowercase;
        if set(["passport","first_name","last_name","birth_date","home","from","entry_reason"]).issubset(entry_dictionary)is False:
                return ["Reject"]

            # Assign the string to each key.
        key_passport = "passport"
        key_first_name = "first_name"
        key_last_name = "last_name"
        key_birth_date = "birth_date"
        key_home = "home"
        key_from = "from"
        key_from_country = "country"
        key_entry_reason = "entry_reason"
        key_via = "via"
        key_via_country = "country"
        key_visa = "visa"
        key_visa_date = "date"
        key_country_in_home = "country"
        key_medical_advisory = "medical_advisory"
        key_visitor_visa_required = "visitor_visa_required"
        key_transit_visa_required = "transit_visa_required"




        home_dictionary = entry_dictionary[key_home];

        for key_in_home_dictionary in home_dictionary.keys():
            key_in_home_dictionary = key_in_home_dictionary.lower();
            #converts every string key in the dictionary to lowercase;
        for value_in_home_dictionary in home_dictionary.values():
            if isinstance(value_in_home_dictionary,str):
                value_in_home_dictionary = value_in_home_dictionary.lower();
                #converts every string in the sub-dictionary of the entry record to lowercase;


        if home_dictionary[key_country_in_home] == "KAN":
            if entry_dictionary[key_entry_reason] == "returning":
                return ["Accept"]

    #If the traveller has a name or passport on the watch list, she or he must be sent to secondary processing.
    #json.contents,watchlist contains travelers on the watchlist
    #firs name, last name, passport and other information must all match with traveler information on the watchlist
        for watchlist_dictionary in json_contents_watchlist_in_list:
            #converts dictionary values to lowercase to prevent differentiation between upper and lowercase
            watchlist_dictionary = [dict((k.lower(), v.lower()) for k,v in watchlist_dictionary.iteritems())]
            if entry_dictionary[key_passport] in watchlist_dictionary:
                return ["Secondary"]

            if entry_dictionary[key_last_name] in watchlist_dictionary:
                if entry_dictionary[key_first_name] in watchlist_dictionary:
                    return ["Secondary"]

    #If the traveler is coming from or via a country that has a medical advisory, he or she must be send to quarantine.
        for countries_dictionary in json_contents_countries_in_dictionary:
            key_code_country = entry_dictionary[key_from][key_from_country]
            if json_contents_countries_in_dictionary[key_code_country][key_medical_advisory].isspace is False:
                return ["Quarantine"]

            if key_via in entry_dictionary:
                if json_contents_countries_in_dictionary[entry_dictionary[key_via][key_from_country]][key_medical_advisory].isspace is False:
                    return ["Quarantine"]

    #If the reason for entry is to visit and the visitor has a passport from a country from which a visitor visa is required,
    #The traveller must have a valid visa. A valid visa is one that is less than two years old.
                if json_contents_countries_in_dictionary[entry_dictionary[key_via][key_from_country]][key_visitor_visa_required] == 1:
                    if key_visa in entry_dictionary:
                        if entry_dictionary[key_visa][key_visa_date].date().day- datetime.datetime.now().day > 2*365:
                            return ["Reject"]

    #If the reason for entry is transit and the visitor has a passport from a country from which a transit visa is required,
    #the traveller must have a valid visa. A valid visa is one that is less than two years old.
                if json_contents_countries_in_dictionary[entry_dictionary[key_via][key_via_country]][key_transit_visa_required] == 1:
                    if key_visa in entry_dictionary:
                        if entry_dictionary[key_visa][key_visa_date].date().day- datetime.datetime.now().day > 2*365:
                            return ["Reject"]


#An entry should not be rejected if there is a mismatch between uppercase and lowercase.
#The case of the country code and passport numbers should not matter.
#For example: "LUG" is identical to "lug"
print(decide("test_returning_citizen.json", "watchlist.json", "countries.json"))






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
