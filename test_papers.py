#!/usr/bin/env python3

""" Module to test papers.py  """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

"""
This program is used to test each function for "papers.py".
For the decide() function, we added extra tests for it:
1. If the reason for entry is to visit and the visitor has a passport from a country from which a visitor
visa is required, the traveller must have a valid visa.
2. If the reason for entry is transit and the visitor has a passport from a country from which a transit
visa is required, the traveller must have a valid visa.
3. If the person only has last name and first name on watchlist without passport number on watchlist.
4. If the person did not come from the country with medical advisory but went via the country with medical advisory.
Additionally, we added the test cases for the functions valid_passport_format() and valid_date_format();
"""
# imports one per line
import papers
from papers import decide
from papers import valid_date_format
from papers import valid_passport_format


def test_basic():
    assert decide("test_returning_citizen.json", "watchlist.json", "countries.json") == ["Accept", "Accept"]
    assert decide("test_watchlist.json", "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_quarantine.json", "watchlist.json", "countries.json") == ["Quarantine"]


def test_files():
    FileNotFoundError = IOError
    with papers.raises(FileNotFoundError):
        decide("test_returning_citizen.json", "", "countries.json")

def test_visa_valid():# Test the person who come to a country which needs visa but his visa is invalid.
    assert decide("test_vistor_visa_expired.json", "watchlist.json", "countries.json") == ["Reject"] #came from CFR (this country needs vistor visa)
    assert decide("test_transit_visa_expired.json", "watchlist.json", "countries.json") == ["Reject"] #came from LUG (I personally changed the vistor_visa_required for LUG to 0 for convenient test)

def test_secondary():# Test the person who only have last name and first name on watchlist without passport number on watchlist.
    assert decide("test_secondary.json", "watchlist.json", "countries.json") == ["Reject"]# First name:LIBBIE Last name: Lusk.


def test_quarantine_for_via():#Test the person who did not come from the country with medical advisory but went via the country with medical advisory.
    assert decide("test_quarantine_via.json", "watchlist.json", "countries.json") == ["Quarantine"]

def test_valid_passport_format():#Test the function for valid passport format
    assert valid_passport_format("R7XRX-8AON6-RAM13-W0UPF-TT7BT") == True
    assert valid_passport_format("R7XRX-8AON6-RAM13-W0UPF-TT7BT-TD37A")  == False

def test_valid_date_format():#Test the function for valid date format
    assert valid_date_format("2014-04-30") == True
    assert valid_date_format("20140430") == False



