from eventlet import Event
# from threading import Event

class EventGetMixin():

    def get_reply_event(self, reply_id):
        reply_event = Event()
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




