from unittest.mock import patch, Mock

import pytest
import requests

from api import fetch_restaurants


def _fake_restaurant(i: int) -> dict:
    return {
        "name": f"Restaurant {i}",
        "cuisines": [],
        "rating": {"starRating": 0},
        "address": {},
    }


def _mock_response(json_data: dict) -> Mock:
    mock = Mock()
    mock.json.return_value = json_data
    mock.raise_for_status.return_value = None
    return mock


@patch("api.requests.get")
def test_returns_first_10_restaurants_by_default(mock_get):
    mock_get.return_value = _mock_response(
        {"restaurants": [_fake_restaurant(i) for i in range(20)]}
    )

    result = fetch_restaurants("EC4M7RF")

    assert len(result) == 10
    assert result[0].name == "Restaurant 0"
    assert result[9].name == "Restaurant 9"


@patch("api.requests.get")
def test_returns_empty_list_when_no_restaurants(mock_get):
    mock_get.return_value = _mock_response({"restaurants": []})

    result = fetch_restaurants("EC4M7RF")

    assert result == []


@patch("api.requests.get")
def test_returns_empty_list_when_key_missing(mock_get):
    mock_get.return_value = _mock_response({})

    result = fetch_restaurants("EC4M7RF")

    assert result == []


@patch("api.requests.get")
def test_postcode_is_cleaned_in_url(mock_get):
    mock_get.return_value = _mock_response({"restaurants": []})

    fetch_restaurants("ec4m 7rf")

    called_url = mock_get.call_args[0][0]
    assert called_url.endswith("/EC4M7RF")


@patch("api.requests.get")
def test_postcode_with_multiple_spaces_is_cleaned(mock_get):
    mock_get.return_value = _mock_response({"restaurants": []})

    fetch_restaurants("  EC4M  7RF  ")

    called_url = mock_get.call_args[0][0]
    assert called_url.endswith("/EC4M7RF")


@patch("api.requests.get")
def test_respects_max_restaurants_parameter(mock_get):
    mock_get.return_value = _mock_response(
        {"restaurants": [_fake_restaurant(i) for i in range(20)]}
    )

    result = fetch_restaurants("EC4M7RF", max_restaurants=5)

    assert len(result) == 5


@patch("api.requests.get")
def test_returns_all_when_fewer_than_max(mock_get):
    mock_get.return_value = _mock_response(
        {"restaurants": [_fake_restaurant(i) for i in range(3)]}
    )

    result = fetch_restaurants("EC4M7RF")

    assert len(result) == 3


@patch("api.requests.get")
def test_raises_on_http_error(mock_get):
    mock = Mock()
    mock.raise_for_status.side_effect = requests.HTTPError("403 Forbidden")
    mock_get.return_value = mock

    with pytest.raises(requests.HTTPError):
        fetch_restaurants("EC4M7RF")


@patch("api.requests.get")
def test_sends_user_agent_header(mock_get):
    mock_get.return_value = _mock_response({"restaurants": []})

    fetch_restaurants("EC4M7RF")

    headers = mock_get.call_args.kwargs["headers"]
    assert "User-Agent" in headers
