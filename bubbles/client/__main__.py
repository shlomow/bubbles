import click
import bubbles.client


@click.group()
def cli():
    pass


@cli.command()
@click.option('--host', '-h', default='127.0.0.1', help='hostname to connect')
@click.option('--port', '-p', default=8000)
@click.argument('path', type=str)
def upload_sample(host, port, path):
    '''Upload samples to the server

    :param host: hostname that the client connects to. Defaults to `127.0.0.1`.
    :type host: str
    :param port: port number of the server. Defaults to `8000`.
    :type port: int
    :param path: path to where the snapshots are placed.
    :type path: str
    '''
    bubbles.client.upload_sample(host, port, path)


cli()
