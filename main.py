import sys
from api import fetch_restaurants
from display import display_restaurants


def main():
    """CLI entry point: read a postcode, fetch restaurants, display them.

    The postcode is taken from command-line arguments if provided, otherwise
    prompted for interactively. It is normalised (whitespace stripped,
    uppercased) before being sent to the API. Errors from the API or network
    are caught and reported with a non-zero exit code.
    """
    if len(sys.argv) > 1:
        postcode = " ".join(sys.argv[1:])
    else:
        postcode = input("Enter a UK postcode: ")

    postcode = "".join(postcode.split()).upper()

    if not postcode:
        print("Error: No postcode provided.")
        sys.exit(1)

    try:
        restaurants = fetch_restaurants(postcode)
        display_restaurants(restaurants)
    except Exception as e:
        print(f"Error fetching restaurants: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
