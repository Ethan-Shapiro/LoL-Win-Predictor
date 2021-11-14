import pytest

from src.RawDataWrangler import RawDataWrangler

region = 'na1'
username = 'Sasheemy'


def test_constructor():
    assert type(RawDataWrangler(region, username)) == RawDataWrangler


rdw = RawDataWrangler(region, username)


def test_set_region():
    assert rdw.set_region('notvalid1') == False
    assert rdw.set_region('na1') == True
    assert rdw.set_region('br1') == True


def test_get_raw_match_timelines():
    pass
