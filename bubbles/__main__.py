import click
import bubbles

@click.group()
def cli():
    pass

@cli.command()
@click.option('--host', default='0.0.0.0', help='hostname to bind')
@click.option('--port', '-p', default=5000)
@click.argument('data', type=str)
def run(host, port, data):
    bubbles.run_server((host, port), data)


@cli.command()
@click.option('--host', default='localhost', help='hostname to connect')
@click.option('--port', '-p', default=5000)
@click.argument('user_id', type=int)
@click.argument('thought', type=str)
def upload(host, port, user_id, thought):
    bubbles.upload_thought((host, port), user_id, thought)

cli()
