import click
from app.services import Container

@click.group()
def cli():
    pass

# kobidh container:push web worker
@cli.command(name="container:push")
@click.argument('services', nargs=-1)
def container_push(services):
    Container().push()
    services = list(services) if services else ['web']
    click.echo(f"Performing 'push' on container: {services}")

@cli.command(name="container:release")
@click.argument('services', nargs=-1)
def container_release(services):
    services = list(services) if services else ['web']
    click.echo(f"Performing 'release' on container: {services}")
