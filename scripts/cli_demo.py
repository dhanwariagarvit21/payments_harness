import httpx
import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def check(item: str, price: float):
    r = httpx.post(
        "http://127.0.0.1:8000/evaluate",
        json={"user_id": "u1", "item": item, "price": price},
    )
    data = r.json()
    color = {"approve": "green", "reauth": "yellow", "block": "red"}.get(data["decision"], "white")
    console.print(f"[{color}]{data['decision'].upper()}[/{color}] {data['reason']}")


if __name__ == "__main__":
    app()