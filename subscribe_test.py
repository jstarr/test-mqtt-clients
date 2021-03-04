#!/home/pi/GitHub/test-mqtt-clients/env/bin/python
'''
Create a python client to test SUBSCRIBING to an MQTT publisher
This was created with much help from
https://www.digikey.com/en/maker/blogs/2019/how-to-use-mqtt-with-the-raspberry-pi

'''
import signal
import argh
import sys
import time
from mqttConnectError import MQTTConnectionError
from mqtt_assistant import Mqtt_Assistant


def on_connect(client, topic, flags, rc, fnow):
    '''Simply subscribe to our topic
    '''

    #   We subscribe to the topic in this on_connect function
    client.subscribe(topic.strip())


def main(broker: 'The name of the MQTT broker server' = None,
         cn: 'The name of the subscriber' = "Test_Subscriber",
         msg: 'You may ignore this for subscribe_test.py' = None,
         port: 'The port the broker is using' = 1883,
         Psw: 'Broker password for this user name' = None,
         qos: 'The quality of service level to use' = 0,
         retain: 'True, will message set  "last known good message".' = False,
         topic: 'The topic we will listen for' = 'Test',
         userName: 'Set a username for broker authentication' = None,
         waitTime: 'Time between printing a "."' = 1):

    #   ClientWork is where most of the real work is performed.
    clientWorker = Mqtt_Assistant(__file__, broker, cn, msg, port, Psw, qos,
                                  retain, topic, userName)
    clientWorker.set_out_connect(on_connect)

    # Handler for ctrl-c press
    signal.signal(signal.SIGINT, clientWorker.signal_handler)

    clientWorker.loop()
    try:

        nloop = 0
        while(True):
            if waitTime:
                nloop += 1
                sys.stdout.write('.')
                if nloop == 60:
                    sys.stdout.write('\n')
                    nloop = 0
                sys.stdout.flush()
            time.sleep(waitTime)
    except MQTTConnectionError:
        print(MQTTConnectionError.message)
        clientWorker.allDone()
    except SystemExit:
        return


if __name__ == "__main__":
    v = sys.version
    print(f'Python Version being used: {v}')
    argh.dispatch_command(main)
