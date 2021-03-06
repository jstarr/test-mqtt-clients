#!./bin/python
'''
Create a python client to test PUBLISHING to an MQTT publisher
This was created with much help from https://www.digikey.com/en/maker/blogs/2019/how-to-use-mqtt-with-the-raspberry-pi

Usage:
    publish_test.py options
    Where the options are:
    -h -- Display the help message
    -m -- The message to send (defaults to 'This is just a test #')
    -p -- The password for the broker (defaults to None)
    -q -- The quality of server (defaults to 0.  Must be 0, 1 or 2)
    -r -- if set to True, the will message will be set as the "last known good"/retained message for the topic.
          (default: False.  Must be the word True or False)
    -t -- The topic to publish (defaults to 'Test')
    -u -- The username for the mqtt broker (defaults to None)
'''
import paho.mqtt.client as mqtt
import sys, getopt, os
import signal

def helpMsg():
    msg = '''
    subscribe_test.py
    This python script can be used to test mqtt broker's subscribe function.
    Usage:
        python3 subscribe_test.py <options>

        Options:
        -b, --broker: The address on the network for the broker (default:localhost)
        -c, --client: Name to use for this client.  (default: Test_publisher)
        -h, --help: Displays this message.
        -m, --message: The payload for publisher.  Not used here (default:None)
        -p, --password: The password to use for the broker. (default: None)
        -o, --poer: The port number of the broker
        -q, --qos: The quality of service (0, 1, 2) (default:0)
        -r, --retain: if set to True, the will message will be set as the
                      "last known good"/retained message for the topic.
                      Valid values: True or False
        -t, --topic: Topic to monitor (default: Test)
        -u, --username: User name for the broker (default: None)
    '''
    return msg

def toIntwDefault(val, default):
    try:
        y = int(val)
    except:
        y = default

    return y

def signal_handler(sig, frame):
    '''Handler to handle when user presses ctrl-c
This implementation simply answers 'Done' and exits with a 0'''

    print('Done')
    sys.exit(0)

def getAppOptions(argv):
    mName = os.environ.get('MQTTNAME')
    broker = ('localhost', mName)[mName == None]
    cn = "Test_publisher"
    msg = 'This is just a test #'
    port = 1883
    psw = os.environ.get('PSWVAL')
    qos = 0
    retain = False
    topic = 'Test'
    userName = os.environ.get('USERNAME')

    if len(argv) == 0:
        return (broker, cn, msg, psw, port, qos, retain, topic, userName)

    try:
        opts, args = getopt.getopt(argv, "b:c:hm:o:p:q:r:t:u:",
                     ["broker=", "client=", "help", "message=", "password=",
                     "port=", "qos=", "retail=", "topic=", "username="])
    except getopt.GetoptError as err:
        helpmsg = helpMsg()
        print (f'Command Line Error {err} Occured\n{helpmsg}')
        sys.exit(2)

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
            print(f'The message: {arg}.   The opt was {opt}')
            msg = arg
        elif opt in ("-o", "--port"):
            port = toIntwDefault(arg, port)
        elif opt in ("-p", "--pasword"):
            psw = arg
        elif opt in ("-q", "--qos"):
            qos = toIntwDefault(arg, qos)
        elif opt in ("-r", "--retail"):
            retain = bool(arg)
        elif opt in ("-t", "--topic"):
            topic = arg
        elif opt in ("-u", "--username"):
            userName = arg

    return (broker, cn, msg, psw, port, qos, retain, topic, userName)

def messageFunction(client, userdata, message):
    topic = str(message.topic)
    message = str(message.payload.decode("utf-8"))
    print(topic + message)

def on_connect(client, userdata, flags, rc):
    '''Callback function called when the client connects.
    Simply prints a connection confirmation message
    '''
    print(f"Connected {__file__} with result code {rc}")

def on_publish(client, userdata, mid):
    '''Called when a message that was to be sent using the publish() call has completed transmission to the broker. For messages with QoS levels 1 and 2, this means that the appropriate handshakes have completed. For QoS 0, this simply means that the message has left the client. The mid variable matches the mid variable returned from the corresponding publish() call, to allow outgoing messages to be tracked.
This callback is important because even if the publish() call returns success, it does not always mean that the message has been sent.
    '''
    if client.rc == mqtt.MQTT_ERR_SUCCESS:
        print('Message sent...')
    else:
        pring(f'Error # {client.rc}')

def on_disconnect(client, userdata, rc):
    '''Callback function called when the client sends a disconnect.
    Simply prints a disconnect message
    '''
    print(f'Disconnected: {rc}')

def main(argv):
    # Handler for ctrl-c press
    signal.signal(signal.SIGINT, signal_handler)

    run = True
    broker, cn, msg, psw, port, qos, retain, topic, userName = getAppOptions(argv)
    print(f'Broker: {broker}\nClient Name: {cn}\nMessage: {msg}')
    print(f'QOS: {qos}\nRetain:{retain}\nTopic:{topic}\nUser Name: {userName}')
    counter = 1
    ourClient = mqtt.Client(cn)
    ourClient.username_pw_set(userName, psw)
    ourClient.will_set('Oh I am slain')
    ourClient.on_connect = on_connect
    ourClient.on_disconnect = on_disconnect

    ourClient.connect(broker, port)
    while run:
        print(f'Publishing on topic: {topic} message: {msg}')
        mqttMsg = ourClient.publish(topic, msg + str(counter), qos, retain)
        print(f'{mqttMsg}')
        run = toIntwDefault(input(f"MQTTMessageInfo: {counter}> "), 0)
        counter += 1

    print('Complete')

if __name__ == "__main__":
    main(sys.argv[1:])
