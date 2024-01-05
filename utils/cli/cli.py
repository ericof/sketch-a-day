import click

from utils.helpers import sketch_for_day, sketch_info_for_day

from .create import create_new_sketch
from .readme import update_readme
from .repo import commit_changes
from .site import post_to_site


@click.group()
def cli():
    """Sketches CLI."""
    pass


@cli.command()
@click.argument("day")
def create(day: str):
    """Create a new sketch structure."""
    click.echo(f"Creating sketch for day {day}")
    create_new_sketch(day)


@cli.command()
@click.argument("day")
def readme(day: str):
    """Update the README.md file with the entry for a given day."""
    info = sketch_info_for_day(day)
    click.echo(f"Updating the README.md file for day {day}")
    update_readme(info)


@cli.command()
@click.argument("day")
def commit(day: str):
    """Commit changes for a given day."""
    info = sketch_info_for_day(day)
    click.echo(f"Commit changes for day {day}")
    commit_changes(info)


@cli.command()
@click.argument("day")
def publish(day: str):
    """Publish sketch to ericof.com."""
    sketch = sketch_for_day(day)
    click.echo(f"Publish sketch for day {day} to ericof.com")
    url = post_to_site(sketch)
    click.echo(f"Sketch for day {day} published on {url}")


@cli.command()
@click.argument("day")
def all(day: str):
    """Update Readme, Commit changes, Publish on ericof.com."""
    info = sketch_info_for_day(day)
    click.echo(f"Updating the README.md file for day {day}")
    update_readme(info)
    click.echo(f"Commit changes for day {day}")
    commit_changes(info)
    sketch = sketch_for_day(day)
    click.echo(f"Publish sketch for day {day} to ericof.com")
    url = post_to_site(sketch)
    click.echo(f"Sketch for day {day} published on {url}")
