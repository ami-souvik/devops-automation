import click
from app.services import Container

@click.group()
def cli():
    pass

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
    Container().push(app, services)

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
