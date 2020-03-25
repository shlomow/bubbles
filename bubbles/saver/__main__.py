import click
from bubbles.saver import Saver
import json
import bubbles.publishers


@click.group()
def cli():
    pass


@cli.command()
@click.option('-d', '--database', required=True, help='database url')
@click.argument('topic', help='topic name represents the content in path')
@click.argument('path', help='path to topic result')
def save(database, topic, path):
    with open(path) as f:
        data = json.loads(f.read())

    saver = Saver(database)
    saver.save(topic, data)


@cli.command()
@click.argument('database', help='database url')
@click.argument('mq', help='message queue url')
def run_saver(database, mq):
    publish = bubbles.publishers.find_publisher(mq)
    saver = Saver(database)


cli()
