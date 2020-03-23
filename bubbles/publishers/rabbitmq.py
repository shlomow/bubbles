import pika
from furl import furl


class RabbitmqPublisher:
    scheme = 'rabbitmq'

    def __init__(self, url):
        self.url = furl(url)
        if self.url.port is None:
            self.url.port = 5672  # default port of rabbitmq

    def publish(self, msg):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.url.host, port=self.url.port)
            )

        channel = connection.channel()
        channel.queue_declare(queue='snapshots', durable=True)

        channel.basic_publish(
            exchange='',
            routing_key='snapshots',
            body=msg,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        connection.close()
