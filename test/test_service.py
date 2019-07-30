import time
import json
import pytest
from unittest.mock import MagicMock
import unittest
import inspect
import paho.mqtt.client as mqtt

from jmqttrpc.service import BaseRPCService, RPCService
from .utils import get_random_id



class TestRPCService:

    def test_reply(self):
        pass


    @pytest.mark.parametrize("rpcservice", [["handle_request_msg", ]], indirect=True)
    def test_handle_request_msg(self, rpcservice, mqttrpc):
        topic = mqttrpc.REQUEST_TOPIC_TMP.format(version=mqttrpc.VERSION,
                                               service=rpcservice.service_name,
                                                device_id=get_random_id(),
                                               method="test",
                                               pid=get_random_id()
                                               )
        mqttrpc.publish(topic, json.dumps({"ll":1}))
        time.sleep(1)
        assert rpcservice.handle_request_msg.call_count == 1

