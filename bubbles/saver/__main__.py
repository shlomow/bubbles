import click
from bubbles.saver import Saver
# import bubbles.publishers


@click.group()
def cli():
    pass


@cli.command()
@click.option('-d', '--database', required=True, help='database url')
@click.argument('topic')
@click.argument('path')
def save(database, topic, path):
    with open(path) as f:
        data = f.read()

    saver = Saver(database)
    saver.save(topic, data)


@cli.command()
@click.argument('database')
@click.argument('mq')
def run_saver(database, mq):
    # publish = bubbles.publishers.find_publisher(mq)
    # saver = Saver(database)
    pass


cli()
