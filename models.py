from dataclasses import dataclass


@dataclass
class Restaurant:
    """Represents a single restaurant with only the fields we care about for display."""

    name: str
    cuisines: list[str]
    rating: float
    address: str

    @classmethod
    def from_api_response(cls, data: dict) -> "Restaurant":
        """Build a Restaurant from a single entry in the API's `restaurants` array.

        Missing fields fall back to sensible defaults ("Unknown", empty list,
        0.0, empty string) so a malformed entry never crashes the app.
        """
        name = data.get("name", "Unknown")

        cuisines = [c["name"] for c in data.get("cuisines", [])]

        rating = data.get("rating", {}).get("starRating", 0.0)

        address_data = data.get("address", {})
        address_parts = [
            address_data.get("firstLine", ""),
            address_data.get("city", ""),
            address_data.get("postalCode", ""),
        ]
        address = ", ".join(part for part in address_parts if part)

        return cls(
            name=name,
            cuisines=cuisines,
            rating=float(rating),
            address=address,
        )
