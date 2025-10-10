import pytest
from src.build_url import build_seloger_url, build_pap_url

def test_build_seloger_url():
    params = {
        "city": "Paris",
        "max_rent": 1200,
        "min_area": 30,
        "min_rooms": 2
    }
    url = build_seloger_url(params)
    assert "seloger.com" in url
    assert "1200" in url
    assert "30" in url

def test_build_pap_url():
    params = {
        "city": "Paris",
        "max_rent": 1200,
        "min_area": 30,
        "min_rooms": 2
    }
    url = build_pap_url(params)
    assert "pap.fr" in url
    assert "1200" in url
    assert "30" in url