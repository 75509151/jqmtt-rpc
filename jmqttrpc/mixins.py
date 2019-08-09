import eventlet
import threading

from jmqttrpc.erros import JTimeoutError


class EventGetMixin():

    def get_reply_event(self, reply_id):
        reply_event = eventlet.Event()
        self._reply_events[reply_id] = reply_event
        return reply_event


class AsyncEvent():
    __slots__ = ["_event", "_result", "_ex"]

    def __init__(self):
        self._event = threading.Event()
        self._result = None
        self._ex = None

    def send(self, result):
        self._result = result
        self._event.set()

    def send_exception(self, ex):
        self._ex = ex
        self._event.set()

    def wait(self, timeout=None):
        if self._event.wait(timeout):
            if self._ex:
                raise self._ex
            else:
                return self._result
        raise JTimeoutError()

class EventMixin():

    def get_reply_event(self, reply_id):
        reply_event = AsyncEvent()
        self._reply_events[reply_id] = reply_event
        return reply_event



class SubscribeMixin():

    def reset_subscribes(self):
        self.subscribes = set()

    def add_subscribes(self, topic):
        if isinstance(topic, tuple):
            topic, qos = topic
        if isinstance(topic, str):
            self.subscribes.add(topic)

        elif isinstance(topic, list):
            for t, q in topic:
                self.subscribes.add(t)

    def del_subscribes(self, topic):
        if isinstance(topic, tuple):
            topic, qos = topic
        if isinstance(topic, str):
            self.subscribes.remove(topic)

        elif isinstance(topic, list):
            for t, q in topic:
                self.subscribes.remove(t)
