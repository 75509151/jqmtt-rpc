import time
import json
import pytest
from unittest.mock import MagicMock
import unittest
import paho.mqtt.client as mqtt

from jmqttrpc.client import MQTTClient, BaseMQTTRPC, MQTTRPC
from jmqttrpc.service import RPCService
from jmqttrpc.protocol import RPCProtocol
from jmqttrpc.rpcproxy import RPCProxy
from jmqttrpc.constants import *

from .config import MQTT_BORKER_URL, MQTT_BORKER_PORT
from .utils import get_random_id

# class MQTTRPC4Test(BaseMQTTRPC):

    # def on_mqtt_msg(self, client, userdata, msg):
        # pass

    # def on_mqtt_connect(self, client, userdata, flags, rc):
        # pass


@pytest.yield_fixture(autouse=True)
def reset():
    pass


@pytest.yield_fixture
def basemqttrpc(request):
    client_id = get_random_id()
    client = BaseMQTTRPC(client_id)

    need_mocks= getattr(request, "param",[])
    print("need_mocks: %s" % need_mocks)
    if need_mocks:
        for mock_method in need_mocks:
            if hasattr(client, mock_method):
                setattr(client, mock_method, MagicMock())

    client.connect(MQTT_BORKER_URL, MQTT_BORKER_PORT)
    print("connect")
    client.loop_start()
    time.sleep(1)

    yield client

    client.stop()
    print("stop")

@pytest.yield_fixture(scope="class")
def unlive_client():
    client_id = get_random_id()
    client = MQTTClient(client_id)
    yield client



@pytest.yield_fixture()
def mqttrpc(request):
    client_id = get_random_id()
    client = MQTTRPC(client_id)

    need_mocks= getattr(request, "param",[])
    print("need_mocks: %s" % need_mocks)
    if need_mocks:
        for mock_method in need_mocks:
            if hasattr(client, mock_method):
                setattr(client, mock_method, MagicMock())



    client.connect(MQTT_BORKER_URL, MQTT_BORKER_PORT)
    print("rpc connect")
    client.loop_start()
    time.sleep(1)
    yield client
    client.stop()
    print("rpc stop")




class RPCService4Test(RPCService):
    def get_reponse(self, request):
        return SUC, CODE_MSG[SUC], request.func

@pytest.yield_fixture()
def rpcservice(request):
    client_id = get_random_id()
    config = {"service_name": "test",
              "client_id": get_random_id()}
    client = RPCService4Test(config, None)

    need_mocks= getattr(request, "param",[])
    print("need_mocks: %s" % need_mocks)
    if need_mocks:
        for mock_method in need_mocks:
            if hasattr(client, mock_method):
                setattr(client, mock_method, MagicMock())


    client.connect(MQTT_BORKER_URL, MQTT_BORKER_PORT)
    print("rpcservice connect")
    client.loop_start()
    time.sleep(1)
    yield client
    client.stop()
    print("rpcservice stop")


# @pytest.yield_fixture()
# class LocalRPCProxy(RPCProxy):
    # def __init__(self):
        # publisher = MQTTRPC("")
        # super(LocalRPCProxy, self).__init__(None,)


