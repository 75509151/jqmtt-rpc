import paho.mqtt.client as mqtt
import uuid
from protocol import RPCProtocol
from mixins import EventGetMixin


class StateError(Exception):
    def __init__(self, err):
        Exception.__init__(self, err)


class MQTTClient(mqtt.Client):


    def __init__(self, client_id, clean_session=True, userdata=None, protocol=mqtt.MQTTv311):
        super(MQTTClient, self).__init__(client_id, clean_session, userdata, protocol)
        self.subscribes = set()

    def topic_in_subscribes(self, topic):
        return any(mqtt.topic_matches_sub(s, topic) for s in self.subscribes)


    def publish(self, topic, payload=None, qos=1, retain=False):
        if self._state != mqtt.mqtt_cs_connected:
            raise StateError("{state} not in CONNECTED state".format(self._state))
        return super(MQTTClient, self).publish(topic, payload, qos, retain)

    def subscribe(self, topic, qos=1):
        if self._state != mqtt.mqtt_cs_connected:
            raise StateError("{state} not in CONNECTED state".format(self._state))
        ret,mid = super(MQTTClient, self).subscribe(topic,qos)
        if ret == 0:
            #TODO: do in ack?
            self.subscribes.add(topic)
        return ret, mid

    def unsubscribe(self, topic):
        if self._state != mqtt.mqtt_cs_connected:
            raise StateError("{state} not in CONNECTED state".format(self._state))
        ret,mid = super(MQTTClient, self).unsubscribe(topic)
        if ret == 0:
            #TODO: do in ack?
            self.subscribes.remove(topic)
        return ret, mid



class BaseMQTTRPC(MQTTClient):


    def __init__(self, client_id, clean_session=True, userdata=None, protocol=mqtt.MQTTv311):
        super(BaseMQTTRPC, self).__init__(client_id, clean_session, userdata, protocol)
        self._reply_events = {}

        self.on_message = self.on_mqtt_msg

    def _get_pid(self):
        return uuid.uuid4()

    def on_mqtt_msg(self, client, userdata, msg):
        pass

    def call(self, *args, **kw):
        raise NotImplementedError

    def call_async(self, *args, **kw):
        raise NotImplementedError

    def get_message(self):
        raise NotImplementedError


class MQTTRPC(BaseMQTTRPC, EventGetMixin):
    version = 1.0
    request_topic = "/rpc/request/{version}/{service}/{method}/{pid}"
    request_topic_model = "/rpc/+/+/+/+"
    reply_topic_mode = request_topic_model+"/reply"

    protocol = RPCProtocol



    def __init__(self, client_id, clean_session=True, userdata=None, protocol=mqtt.MQTTv311):
        super(MQTTRPC, self).__init__(client_id, clean_session, userdata, protocol)

    def on_mqtt_msg(self, client, userdata, msg):
        topic = msg.topic

        if mqtt.topic_matches_sub(self.reply_topic_mode, topic):
            self.handle_reply_msg(msg)
        elif mqtt.topic_matches_sub(self.request_topic,topic):
            self.handle_request_msg(msg)
        else:
            self.handle_unkwon_msg(msg)


    def handle_unkwon_msg(self, msg):
        pass


    def handle_reply_msg(self, msg):
        pass

    def handle_request_msg(self, msg):
        pass



    def call(self,service, method, params, timeout=60):
        pid = self._get_pid()
        topic = self.request_topic.format(version=self.version,
                                          service=service,
                                          method=method,
                                          pid=pid)
        reply_event = self.get_reply_event(pid)
        payload = self.protocol.create_request(method, params)
        ret, mid = self.publish(topic, payload)
        #TODO: to deal with error and empty
        reply_body = self.reply_event.wait(timeout)
        return reply_body



