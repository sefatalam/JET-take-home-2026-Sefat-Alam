from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from models import Restaurant


console = Console()


def _rating_colour(rating: float) -> str:
    if rating >= 4.5:
        return "bold green"
    if rating >= 3.0:
        return "yellow"
    return "red"


def _build_panel(index: int, r: Restaurant) -> Panel:
    cuisines_str = ", ".join(r.cuisines) if r.cuisines else "N/A"

    body = Text()
    body.append("Cuisines: ", style="bold")
    body.append(f"{cuisines_str}\n")
    body.append("Rating:   ", style="bold")
    body.append(f"{r.rating}", style=_rating_colour(r.rating))
    body.append("\n")
    body.append("Address:  ", style="bold")
    body.append(r.address)

    return Panel(
        body,
        title=f"[bold cyan]{index}. {r.name}[/bold cyan]",
        title_align="left",
        box=box.ROUNDED,
        padding=(0, 1),
    )


def display_restaurants(restaurants: list[Restaurant]) -> None:
    if not restaurants:
        console.print("[yellow]No restaurants found for this postcode.[/yellow]")
        return

    console.print(f"\n[bold]Found {len(restaurants)} restaurant(s):[/bold]\n")

    for i, r in enumerate(restaurants, start=1):
        console.print(_build_panel(i, r))
