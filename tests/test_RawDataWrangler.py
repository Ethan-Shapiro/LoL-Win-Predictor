import pytest

from src.RawDataWrangler import RawDataWrangler

region = 'na1'
username = 'Sasheemy'


def test_rawdatawrangler():
    assert type(RawDataWrangler(region, username)) == RawDataWrangler
