import time
import uuid
from multiprocessing import Pool



from jmqttrpc.client import MQTTClient, BaseMQTTRPC, MQTTRPC
from config import MQTT_BORKER_URL, MQTT_BORKER_PORT, BATCH_TEST_SERVICE_NAME


def get_random_id():
    return str(uuid.uuid4())

def call_service(ind=0, service_name=BATCH_TEST_SERVICE_NAME):
    try:
        client_id = "retain_test"
        client = MQTTRPC(client_id, clean_session=False)

        client.connect(MQTT_BORKER_URL, MQTT_BORKER_PORT)
        client.loop_start()

        ret = client.call(service_name,"test",{"l":1,"p":2},
                            timeout=1, once=False)
        ret = client.call(service_name,"test",{"l":2,"p":2},
                            timeout=1, once=True)


        if not ret:
            raise Exception("timout")
        print(ret)

        client.stop()
        return ret
    except Exception as e:
        print(str(e))






if __name__ == "__main__":
    call_service()
    time.sleep(20)

