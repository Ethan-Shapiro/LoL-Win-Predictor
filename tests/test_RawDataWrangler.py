import pytest

from src import RawDataWrangler

region = 'na1'
username = 'Sasheemy'

def test_rawdatawrangler():
    assert type(RawDataWrangler(region, username)) == RawDataWrangler

print("In module products __package__, __name__ ==", __package__, __name__)

