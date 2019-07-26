import eventlet
eventlet.monkey_patch()

import paho.mqtt.client as mqtt

from jmqttrpc.client import BaseMQTTRPC
from jmqttrpc.constants import DEFAUT_MAX_WOKERS


class BaseRPCService(BaseMQTTRPC):

    def __init__(self,config, worker):
        self.service_name = config.get("service_name") or config["client_id"]
        self.max_workers = config.get("wokers_num") or DEFAUT_MAX_WOKERS
        self.pool = eventlet.GreenPool(size=self.max_workers)
        self.worker = worker
        super(BaseRPCService, self).__init__(client_id=config["client_id"],
                                         clean_session=config.get("clean_session", True),
                                         userdata=config.get("user_data", None),
                                         protocol=config.get("protocol", mqtt.MQTTv311))

    def reply(self, request_topic, msg):
        raise NotImplementedError

    def subscribes_rpc_topics(self):
        self.subscribe(self.REQUEST_TOPIC_TMP.format(versioin=self.VERSION,
                                                   service=self._client_id,
                                                   method="+",
                                                   topic="+",
                                                     pid="+"))






class RPCService(BaseRPCService):

    def reply(self, request_topic, msg):
        reply_topic = request_topic+"/reply"
        return self.publish(reply_topic, msg)

    def handle_request_msg(self, msg):
        topic = msg.topic
        _,_,version,service,method,pid = topic.split("/")
        self.reply(topic, {"code":0,
                           "msg":"ok"})
