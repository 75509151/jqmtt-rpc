import eventlet
eventlet.monkey_patch()
import time
import uuid



from jmqttrpc.client import MQTTClient, BaseMQTTRPC, MQTTRPC
from config import MQTT_BORKER_URL, MQTT_BORKER_PORT, BATCH_TEST_SERVICE_NAME


def get_random_id():
    return str(uuid.uuid4())

def call_service(ind=0, service_name=BATCH_TEST_SERVICE_NAME):
    try:
        client_id = get_random_id()
        client = MQTTRPC(client_id)

        client.connect(MQTT_BORKER_URL, MQTT_BORKER_PORT)
        client.loop_start()

        ret = client.call(service_name,"test",{"l":1,"p":2},
                            timeout=30)

        print(ind, ret)

        return ret
    except Exception as e:
        print(str(e))
    finally:
        client.loop_stop()


def pool_run(pool_count=100):
    results = []
    pool = eventlet.GreenPool(pool_count)
    for i in range(pool_count):
        ret = pool.spawn(call_service, i)
        results.append(ret)
    time.sleep(100)




if __name__ == "__main__":
    # ret = call_service()
    # print(ret)
    pool_run()

