import click
import requests


@click.group()
def cli():
    pass


@cli.command()
@click.option('--host', '-h', default='localhost', help='hostname to connect')
@click.option('--port', '-p', default=5000)
def get_users(host, port):
    url = f'http://{host}:{port}/users'
    res = requests.get(url)
    click.echo(res.text)


@cli.command()
@click.option('--host', '-h', default='localhost', help='hostname to connect')
@click.option('--port', '-p', default=5000)
@click.argument('user_id', type=int)
def get_user(host, port, user_id):
    url = f'http://{host}:{port}/users/{user_id}'
    res = requests.get(url)
    click.echo(res.text)


@cli.command()
@click.option('--host', '-h', default='localhost', help='hostname to connect')
@click.option('--port', '-p', default=5000)
@click.argument('user_id', type=int)
def get_snapshots(host, port, user_id):
    url = f'http://{host}:{port}/users/{user_id}/snapshots'
    res = requests.get(url)
    click.echo(res.text)


@cli.command()
@click.option('--host', '-h', default='localhost', help='hostname to connect')
@click.option('--port', '-p', default=5000)
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=int)
def get_snapshot(host, port, user_id, snapshot_id):
    url = f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}'
    res = requests.get(url)
    click.echo(res.text)


cli()
