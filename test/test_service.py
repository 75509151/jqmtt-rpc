import time
import json
import uuid
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

    def test_handle_request_msg(self, rpcservice, mqttrpc):
        topic = mqttrpc.REQUEST_TOPIC_TMP.format(version=rpcservice.VERSION,
                                               service=rpcservice.service_name,
                                               method="test",
                                               pid=get_random_id()
                                               )
        mqttrpc.publish(topic, json.dumps({"ll":1}))

