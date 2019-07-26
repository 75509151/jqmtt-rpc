import json
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("connected")


def on_message(client, userdata, msg):
    try:
        print("msg: %s " % (json.loads(msg.payload)["slot_id"]))
    except Exception as e:
        print (str(e))


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("mm", "howcute121")
client.connect("127.0.0.1", 1883, 60)

client.subscribe("/cereson/yc_a045/deliver")

client.loop_forever()

