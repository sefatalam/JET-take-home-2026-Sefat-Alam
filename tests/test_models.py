from models import Restaurant


def test_parses_complete_restaurant():
    data = {
        "name": "Curry Queen",
        "cuisines": [{"name": "Indian"}, {"name": "Curry"}],
        "rating": {"starRating": 4.5},
        "address": {
            "firstLine": "1 Shenfield Street",
            "city": "London",
            "postalCode": "N1 6SE",
        },
    }

    r = Restaurant.from_api_response(data)

    assert r.name == "Curry Queen"
    assert r.cuisines == ["Indian", "Curry"]
    assert r.rating == 4.5
    assert r.address == "1 Shenfield Street, London, N1 6SE"


def test_missing_name_defaults_to_unknown():
    data = {"cuisines": [], "rating": {}, "address": {}}
    r = Restaurant.from_api_response(data)
    assert r.name == "Unknown"


def test_missing_cuisines_becomes_empty_list():
    data = {"name": "X", "rating": {}, "address": {}}
    r = Restaurant.from_api_response(data)
    assert r.cuisines == []


def test_missing_rating_defaults_to_zero():
    data = {"name": "X", "cuisines": [], "address": {}}
    r = Restaurant.from_api_response(data)
    assert r.rating == 0.0


def test_rating_is_returned_as_float():
    data = {"name": "X", "cuisines": [], "rating": {"starRating": 5}, "address": {}}
    r = Restaurant.from_api_response(data)
    assert isinstance(r.rating, float)
    assert r.rating == 5.0


def test_address_skips_empty_parts():
    data = {
        "name": "X",
        "cuisines": [],
        "rating": {"starRating": 3},
        "address": {"city": "London"},
    }
    r = Restaurant.from_api_response(data)
    assert r.address == "London"


def test_address_all_empty_becomes_empty_string():
    data = {"name": "X", "cuisines": [], "rating": {}, "address": {}}
    r = Restaurant.from_api_response(data)
    assert r.address == ""
