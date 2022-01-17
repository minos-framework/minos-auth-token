
import sys
import typer


app = typer.Typer()

@app.command("start")
def start():
    """Perform Start operation."""

    raise NotImplementedError


@app.command("status")
def status():
    """Perform Status operation."""
    raise NotImplementedError


@app.command("stop")
def stop():
    """Perform Stop operation."""
    raise NotImplementedError

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
