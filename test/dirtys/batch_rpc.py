import time
import uuid
from multiprocessing.pool import ThreadPool as Pool



from jmqttrpc.client import MQTTClient, BaseMQTTRPC, MQTTRPC
from config import MQTT_BORKER_URL, MQTT_BORKER_PORT, BATCH_TEST_SERVICE_NAME


def get_random_id():
    return str(uuid.uuid4())

def call_service(ind=0, service_name=BATCH_TEST_SERVICE_NAME):
    try:
        client_id = get_random_id()
        client = MQTTRPC(client_id, clean_session=True)

        client.connect(MQTT_BORKER_URL, MQTT_BORKER_PORT)
        client.loop_start()

        ret = client.call(service_name,"test",{"l":1,"p":2},
                            timeout=100)
        if not ret:
            raise Exception("timout")
        print(ret)

        client.stop()
        return ret
    except Exception as e:
        print(str(e))


def evpool_run(pool_count=100):
    import eventlet
    results = []
    pool = eventlet.GreenPool(pool_count)
    for i in range(20000):
        ret = pool.spawn(call_service, i)
        results.append(ret)
    pool.waitall()


def pool_run(client_count=300):
    results = []
    pool = Pool(100)
    for i in range(client_count):
        pool.apply_async(call_service)
    pool.close()
    pool.join()




if __name__ == "__main__":
    # ret = call_service()
    # print(ret)
    # pool_run()
    pool_run(10000000)

