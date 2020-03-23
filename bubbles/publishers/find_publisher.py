from .rabbitmq import RabbitmqPublisher


def find_publisher(url):
    pub = RabbitmqPublisher(url)
    return pub.publish
