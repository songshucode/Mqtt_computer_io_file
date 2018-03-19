#   time:       2018-3-17
#   author:     songshu
#   functions:  using mqtt technology to send message to edison board
#               to control the led on the board
#   version:    Python: 3.6.1
#               paho-mqtt: 1.3.1

import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("chat_wjj")
    client.publish("chat_wjj", json.dumps({"user": user, "say": "Helloanyone!"}))


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    print(payload.get("user")+":"+payload.get("say"))


if __name__ == '__main__':
    client = mqtt.Client()
    client.username_pw_set("admin", "password")  # 必须设置，否则会返回「Connected with result code 4」
    client.on_connect = on_connect
    client.on_message = on_message

    # HOST = "iot.eclipse.org"
    HOST = "111.231.222.203"

    client.connect(HOST, 1883, 60)

    user = input("please input your nema:")
    client.user_data_set(user)

    client.loop_start()

    while True:
        str = input()
        if str:
            client.publish("chat_wjj", json.dumps({"user": user, "say": str}))