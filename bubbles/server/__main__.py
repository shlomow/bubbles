import bubbles.publishers
import click
import bubbles.server


@click.group()
def cli():
    pass


@cli.command()
@click.option('--host', default='localhost', help='hostname to connect')
@click.option('--port', '-p', default=8000)
@click.argument('url', type=str)
def run_server(host, port, url):
    publish = bubbles.publishers.find_publisher(url)
    bubbles.server.run_server(host, port, publish)


cli()
