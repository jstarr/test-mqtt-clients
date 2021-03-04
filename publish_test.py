#!/home/pi/GitHub/test-mqtt-clients/env/bin/python
'''
Create a python client to test PUBLISHING to an MQTT publisher
This was created with much help from https://www.digikey.com/en/maker/blogs/2019/how-to-use-mqtt-with-the-raspberry-pi

Usage:
    publ{"name":"Python: Current File","type":"python","request":"launch","program":"${file}","console":"integratedTerminal"},ish_test.py options
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
import signal
import argh
from mqttConnectError import MQTTConnectionError
from mqtt_assistant import Mqtt_Assistant


def on_publish(client, userdata, mid):
    '''This version of the on_publish simply outputs a success message'''
    print('Message sucessfully sent...')


def main(broker: 'The name of the MQTT broker server' = None,
         cn: 'The name of the subscriber' = "Test_Publisher",
         msg: 'You may ignore this for subscribe_test.py' = None,
         port: 'The port the broker is using' = 1883,
         Psw: 'Broker password for this user name' = None,
         qos: 'The quality of service level to use' = 0,
         retain: 'True, will message set  "last known good message".' = False,
         topic: 'The topic we will listen for' = 'Test',
         userName: 'Set a username for broker authentication' = None):

    if (msg):
        #   ClientWork is where most of the real work is performed.
        clientWorker = Mqtt_Assistant(__file__, broker, cn, msg, port, Psw,
                                      qos, retain, topic, userName)
        clientWorker.set_out_publish(on_publish)

        # Handler for ctrl-c press
        signal.signal(signal.SIGINT, clientWorker.signal_handler)

        print(40*'-')
        print(f'Publishing on topic: {topic} message: {clientWorker.msg}')
        try:
            clientWorker.publish()
        except MQTTConnectionError:
            print(f'Publish error: {MQTTConnectionError}')

        clientWorker.allDone()

    else:
        print('Message is required for this to work.')
    print('Complete')


if __name__ == "__main__":
    argh.dispatch_command(main)
