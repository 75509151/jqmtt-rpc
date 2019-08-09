import time
from jmqttrpc.client import MQTTClient, BaseMQTTRPC, MQTTRPC
from jmqttrpc.service import RPCService
from jmqttrpc.protocol import RPCProtocol
from jmqttrpc.rpcproxy import RPCProxy
from jmqttrpc.constants import *

from config import MQTT_BORKER_URL, MQTT_BORKER_PORT, BATCH_TEST_SERVICE_NAME

class RPCService4Batch(RPCService):
    def get_reponse(self, request):
        print("lll")
        time.sleep(5)
        return SUC, CODE_MSG[SUC], request.func


if __name__ == "__main__":
    config = {"service_name": BATCH_TEST_SERVICE_NAME,
              "client_id": "batch_test",
              "max_workers": 150,
              "clean_session": False}
    service = RPCService4Batch(config, None)
    service.connect(MQTT_BORKER_URL, MQTT_BORKER_PORT)
    service.loop_forever()

