import pika
from furl import furl


class RabbitmqPublisher:
    scheme = 'rabbitmq'

    def __init__(self, url, *args, **kwargs):
        self.url = furl(url)
        if self.url.port is None:
            self.url.port = 5672  # default port of rabbitmq

        self.is_publisher = False
        if 'pub_exchange' in kwargs:
            self.pub_exchange = kwargs['pub_exchange']
            self.pub_routing_key = kwargs['pub_routing_key']
            self.is_publisher = True

        self.is_subscriber = False
        if 'sub_exchange' in kwargs:
            self.sub_exchange = kwargs['sub_exchange']
            self.sub_routing_key = kwargs['sub_routing_key']
            self.sub_queue = kwargs['sub_queue']
            self.user_callback = kwargs['callback']
            self.is_subscriber = True

        self.connection, self.channel = self.create_connection()

    def create_connection(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.url.host, port=self.url.port)
            )

        channel = connection.channel()

        if self.is_publisher:
            channel.exchange_declare(exchange=self.pub_exchange,
                                     exchange_type='topic')

        if self.is_subscriber:
            channel.exchange_declare(exchange=self.sub_exchange,
                                     exchange_type='topic')
            channel.queue_declare(self.queue, durable=True)

            channel.queue_bind(exchange=self.sub_exchange,
                               queue=self.sub_queue,
                               routing_key=self.sub_routing_key)

            channel.basic_qos(prefetch_count=1)

        return connection, channel

    def publish(self, msg):
        self.channel.basic_publish(
            exchange=self.pub_exchange,
            routing_key=self.pub_routing_key,
            body=msg,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))

    def on_message_callback(self, ch, method, properties, body):
        self.user_callback(self, body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def subscribe(self):
        self.channel.basic_consume(
            queue=self.sub_queue,
            on_message_callback=self.on_message_callback)

    def close(self):
        self.connection.close()
