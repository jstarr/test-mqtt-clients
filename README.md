# test-mqtt-clients
Experiments python code to publish to and subscribe from an MQTT broker

## publish_test.py
### Usage and Command Line Parameters:

    This python script can be used to test mqtt broker's subscribe function.
    Usage:
        python3 subscribe_test.py <options>

        Options:
        -b, --broker: The address on the network for the broker (default:localhost)
        -c, --client: Name to use for this client.  (default: Test_Scriber)
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
        -w, --wait-time: Times between loop (default: 1 sesc)


## subscribe_test.py
### Usage and Command Line Parameters

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
