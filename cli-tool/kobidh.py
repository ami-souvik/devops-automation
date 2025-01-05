import functools
import click
from time import sleep
from services.environment import Environment


def _require_region(func):
    @click.option('--region', '-r', prompt='region', help='region')
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def _require_environment(func):
    @click.option('--environment', '-e', prompt='environment', help='environment')
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@click.group()
def cli():
    pass


@cli.command()
def test():
    for i in range(1, 11):
        # Replace the same line with new content
        click.echo(f"\rProcessing... {i * 10}%", nl=False)
        sleep(0.5)  # Simulate some work
    # Move to a new line after completing the loop
    click.echo("\rTask complete!          ")


# kobidh environment.create development -r ap-south-1
@cli.command(name="environment.create", help="Create a new environment")
# @_require_region
@click.argument('name', type=str)
def environment_create(name, region=None):
    click.echo(f"Creating {name} environment...")
    Environment(name, region).create()


# kobidh environment.delete development -r ap-south-1
@cli.command(name="environment.delete", help="Delete an environment")
# @_require_region
@click.argument('name', type=str)
def environment_delete(name, region=None):
    click.echo(f"Deleting {name} environment...")
    Environment(name, region).delete()


# kobidh environment.describe development -r ap-south-1
@cli.command(name="environment.describe", help="Describe an environment")
# @_require_region
@click.argument('name', type=str)
def environment_describe(name, region=None):
    click.echo(f"Describing {name} environment...")
    Environment(name, region).describe()


# kobidh apps.create fastapi-basicapp -e development
@cli.command(name="apps.create")
@_require_environment
@click.argument('name', type=str)
def apps_create(environment, name):
    click.echo(f"Creating {name} app in {environment}...")


# kobidh apps.configure fastapi-basicapp
@cli.command(name="apps.configure")
# @_require_environment
@click.argument('name', type=str)
def apps_configure(name):
    click.echo(f"Creating {name} app...")
    Environment(name).configure()
