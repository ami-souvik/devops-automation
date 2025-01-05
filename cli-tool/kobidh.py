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


# kobidh container:push web -a fastapi-basicapp
@cli.command(name="container:push")
@click.argument('services', nargs=-1)
@click.option('-a', '--app', type=str, help='Name of app', default=None)
def container_push(services, app):
    if not app:
        click.echo(f"Name of the app is required, in order to push")
        return
    services = list(services) if services else ['web']
    click.echo(f"Performing 'push' on container: {services}")
    # Container().push(app, services)


# kobidh container:release web worker -a fastapi-basicapp
@cli.command(name="container:release")
@click.argument('services', nargs=-1)
@click.option('-a', '--app', type=str, help='Name of app', default=None)
def container_release(services, app):
    if not app:
        click.echo(f"Name of the app is required, in order to release")
        return
    services = list(services) if services else ['web']
    click.echo(f"Performing 'release' on container: {services}")
