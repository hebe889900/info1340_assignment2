#!/usr/bin/env python3

""" Module to test papers.py  """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

"""
This program is used to test each functions in "papers.py".
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
    FileNotFoundError = IOError # Raises FileNotFoundError if there is IO error.
    with papers.raises(FileNotFoundError):
        decide("test_returning_citizen.json", "", "countries.json")

# Determines if visitor who come from a country which needs visa if his visa is invalid.
def test_visa_valid():
    assert decide("test_vistor_visa_expired.json", "watchlist.json", "countries.json") == ["Reject"]
    # Came from CFR (this country needs visitor visa)
    assert decide("test_transit_visa_expired.json", "watchlist.json", "countries.json") == ["Reject"]
    # Came from LUG (I personally changed the visitor_visa_required for LUG to 0 for convenient test)

# Test to reject the person who only have last name and first name on watchlist without passport number on watchlist.
def test_secondary():
    assert decide("test_secondary.json", "watchlist.json", "countries.json") == ["Secondary"]
    # First name:LIBBIE Last name: Lusk.

#Test travelers who did not come from the country with medical advisory but went via the country with medical advisory.
def test_quarantine_for_via():
    assert decide("test_quarantine_via.json", "watchlist.json", "countries.json") == ["Quarantine"]

#Test the function for valid passport format
def test_valid_passport_format():
    assert valid_passport_format("R7XRX-8AON6-RAM13-W0UPF-TT7BT") == True
    assert valid_passport_format("R7XRX-8AON6-RAM13-W0UPF-TT7BT-TD37A")  == False

#Test the function for valid date format
def test_valid_date_format():
    assert valid_date_format("2014-04-30") == True
    assert valid_date_format("20140430") == False



