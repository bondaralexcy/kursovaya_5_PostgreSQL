import pytest
from src.utils import *


def test_clear_string():
    assert clear_string('any <p>string \rfor filter\n') == 'any string for filter'


def test_detect_salary():
    assert detect_salary(None) is None

    assert detect_salary({
        'from': 10,
        'to': 20
    }) == 10

    assert detect_salary({
        'from': 10,
        'to': None
    }) == 10

    assert detect_salary({
        'from': None,
        'to': 10
    }) == 10


