import time
import uuid
import pytest
from unittest.mock import MagicMock
import unittest
import inspect
import paho.mqtt.client as mqtt

from jmqttrpc.erros import StateError
from jmqttrpc.client import MQTTClient, BaseMQTTRPC, MQTTRPC
from .utils import get_random_id



class TestMQTTClient:

    def test_subscribe_in_wrong_state(self, unlive_client):
        with pytest.raises(StateError):
            topic = "123"
            unlive_client.subscribe(topic, "")

    def test_unsubscribe_in_wrong_state(self, unlive_client):
        with pytest.raises(StateError):
            topic = "123"
            unlive_client.unsubscribe(topic)

    def test_public_in_wrong_state(self, unlive_client):

        with pytest.raises(StateError):
            topic = "123"
            unlive_client.publish(topic, "")


class TestBaseMQTTClient:

    @pytest.mark.parametrize("basemqttrpc", [["subscribes_rpc_topics", ]], indirect=True)
    def test_on_mqtt_connect(self, basemqttrpc):
        assert basemqttrpc.subscribes_rpc_topics.call_count == 1


    @pytest.mark.parametrize("basemqttrpc", [["handle_unkwon_msg", ]], indirect=True)
    def test_handle_unkown_msg(self, basemqttrpc, mqttrpc):
        topic = "/test/test_on_mqtt_msg"
        basemqttrpc.subscribe(topic)
        time.sleep(1)
        mqttrpc.publish(topic, "hello")
        time.sleep(1)
        assert basemqttrpc.handle_unkwon_msg.call_count == 1




    @pytest.mark.parametrize("basemqttrpc", [["handle_reply_msg", ]], indirect=True)
    def test_handle_reply_msg(self, basemqttrpc, mqttrpc):
        topic = mqttrpc.REPLY_TOPIC_TMP.format(version=basemqttrpc.VERSION,
                                               service="ll",
                                               method="test",
                                               pid=get_random_id()
                                               )
        assert mqtt.topic_matches_sub(basemqttrpc.REPLY_TOPIC_MODEL, topic)
        basemqttrpc.subscribe(topic)
        time.sleep(1)
        mqttrpc.publish(topic, "test")
        time.sleep(1)
        assert basemqttrpc.handle_reply_msg.call_count == 1


    @pytest.mark.parametrize("basemqttrpc", [["handle_request_msg", ]], indirect=True)
    def test_handle_request_msg(self, basemqttrpc, mqttrpc):
        topic = mqttrpc.REQUEST_TOPIC_TMP.format(version=basemqttrpc.VERSION,
                                               service="hhah",
                                               method="test",
                                               pid=get_random_id()
                                               )
        assert mqtt.topic_matches_sub(basemqttrpc.REQUEST_TOPIC_MODEL, topic)
        basemqttrpc.subscribe(topic)
        time.sleep(1)
        mqttrpc.publish(topic, "test")
        time.sleep(1)
        assert basemqttrpc.handle_request_msg.call_count == 1


