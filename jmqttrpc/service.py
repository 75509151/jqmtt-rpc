import eventlet
eventlet.monkey_patch()
from logging import getLogger
import json

import paho.mqtt.client as mqtt

import jmqttrpc.constants as cos
from jmqttrpc.client import BaseMQTTRPC
from jmqttrpc.protocol import RPCProtocol, RPCParseError


_log = getLogger(__name__)


class BaseRPCService(BaseMQTTRPC):

    def __init__(self, config, worker):
        self.service_name = config.get("service_name") or config["client_id"]
        self.worker = worker
        super(BaseRPCService, self).__init__(client_id=config["client_id"],
                                             clean_session=config.get("clean_session", True),
                                             userdata=config.get("user_data", None),
                                             protocol=config.get("protocol", mqtt.MQTTv311),
                                             max_workers=config.get("max_workers", cos.DEFAUT_MAX_WOKERS))

    def reply(self, request_topic, msg):
        raise NotImplementedError

    def subscribe_rpc_topics(self):
        topic = self.REQUEST_TOPIC_TMP.format(version=self.VERSION,
                                              service=self.service_name,
                                              device_id="+",
                                              method="+",
                                              pid="+")
        self.subscribe(topic)

        _log.debug("subs: %s" % topic)


class RPCService(BaseRPCService):

    def reply(self, request_topic, msg):

        reply_topic = request_topic + "/reply"
        print("reply: %s" % reply_topic)
        return self.publish(reply_topic, msg)

    def handle_request_msg(self, msg):
        request = None
        try:
            request = RPCProtocol.parse_requset(msg)
            code, msg, data =self.get_reponse(request)
            ret = self.reply(request.topic,
                        RPCProtocol.create_reply(code, msg, data))
            print("reply: %s" % ret)
        except RPCParseError as e:
            print(str(e))
            _log.error("parse err: %s" % str(e))
            self.reply(cos.PARSE_ERR, cos.CODE_MSG[cos.PARSE_ERR])

        except Exception as e:
            print(str(e))
            _log.error("handle_request err: %s" % str(e))

    def get_reponse(self, request):
        """get_reponse

        :param request: RPCRequest

        return code, msg, data
        """
        raise NotImplementedError

