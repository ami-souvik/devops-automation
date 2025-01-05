import click

def log(text, **kwargs):
    click.secho(text, fg='green', **kwargs)

def log_error(text, **kwargs):
    click.secho(text, fg='red', bold=True, **kwargs)

def log_warning(text, level=0, **kwargs):
    click.secho(text, fg='yellow', **kwargs)

def log_bold(text, **kwargs):
    click.secho(text, fg='green',  bold=True, **kwargs)

def log_intent(text, level=1, **kwargs):
    click.secho((" " * 4 * level) + text, fg='green', **kwargs)

def log_intent_error(text, level=1, **kwargs):
    click.secho((" " * 4 * level) + text, fg='red', **kwargs)

def log_with_color(text, color, level=2, **kwargs):
    click.secho((" " * 4 * level) + text, fg=color, **kwargs)

def log_list(logs: list[tuple], **kwargs):
    for l in logs:
        click.secho((" " * 4 * l[2]) + l[0], fg=l[1], **kwargs)
