import bubbles.gui
import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('--host', '-h', default='localhost')
@click.option('--port', '-p', default=8080)
@click.option('--api-host', '-H', default='localhost')
@click.option('--api-port', '-P', default=5000)
def run_server(host, port, api_host, api_port):
    bubbles.gui.run_server(host, port, api_host, api_port)


cli()
