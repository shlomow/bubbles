import bubbles.publishers
import click
import bubbles.server


@click.group()
def cli():
    pass


@cli.command()
@click.option('--host', '-h', default='localhost', help='hostname to connect')
@click.option('--port', '-p', default=8000)
@click.argument('url', type=str)
def run_server(host, port, url):
    publisher = bubbles.publishers.find_publisher(url)
    publisher_obj = publisher(url,
                              pub_exchange='snapshots',
                              pub_routing_key='snapshot.data')
    bubbles.server.run_server(host, port, publisher_obj.publish)


cli()
