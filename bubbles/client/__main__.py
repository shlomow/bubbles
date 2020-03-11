import click
import bubbles.client


@click.group()
def cli():
    pass

@cli.command()
@click.option('--host', default='localhost', help='hostname to connect')
@click.option('--port', '-p', default=8000)
@click.argument('path', type=str)
def upload_sample(host, port, path):
    bubbles.client.upload_sample(host, port, path)

cli()