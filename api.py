import requests
from models import Restaurant

API_URL = "https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode"
#MAX_RESTAURANTS = 10


def fetch_restaurants(postcode: str, max_restaurants=10) -> list[Restaurant]:
    """Fetch restaurants for the given UK postcode from the Just Eat API.

    The postcode is normalised (whitespace stripped, uppercased) before the
    request. A `User-Agent` header is required as the API rejects the default
    `requests` user-agent with 403.

    Args:
        postcode: A UK postcode, with or without spaces (e.g. "EC4M 7RF").
        max_restaurants: Cap on how many restaurants to return. Defaults to 10.

    Returns:
        A list of Restaurant objects, up to `max_restaurants` long.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    cleaned_postcode = "".join(postcode.split()).upper()
    url = f"{API_URL}/{cleaned_postcode}"

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    restaurants_data = data.get("restaurants", [])

    result_restaurants = []
    for r in restaurants_data[:max_restaurants]:
        result_restaurants.append(Restaurant.from_api_response(r))
    
    return result_restaurants
