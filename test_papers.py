#!/usr/bin/env python3

""" Module to test papers.py  """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import papers
from papers import decide


def test_basic():
    assert decide("test_returning_citizen.json", "watchlist.json", "countries.json") == ["Accept", "Accept"]
    assert decide("test_watchlist.json", "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_quarantine.json", "watchlist.json", "countries.json") == ["Quarantine"]


def test_files():
    FileNotFoundError = IOError
    with papers.raises(FileNotFoundError):
        decide("test_returning_citizen.json", "", "countries.json")

def test_visa_valid():
    assert decide("test_vistor_visa_expired.json", "watchlist.json", "countries.json") == ["Reject"] #from CFR
    assert decide("test_transit_visa_expired.json", "watchlist.json", "countries.json") == ["Reject"]
    #from LUG (I personally changed the visitor_visa_required for LUG to 0 for convenient testing)

def test_secondary():
    assert decide("test_secondary.json", "watchlist.json", "countries.json") == ["Reject"]
    # Tests the person who only have last name and first name on watchlist without passport number on watchlist
    # For example: First name:LIBBIE Last name: Lusk




# add functions for other tests

