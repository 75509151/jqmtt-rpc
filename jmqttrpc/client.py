
import uuid
import threading
import traceback

from logging import getLogger

import paho.mqtt.client as mqtt

from jmqttrpc.protocol import RPCProtocol
from jmqttrpc.mixins import EventGetMixin, SubscribeMixin
from jmqttrpc.erros import StateError

_log = getLogger(__name__)


class MQTTClient(mqtt.Client, SubscribeMixin):

    def __init__(self, client_id, clean_session=True, userdata=None, protocol=mqtt.MQTTv311):
        self.device_id = client_id
        super(MQTTClient, self).__init__(client_id, clean_session, userdata, protocol)
        self._stop = threading.Event()
        self.setup()

    def start(self):
        self._stop.clear()
        self.loop_start()

    def stop(self):
        self._stop.set()
        self.disconnect()
        self.loop_stop()

    def setup(self):
        self.on_message = self.on_mqtt_msg
        self.on_connect = self.on_mqtt_connect
        self.on_disconnect = self.on_mqtt_disconnect

    def teardwon(self):
        pass

    def on_mqtt_disconnect(self):
        pass


    def on_mqtt_msg(self, client, userdata, msg):
        pass

    def on_mqtt_connect(self, client, userdata, flags, rc):
        pass

    def publish(self, topic, payload=None, qos=1, retain=False):
        if self._state != mqtt.mqtt_cs_connected:
            raise StateError("{state} not in CONNECTED state".format(state=self._state))
        return super(MQTTClient, self).publish(topic, payload, qos, retain)

    def subscribe(self, topic, qos=1):
        if self._state != mqtt.mqtt_cs_connected:
            raise StateError("{state} not in CONNECTED state".format(state=self._state))
        ret, mid = super(MQTTClient, self).subscribe(topic, qos)
        if ret == 0:
            # TODO: do in ack?
            self.add_subscribes(topic)
        return ret, mid

    def unsubscribe(self, topic):
        if self._state != mqtt.mqtt_cs_connected:
            raise StateError("{state} not in CONNECTED state".format(state=self._state))
        ret, mid = super(MQTTClient, self).unsubscribe(topic)
        if ret == 0:
            # TODO: do in ack?
            self.del_subscribes(topic)
        return ret, mid


class BaseMQTTRPC(MQTTClient, SubscribeMixin):
    VERSION = 1.0
    REQUEST_TOPIC_TMP = "/rpc/request/{version}/{service}/{device_id}/{method}/{pid}"
    REQUEST_TOPIC_MODEL = "/rpc/request/+/+/+/+/+"
    REPLY_TOPIC_TMP = "/rpc/request/{version}/{service}/{device_id}/{method}/{pid}/reply"
    REPLY_TOPIC_MODEL = REQUEST_TOPIC_MODEL + "/reply"

    def __init__(self, client_id, clean_session=True, userdata=None, protocol=mqtt.MQTTv311):
        super(BaseMQTTRPC, self).__init__(client_id, clean_session, userdata, protocol)
        self._reply_events = {}
        self.subscribes = set()

    def teardwon(self):
        for t in self.subscribes:
            self.unsubscribe(t)

    def on_mqtt_disconnect(self):
        if self._clean_session and self._stop.is_set():
            self.reset_subscribes()

    def on_mqtt_connect(self, client, userdata, flags, rc):
        self.subscribe_rpc_topics()

    def subscribe_rpc_topics(self):
        raise NotImplementedError

    def _get_pid(self):
        return str(uuid.uuid4())

    def call(self, *args, **kw):
        raise NotImplementedError

    def get_message(self):
        raise NotImplementedError

    def on_mqtt_msg(self, client, userdata, msg):
        topic = msg.topic
        _log.info("msg topic: %s, payload:%s" % (topic, msg.payload))
        try:

            if mqtt.topic_matches_sub(self.REPLY_TOPIC_MODEL, topic):
                self.handle_reply_msg(msg)
            elif mqtt.topic_matches_sub(self.REQUEST_TOPIC_MODEL,topic):
                self.handle_request_msg(msg)
            else:
                _log.warning("handle_unkwon_msg")
                print("unkown msg")
                self.handle_unkwon_msg(msg)
        except Exception as e:
            _log.error("on_mqtt_msg error: %s" % str(traceback.format_exc()))
            print("on_mqtt_msg error: %s" % str(traceback.format_exc()))
            raise e

    def handle_unkwon_msg(self, msg):
        pass

    def handle_reply_msg(self, msg):
        pass

    def handle_request_msg(self, msg):
        pass


class MQTTRPC(BaseMQTTRPC, EventGetMixin):
    """
    client
    """

    protocol = RPCProtocol

    def __init__(self, client_id, clean_session=True, userdata=None, protocol=mqtt.MQTTv311):
        super(MQTTRPC, self).__init__(client_id, clean_session, userdata, protocol)

    def subscribe_rpc_topics(self):

        topic = self.REPLY_TOPIC_TMP.format(version=self.VERSION,
                                                   service="+",
                                                device_id=self.device_id,
                                                   method="+",
                                                   topic="+",
                                                   pid="+")
        self.subscribe(topic)
        _log.info("subs reply:%s" % topic)
        print("subs reply:%s" % topic)


    def handle_reply_msg(self, msg):
        try:
            reply  = self.protocol.parse_reply(msg)
            print("pid:%s" % reply.pid)

            try:
                reply_event = self._reply_events.pop(reply.pid)
            except KeyError:
                _log.warning("expired msg? topic: %s, payload: %s" % (msg.topic,
                                                                      msg.payload))
            else:
                reply_event.send(reply)
        except Exception as e:
            _log.error(str(e))
            raise e



    def call(self, service, method, dict_params, timeout=60):
        assert type(dict_params) == dict
        pid = self._get_pid()
        topic = self.REQUEST_TOPIC_TMP.format(version=self.VERSION,
                                              service=service,
                                              device_id=self.device_id,
                                              method=method,
                                              pid=pid)
        reply_event = self.get_reply_event(pid)
        payload = self.protocol.create_request(method, dict_params)
        ret, mid = self.publish(topic, payload)
        # TODO: to deal with error and empty
        reply = reply_event.wait(timeout)
        if not reply:
           self._reply_events.pop(pid)
        return reply
