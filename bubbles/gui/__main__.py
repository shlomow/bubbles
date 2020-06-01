import bubbles.gui
import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('--host', '-h', default='localhost', help='hostname to connect')
@click.option('--port', '-p', default=8080)
@click.option('--api-host', default='localhost', help='hostname to connect')
@click.option('--api-port', default=5000)
def run_server(host, port, api_host, api_port):
    bubbles.gui.run_server(host, port, api_host, api_port)


cli()
