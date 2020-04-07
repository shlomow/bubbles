import pika
from furl import furl


class RabbitmqPublisher:
    '''Rabbitmq message queue handler.
    '''
    scheme = 'rabbitmq'

    def __init__(self, url, *args, **kwargs):
        '''Constructor

        :param url: url of rabbitmq server. port is `5672` if not given.
        :param kwargs: additional parameters needed to config the session.
            `pub_exchange`, `pub_routing_key` for publishing,
            `sub_exchange`, `sub_routing_key`, `sub_queue` for subscribing.
            `callback` is a function that this handle will call each message
            given. `callback_args`, `callback_kwargs` will be passed to
            `callback` and are optional.
        '''
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
            self.user_callback_args = []
            if 'callback_args' in kwargs:
                self.user_callback_args = kwargs['callback_args']
            self.user_callback_kwargs = dict()
            if 'callback_kwargs' in kwargs:
                self.user_callback_kwargs = kwargs['callback_kwargs']
            self.is_subscriber = True

    def create_connection(self):
        '''Creates connection with server.

        :return: connection and channel created from `__init__` parameters.
        '''
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
            channel.queue_declare(self.sub_queue, durable=True)

            channel.queue_bind(exchange=self.sub_exchange,
                               queue=self.sub_queue,
                               routing_key=self.sub_routing_key)

            channel.basic_qos(prefetch_count=1)

        return connection, channel

    def publish(self, msg):
        '''Publish `msg` to rabbitmq server.

        :param msg: message to publish.
        '''
        if not self.is_subscriber:
            self.connection, self.channel = self.create_connection()

        self.channel.basic_publish(
            exchange=self.pub_exchange,
            routing_key=self.pub_routing_key,
            body=msg,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))

        if not self.is_subscriber:
            self.connection.close()

    def on_message_callback(self, ch, method, properties, body):
        '''Callback that is called after a message given by subscribing.
            This function will call the callback given by `__init__`
            and send ack to the server.
        '''
        self.user_callback(self, ch, method, properties, body,
                           *self.user_callback_args,
                           **self.user_callback_kwargs)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def subscribe(self):
        '''Subscribe according to the parameters given to `__init__`.
        Runs forever.
        '''
        if self.is_subscriber:
            self.connection, self.channel = self.create_connection()

        self.channel.basic_consume(
            queue=self.sub_queue,
            on_message_callback=self.on_message_callback)
        self.channel.start_consuming()

    def close(self):
        '''Close connection with the server.
        '''
        self.connection.close()
