import eventlet
eventlet.monkey_patch()

import json
import time
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("connected")

def on_pubish(client, userdata, mid):
    print("on publish d: %s, mid: %s" % (userdata, mid))

def on_subscribe(client, userdata, mid):
    print("on subscribe: %s, mid: %s" % (userdata, mid))

def _get_mid():
    return 1


client = mqtt.Client()
# client._mid_generate = _get_mid
client.on_connect = on_connect
client.on_publish = on_pubish
# print(client.topic_matches_sub('/rpc/v1/+/+/'))
client.connect("127.0.0.1", 1883, 60)

client.loop_start()


count = 0
# while True:
start = time.time()
for i in range(20):
    count += 1
    ret = client.publish("/cereson/yc_a045/deliver", json.dumps({"slot_id": count}), qos=1)
    print("publish ret: %s" % ret)
t = time.time()-start
print(t)
while True:
    print(t)
    time.sleep(1)

