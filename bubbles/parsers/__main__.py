import json
import click
import bubbles.parsers
import bubbles.publishers
from bubbles.protocol import deserialize_message


@click.group()
def cli():
    pass


@cli.command()
@click.argument('topic')
@click.argument('path')
def parse(topic, path):
    with open(path, 'rb') as f:
        data = f.read()
    print(bubbles.parsers.run_parser(topic, data))


def consume_callback(context, body):
    parsers = bubbles.parsers.load_parsers()
    user, snapshot = deserialize_message(body)
    t = parsers['pose'](None, user, snapshot)
    print(json.dumps(t))


@cli.command()
@click.argument('topic')
@click.argument('mq')
def run_parser(topic, mq):
    publisher = bubbles.publishers.find_publisher(mq)
    publisher_obj = publisher(mq,
                              sub_exchange='snapshots',
                              sub_routing_key='snapshot.data',
                              sub_queue=topic,
                              callback=consume_callback)

    publisher_obj.subscribe()


cli()
