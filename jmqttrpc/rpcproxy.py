import eventlet
eventlet.monkey_patch()
import functools


class MethodProxy():
    def __init__(self, publisher,service_name):
        self.publisher = publisher
        self.service_name = service_name

    def __getattr__(self, name):
        call = functools.partial(self.publisher.call, service=self.service_name, method=name)
        return call

class RPCProxy(object):
    def __init__(self, config, publisher):
        self.config = config
        self.publisher = publisher

    def __getattr__(self, name):
        return MethodProxy(self.publisher, name)

