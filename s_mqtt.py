#   time:       2018-3-17
#   author:     website
#   function:   using mqtt technology to send and receive message
#   version:    Python: 3.6.1
#               paho-mqtt: 1.3.1

import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    print("Connected with result code" + str(rc))

    client.subscribe("chat")
    client.publish("chat", json.dumps({"user": user, "say": "Hello,anyone!"}))

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(payload.get("user") + ":" + payload.get("say"))
    except:
        print(msg.payload.decode())


if __name__ == '__main__':
    client = mqtt.Client()
    client.username_pw_set("admin", "password")
    client.on_connect = on_connect
    client.on_message = on_message

    HOST = "iot.eclipse.org"

    client.connect(HOST, 1883, 60)

    user = input("Please input name:")
    client.user_data_set(user)

    client.loop_start()

    while True:
        str = input()
        if str:
            client.publish("chat", json.dumps({"user": user, "say": str}))