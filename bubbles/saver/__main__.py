import click
from bubbles.saver import Saver
import bubbles.publishers


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


def consume_callback(context, ch, method, properties, body, *args, **kwargs):
    database = kwargs['database_url']
    saver = Saver(database)
    topic = method.routing_key.split('.')[0]
    saver.save(topic, body)


@cli.command()
@click.argument('database')
@click.argument('mq')
def run_saver(database, mq):
    publisher = bubbles.publishers.find_publisher(mq)
    publisher_obj = publisher(mq,
                              sub_exchange='parsers',
                              sub_routing_key='*.result',
                              sub_queue='saver',
                              callback=consume_callback,
                              callback_kwargs={'database_url': database})

    publisher_obj.subscribe()


cli()
