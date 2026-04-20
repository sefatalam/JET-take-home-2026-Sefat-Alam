from models import Restaurant
from display import display_restaurants


def test_displays_all_four_fields(capsys):
    restaurants = [
        Restaurant(
            name="Curry Queen",
            cuisines=["Indian", "Curry"],
            rating=4.5,
            address="1 Shenfield Street, London, N1 6SE",
        )
    ]

    display_restaurants(restaurants)
    out = capsys.readouterr().out

    assert "Curry Queen" in out
    assert "Indian, Curry" in out
    assert "4.5" in out
    assert "1 Shenfield Street, London, N1 6SE" in out


def test_empty_list_shows_message(capsys):
    display_restaurants([])
    out = capsys.readouterr().out

    assert "No restaurants found" in out


def test_multiple_restaurants_all_appear(capsys):
    restaurants = [
        Restaurant(name="Alpha", cuisines=["X"], rating=4.0, address="addr a"),
        Restaurant(name="Bravo", cuisines=["Y"], rating=3.5, address="addr b"),
        Restaurant(name="Charlie", cuisines=["Z"], rating=5.0, address="addr c"),
    ]

    display_restaurants(restaurants)
    out = capsys.readouterr().out

    assert "Alpha" in out
    assert "Bravo" in out
    assert "Charlie" in out


def test_empty_cuisines_shown_as_na(capsys):
    restaurants = [
        Restaurant(name="X", cuisines=[], rating=4.0, address="addr"),
    ]

    display_restaurants(restaurants)
    out = capsys.readouterr().out

    assert "N/A" in out


def test_restaurants_are_numbered(capsys):
    restaurants = [
        Restaurant(name="Alpha", cuisines=[], rating=0, address=""),
        Restaurant(name="Bravo", cuisines=[], rating=0, address=""),
    ]

    display_restaurants(restaurants)
    out = capsys.readouterr().out

    assert "1. Alpha" in out
    assert "2. Bravo" in out
