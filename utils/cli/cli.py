import click

from utils.helpers import sketch_for_day, sketch_info_for_day

from .readme import update_readme
from .repo import commit_changes
from .site import post_to_site


@click.group()
def cli():
    """Sketches CLI."""
    pass


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
    post_to_site(sketch)


@cli.command()
@click.argument("day")
def all(day: str):
    """Update Readme, Commit changes, Publish on ericof.com."""
    readme(day)
    commit(day)
    publish(day)
