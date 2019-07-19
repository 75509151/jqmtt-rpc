from eventlet import Event

class EventGetMixin():

    def get_reply_event(self, reply_id):
        reply_event = Event()
        self._reply_events[reply_id] = reply_event
        return reply_event

