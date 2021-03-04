'''
Intended to be raised when there is a connection error to the MQTT broker.
'''


class MQTTConnectionError(Exception):
    '''Error raised when a Paho MQTT app detects a connection error to
    an MQTT broker

    NOTE: Connection error messages were found at:
        http://www.steves-internet-guide.com/client-connections-python-mqtt/

    Attributes:
        connectionError: Connection error number (Integer)
        client: (Optioinal) mqtt.Client used to connect to broker and failed
        message: (Optioinal) Custom error message
    '''

    connectionMsg = ['Connection successful',
                     'Connection refused – incorrect protocol version',
                     'Connection refused – invalid client identifier',
                     'Connection refused – server unavailable',
                     'Connection refused – bad username or password',
                     'Connection refused – not authorised']
    # message = None

    def __init__(self, connectionError, client=None, message=None):
        self._client = client
        if message:
            self.message = message
        else:
            self.message = self.connectionMsg[connectionError]
            print(f'Error: {self.message}')
        super().__init__(self.message)

    def __str__(self):
        return self.message
