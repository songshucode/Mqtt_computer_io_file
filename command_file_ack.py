#      time:       2018-3-17
#      author:     songshu
#      function:   using mqtt technology
#                  send command and file to the device controled
#                  on the control part

import paho.mqtt.client as mqtt
import json
import time

NAME = 'control_1'
# HOST = "iot.eclipse.org"
HOST = '111.231.222.203'
PORT = 1883
time_start = 0
time_stop = 0
# # deal with the command from control
# def deal_cmd(cmd):
#     return
#
# # dela with the file data, and save it
# def deal_file(client, file_name, data):
#     with open('up/'+ file_name, 'w') as file:
#         file.write(data)
#     print('file have been done!')
#     client.publish('ack_message', json.dumps({'user':NAME, 'message':'the cmd have beed done!'}))

# connect function , do it just when connecting to the broker
def on_connect(client, userdata, flags, rc):
    # subscribe the title used, control_message and ack_message
    print('Connected with result code '+str(rc))
    client.subscribe('ack_message', qos=2)
    # client.subscribe('control_message')
    client.publish('control_message', json.dumps({'user': NAME , 'message': 'hello, I am here'}), qos=2)

# message function, do it just when broker have got the message
def on_message(client, userdatga, msg):
    payload = json.loads(msg.payload.decode())
    user = payload.get('user')
    message = payload.get('message')
    # data split to get the control_name, class and file_name
    print(user +':' + message)
    # print('time:', time.time())
    # print('qos:', msg.qos)
    # time_flag = 1
    # user = user.split(':')
    # # data error, it will happen when the first connect to the broker
    # if len(user) == 1:
    #     return
    # # get the cmd data
    # if user[1] == 'cmd':
    #     print('cmd')
    # # get the file data
    # if user[1] == 'file':
    #     deal_file(user[2], message)

def main():
# initialize the mqtt client
    client = mqtt.Client()
    client.username_pw_set('admin', 'password')
    client.on_connect = on_connect
    client.on_message = on_message
# connect the mqtt broker
    client.connect(HOST, PORT, 60)
# set the user name
    client.user_data_set(NAME)
# client start
    client.loop_start()
# system loop for getting command and file
    # test the time
    index = 0
    time_start = time.time()
    # while True:
    #     if index >= 10:
    #         print(time_stop-time_start , 's')
    #         return
    #     if time_flag:
    #         str = 'file:up/sa.txt'
    #         dataSet = ''
    #         try:
    #             # open the special file
    #             data_file = open(str[1], 'r')
    #             # read the data to a string
    #             for data in data_file:
    #                 dataSet = dataSet + data
    #         except:
    #             print('Error! Please input again.')
    #             data_file.close()
    #             continue
    #         data_file.close()
    #         # get the file name
    #         str = str[1].split('/')
    #         # send the data
    #         # user= control_name + class + file_name separated with ':'
    #         # message = a string containing all file content
    #         client.publish('control_message', json.dumps({'user': NAME + ':file:' + str[-1], 'message': dataSet}))
    #         index += 1
    #         time_flag = 0
    while True:
        str = input(NAME+': \n')
        # print('time:', time.time())
        str = str.split(':')
        if str[0] == 'cmd':
            client.publish('control_message', json.dumps({'user': NAME+':cmd', 'message': str[1]}), qos=2)
        if str[0] == 'file':
            dataSet = ''
            try:
                # open the special file
                data_file = open(str[1], 'r')
                # read the data to a string
                for data in data_file:
                    dataSet = dataSet + data
            except:
                print('Error! Please input again.')
                data_file.close()
                continue
            # get the file name
            str = str[1].split('/')
            # send the data
            # user= control_name + class + file_name separated with ':'
            # message = a string containing all file content
            print('time: ', time.time())
            for i in range(15):
                client.publish('control_message', json.dumps({'user':NAME+':file:'+str[-1], 'message':dataSet}), qos=2)
                time.sleep(0.06)
            # print('time: ', time.time())
        if str[0] == 'cook':
            client.publish('control_message', json.dumps({'user':NAME+':cook', 'message':str[1]+':'+str[2]}))

if __name__ == '__main__':
    main()