from .rabbitmq import RabbitmqPublisher


def find_publisher(url):
    '''Find message queue publisher from the scheme of the url

    :param url: url string represents the protocol that the publisher
        should return.
    :return: object with method like publish and subscribe
    '''
    # pub = RabbitmqPublisher(url)
    # return pub.publish
    return RabbitmqPublisher
