import click
import bubbles.parsers
import bubbles.publishers
from bubbles.protocol import deserialize_message


@click.group()
def cli():
    pass


@cli.command()
@click.argument('topic', help='topic name to parse')
@click.argument('path', help='path to snaphost data')
def parse(topic, path):
    with open(path) as f:
        data = f.read()
    bubbles.parsers.run_parser(topic, data)


def temp_cb(context, body):
    parsers = bubbles.parsers.load_parsers()
    user, snapshot = deserialize_message(body)
    print(user)


@cli.command()
@click.argument('topic', help='topic name to parse')
@click.argument('mq', help='message queue url')
def run_parser(topic, mq):
    publisher = bubbles.publishers.find_publisher(mq)
    publisher_obj = publisher(mq,
                              sub_exchange='snapshots',
                              sub_routing_key='snapshot.data',
                              sub_queue=topic,
                              callback=temp_cb)

    publisher_obj.subscribe()


cli()
