import click
import bubbles.parsers
import bubbles.publishers


@click.group()
def cli():
    pass


@cli.command()
@click.argument('topic')
@click.argument('path')
def parse(topic, path):
    with open(path, 'rb') as f:
        data = f.read()
    click.echo(bubbles.parsers.run_parser(topic, data))


def consume_callback(context, ch, method, properties, body):
    data = bubbles.parsers.run_parser(context.sub_queue, body)
    context.publish(data)


@cli.command()
@click.argument('topic')
@click.argument('mq')
def run_parser(topic, mq):
    publisher = bubbles.publishers.find_publisher(mq)
    publisher_obj = publisher(mq,
                              sub_exchange='snapshots',
                              sub_routing_key='snapshot.data',
                              sub_queue=topic,
                              pub_exchange='parsers',
                              pub_routing_key=f'{topic}.result',
                              callback=consume_callback)

    publisher_obj.subscribe()


cli()
