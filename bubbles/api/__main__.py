from bubbles.api import run_api_server
import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('--host', '-h', default='localhost', help='hostname to connect')
@click.option('--port', '-p', default=5000)
@click.option('-d', '--database', required=True)
def run_server(host, port, database):
    run_api_server(host, port, database)


cli()
