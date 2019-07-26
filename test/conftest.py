import time
import pytest
from unittest.mock import MagicMock
import unittest

from jmqttrpc.client import MQTTClient, BaseMQTTRPC, MQTTRPC
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

    if hasattr(request, "param"):
        need_mocks = request.param
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

    client.loop_stop()
    print("stop")

@pytest.yield_fixture(scope="class")
def unlive_client():
    client_id = get_random_id()
    client = MQTTClient(client_id)
    yield client



@pytest.yield_fixture()
def mqttrpc():
    client_id = get_random_id()
    client = MQTTRPC(client_id)
    client.connect(MQTT_BORKER_URL, MQTT_BORKER_PORT)
    print("rpc connect")
    client.loop_start()
    time.sleep(1)
    yield client
    client.loop_stop()
    print("rpc stop")



