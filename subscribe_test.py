#!/usr/bin/env python
'''
Create a python client to test SUBSCRIBING to an MQTT publisher
This was created with much help from https://www.digikey.com/en/maker/blogs/2019/how-to-use-mqtt-with-the-raspberry-pi

'''
import paho.mqtt.client as mqtt
import datetime
import time
import sys
import getopt
import argh
import os
import signal


msgAttempts = 0
messagesReceived = 0


def signal_handler(sig, frame):
    '''Handler to handle when user presses ctrl-c
This implementation simply answers 'Done' and exits with a 0'''

    print('Done')
    sys.exit(0)


def assembleMessage(client, userdata, message):
    '''This function will assemble a final dictionary to send to the database
    Usage:
        msgDictionary = assembleMessage(client, userdata, message)
    Where:
        client - client instance
        userdata - the private user data as set in Client() or user_data_set()
        message - instance of MQTTMessage.  Contains topic, payload, qos and retain
    '''

    topic = str(message.topic)
    message = str(message.payload.decode('utf-8'))
    now = datetime.datetime.now()
    fnow = now.strftime("%Y-%m-%d %H:%M:%S")
    return {'time': fnow, 'topic': topic, 'message': message}


def on_message(client, userdata, message):
    '''
    Message callback function
    This is the on message event.  The function will be
    '''

    global messagesReceived
    messagesReceived += 1
    print(f'Message #{messagesReceived} was received')
    mDict = assembleMessage(client, userdata, message)
    print(f'\tThe Message Received:')
    for key, value in mDict.items():
        print(f'\t{key}: {value}')
    print()
    # client.loop_stop()
    # print('Stopped client')
    # client.disconnect()
    # print('Disconnected')


def on_connect(client, topic, flags, rc):
    '''Callback function called when the client connects.
    Simply prints a connection confirmation message
    '''

    global msgAttempts
    if msgAttempts == 0:
        print(f'Subscribing to topic:{topic} with flags:{flags}')
        fields = (
            "_client_id",
            "_username",
            "_password",
            "_will_topic",
            "_will_qos",
            "_will_retain",
            "_host",
            "_port",
            "_ssl",
            "_ssl_context",
            "_tls_insecure"
        )
        print('Client Data:')
        for key, value in client.__dict__.items():
            if key in fields:
                if len(key) <= 10:
                    tabs = '\t\t'
                else:
                    tabs = '\t'
                print(f'Var: {key}{tabs}Value:{value}')
        msgAttempts += 1
    now = datetime.datetime.now()
    fnow = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"Connected {__file__} with result code {rc} at {fnow}")
    client.subscribe(topic)


def on_disconnect(client, userdata, rc):
    '''Callback function called when the client sends a disconnect.
    Simply prints a disconnect message
    '''
    now = datetime.datetime.now()
    fnow = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f'Disconnected: {rc} at {fnow}')


def main(broker: 'The name of the MQTT broker server' = None,
         cn: 'The name of the subscriber' = "Test_Subscriber",
         msg: 'You may ignore this for subscribe_test.py' = None,
         psw: 'Broker user name' = None,
         qos: 'The quality of service level to use' = 0,
         retain: 'True, will message set  "last known good message".' = False,
         topic: 'The topic we will listen for' = 'Test',
         userName: "Set a username for broker authentication" = None,
         waitTime=1):

    #   Actual defaults that come from the environment
    broker = broker if broker else os.environ.get('MQTTNAME')
    psw = psw if psw else os.environ.get('PSWVAL')
    userName = userName if userName else os.environ.get('USERNAME')

    global messagesReceived
    # Handler for ctrl-c press
    signal.signal(signal.SIGINT, signal_handler)

    print(f'broker:{broker}\ncn:{cn}\nmsg:{msg}\npsw:{psw}\n',
          f'qos:{qos}\nretain:{retain}\ntopic:{topic}\nuserName:{userName}\n',
          f'waitTime:{waitTime}\n')

    ourClient = mqtt.Client(client_id=cn, userdata=topic)
    ourClient.username_pw_set(userName, psw)
    ourClient.will_set(topic, payload=msg, qos=qos, retain=retain)
    ourClient.on_connect = on_connect
    ourClient.on_disconnect = on_disconnect
    ourClient.on_message = on_message

    ourClient.connect_async(broker, port=1883)

    ourClient.loop_start()    # Blocking call to process network traffic

    nloop = 0
    while(True):
        nloop += 1
        sys.stdout.write('.')
        if nloop == 60:
            sys.stdout.write('\n')
        sys.stdout.flush()
        time.sleep(waitTime)


if __name__ == "__main__":
    argh.dispatch_command(main)
