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
    assert decide("test_returning_citizen.json", "watchlist.json", "countries.json") == ["Accept", "Accept"],"Work"
    assert decide("test_watchlist.json", "watchlist.json", "countries.json") == ["Secondary"],"Work"
    assert decide("test_quarantine.json", "watchlist.json", "countries.json") == ["Quarantine"],"Work"


def test_files():
    FileNotFoundError = IOError
    with papers.raises(FileNotFoundError):
        decide("test_returning_citizen.json", "", "countries.json")

# add functions for other tests

