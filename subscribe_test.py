#!/usr/bin/env python
'''
Create a python client to test SUBSCRIBING to an MQTT publisher
This was created with much help from https://www.digikey.com/en/maker/blogs/2019/how-to-use-mqtt-with-the-raspberry-pi

'''
import paho.mqtt.client as mqtt
import datetime
import time
import sys, getopt, os
import signal


msgAttempts = 0
messagesReceived = 0

def helpMsg():
    msg = '''
    subscribe_test.py
    This python script can be used to test mqtt broker's subscribe function.
    Usage:
        python3 subscribe_test.py <options>

        Options:
        -b, --broker: The address on the network for the broker (default:localhost)
        -c, --client: Name to use for this client.  (default: Test_Scriber)
        -h, --help: Displays this message.
        -m, --message: The payload for publisher.  Not used here (default:None)
        -p, --password: The password to use for the broker. (default: None)
        -q, --qos: The quality of service (0, 1, 2) (default:0)
        -r, --retain: if set to True, the will message will be set as the 
                      "last known good"/retained message for the topic.
                      Valid values: True or False
        -t, --topic: Topic to monitor (default: Test)
        -u, --username: User name for the broker (default: None)
        -w, --wait-time: Times between loop (default: 1 sesc)
    '''
    return msg


def signal_handler(sig, frame):
    '''Handler to handle when user presses ctrl-c
This implementation simply answers 'Done' and exits with a 0'''
    
    print('Done')
    sys.exit(0)
def getAppOptions(argv):
    mName = os.environ.get('MQTTNAME')
    broker = ('localhost', mName)[mName == None]
    cn = "Test_Subscriber"
    msg = None
    psw = os.environ.get('PSWVAL')
    qos = 0
    retain = False
    topic = 'Test'
    userName = os.environ.get('USERNAME')
    waitTime = 1
    
    if len(argv) == 0:
        return (broker, cn, msg, psw, qos, retain, topic, userName, waitTime)
    
    try:
        opts, args = getopt.getopt(argv, "b:c:hm:p:q:r:t:u:w:", 
                     ["broker=", "client=", "help", "message=", "password=",
                     "qos=", "retail=", "topic=", "username=", "wait-time="])
    except getopt.GetoptError:
        helpmsg = helpMsg()
        print (helpmsg)
        sys.exit(2)
    
    print(f'options:\n{opts}')
    for opt, arg in opts:
        if opt in ("-b", "--broker"):
            broker = arg
        elif opt in ("-c", "--client"):
            cn = arg
        elif opt in ("-h", "--help"):
            helpmsg = helpMsg()
            print(helpmsg)
            sys.exit()
        elif opt in ("-m", "--message"):
            msg = arg
        elif opt in ("-p", "--pasword"):
            psw = arg
        elif opt in ("-q", "--qos"):
            qos = int(arg)
        elif opt in ("-r", "--retail"):
            retain = bool(arg)
        elif opt in ("-t", "--topic"):
            topic = arg
        elif opt in ("-u", "--username"):
            userName = arg
        elif opt in ("-w", "--wait-time"):
            print(f'Wait Time in the command line: {arg}')
            waitTime = float(arg)
            
    return (broker, cn, msg, psw, qos, retain, topic, userName, waitTime )
    


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
    return {'time': fnow, 'topic': topic, 'message':message}
    
def on_message(client, userdata, message):
    '''
    Message callback function
    This is the on message event.  The function will be
    '''

    global messagesReceived
    print('A message was received')
    mDict = assembleMessage(client, userdata, message)
    print(f'The Message: {mDict}')
    client.loop_stop()
    print('Stopped client')
    client.disconnect()
    print('Disconnected')
    messagesReceived += 1

def on_connect(client, topic, flags, rc):
    '''Callback function called when the client connects.
    Simply prints a connection confirmation message
    '''

    global msgAttempts
    if msgAttempts == 0:
        print(f'Subscribing to topic:{topic}')
        fields = (
            "_clean_session",
            "_client_id",
            "_username",
            "_password",
            "_will_topic",
            "_will_payload",
            "_will_qos",
            "_will_retain",
            "_host",
            "_port",
            "_ssl",
            "_ssl_context",
            "_tls_insecure"
        )
        print('Client Data:')
        for key in client.__dict__:
            if key in fields:
                print(f'Var: {key}\tValue:{client.__dict__[key]}')
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

def main(argv):
    global messagesReceived
    # Handler for ctrl-c press
    signal.signal(signal.SIGINT, signal_handler)
    broker, cn, msg, psw, qos, retain, topic, userName, waitTime = getAppOptions(argv)
    print(f'broker:{broker}\ncn:{cn}\nmsg:{msg}\npsw:{psw}\nqos:{qos}\nretain:{retain}\ntopic:{topic}\nuserName:{userName}\nwaitTime:{waitTime}\n')

    ourClient = mqtt.Client(client_id=cn, userdata=topic)
    ourClient.username_pw_set(userName, psw)
    ourClient.will_set(topic, payload=msg, qos=qos, retain=retain)
    # ourClient.user_data_set(cn)
    ourClient.on_connect = on_connect
    ourClient.on_disconnect = on_disconnect
    ourClient.on_message = on_message

    ourClient.connect_async(broker, port=1883)

    ourClient.loop_start()    # Blocking call to process network traffic


    while(True):
        if messagesReceived == 0:
            now = datetime.datetime.now()
            fNow = now.strftime("%Y-%m-%d %H:%M:%S")
            print(f'Waiting... {fNow}')
            time.sleep(waitTime)
        else:
            sys.exit(0)
        
if __name__ == "__main__":
    main(sys.argv[1:])
    