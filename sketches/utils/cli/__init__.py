from .create import create_new_sketch
from .readme import update_readme
from .repo import commit_changes
from .site import post_to_site
from sketches.utils.helpers.dates import process_day
from sketches.utils.helpers.paths import sketch_path_for_day
from sketches.utils.helpers.sketches import sketch_for_day
from sketches.utils.helpers.sketches import sketch_info_for_day
from sketches.utils.mapas import _expandir_bbox
from sketches.utils.mapas import geocode_to_gdf
from typing import Annotated

import typer


DAY_HELP = "Day of the sketch in YYYY-MM-DD format, e.g., 2025-01-01"


app = typer.Typer(no_args_is_help=True)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Sketches Cli."""
    pass


@app.command(name="create")
def create(day: Annotated[str, typer.Argument(help=DAY_HELP)]):
    """Create a new sketch structure."""
    day = process_day(day)
    typer.echo(f"Creating sketch for day {day}")
    create_new_sketch(day)


@app.command(name="path")
def path(day: Annotated[str, typer.Argument(help=DAY_HELP)]):
    """Print the path to the sketch for a given day."""
    day = process_day(day)
    dst = sketch_path_for_day(day)
    path = f"{dst}/__main__.py"
    typer.echo(path)


@app.command(name="readme")
def readme(day: Annotated[str, typer.Argument(help=DAY_HELP)]):
    """Update the README.md file with the entry for a given day."""
    day = process_day(day)
    info = sketch_info_for_day(day)
    typer.echo(f"Updating the README.md file for day {day}")
    update_readme(info)


@app.command(name="commit")
def commit(day: Annotated[str, typer.Argument(help=DAY_HELP)]):
    """Commit changes for a given day."""
    day = process_day(day)
    info = sketch_info_for_day(day)
    typer.echo(f"Commit changes for day {day}")
    commit_info = commit_changes(info)
    typer.echo(f"Changes committed with SHA: {commit_info.hexsha}")


@app.command(name="publish")
def publish(day: Annotated[str, typer.Argument(help=DAY_HELP)]):
    """Publish sketch to ericof.com."""
    day = process_day(day)
    sketch = sketch_for_day(day)
    typer.echo(f"Publish sketch for day {day} to ericof.com")
    url = post_to_site(sketch)
    typer.echo(f"Sketch for day {day} published on {url}")


@app.command(name="all")
def run_all(day: Annotated[str, typer.Argument(help=DAY_HELP)]):
    """Update Readme, Commit changes, Publish on ericof.com."""
    day = process_day(day)
    info = sketch_info_for_day(day)
    if not info.exists:
        typer.echo(f"Stopping, as the image {info.filepath} was not created.")
        return
    typer.echo(f"Updating the README.md file for day {day}")
    update_readme(info)
    typer.echo(f"Commit changes for day {day}")
    commit_info = commit_changes(info)
    typer.echo(f"Changes committed with SHA: {commit_info.hexsha}")
    sketch = sketch_for_day(day, commit=commit_info)
    typer.echo(f"Publish sketch for day {day} to ericof.com")
    url = post_to_site(sketch, commit_hash=commit_info.hexsha)
    typer.echo(f"Sketch for day {day} published on {url}")


@app.command(name="geocode")
def geocode(
    query: Annotated[
        str,
        typer.Argument(
            help="The query to geocode, e.g., 'Asa Norte, Brasília, DF, Brasil'"
        ),
    ],
    expand: Annotated[
        float, typer.Option(help="How much should we expand the bounds")
    ] = 0.0,
):
    """Test a geocode query."""
    try:
        gdf = geocode_to_gdf(query)
    except ValueError as e:
        typer.echo(f"Could not find location: {query}")
        raise typer.Exit(code=1) from e
    bbox = gdf.total_bounds
    if expand > 0.0:
        bbox = _expandir_bbox(bbox, percentual=expand)
    typer.echo(f"Geocoded {query} to bounds:")
    typer.echo(f" - ({bbox[0]:.6f}, {bbox[3]:.6f})")
    typer.echo(f" - ({bbox[2]:.6f}, {bbox[1]:.6f})")
