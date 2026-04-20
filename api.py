import requests
from models import Restaurant

API_URL = "https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode"
#MAX_RESTAURANTS = 10


def fetch_restaurants(postcode: str, max_restaurants=10) -> list[Restaurant]:
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
