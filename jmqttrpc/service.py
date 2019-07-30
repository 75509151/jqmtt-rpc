import eventlet
eventlet.monkey_patch()

import json
from logging import getLogger
import paho.mqtt.client as mqtt

from jmqttrpc.client import BaseMQTTRPC
from jmqttrpc.constants import DEFAUT_MAX_WOKERS


_log = getLogger(__name__)

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

    def subscribe_rpc_topics(self):
        topic = self.REQUEST_TOPIC_TMP.format(version=self.VERSION,
                                                service=self.service_name,
                                                device_id="+",
                                                method="+",
                                                    pid="+")
        self.subscribe(topic)

        _log.debug("subs: %s"% topic)





class RPCService(BaseRPCService):

    def reply(self, request_topic, msg):

        reply_topic = request_topic+"/reply"
        # print("reply: %s" % reply_topic)
        return self.publish(reply_topic, msg)

    def handle_request_msg(self, msg):
        try:
            request = self.protocol.parse_requset(msg)
            self.reply(request.topic, json.dumps({"code":0,
                            "msg":"ok"}))
        except Exception as e:
            _log.error("handle_request err: %s" % str(e))
