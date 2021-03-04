'''Assistant for publish_test.py and subscribe.py.
These 2 apps have a number of common features.  I have put them in here
to simplify things.
'''
from mqttConnectError import MQTTConnectionError
import paho.mqtt.client as mqtt
import datetime
import sys
import os


class Mqtt_Assistant():
    '''Class to contain common attributes used for PAHO MQTT applications.
    In particular publish_test.py and subscribe_test.py
        Arguments:
            fileName: The name of the calling file
            broker: 'The name of the MQTT broker server'
            cn: The name of the subscriber
            msg: You may ignore this for subscribe_test.py
            port: Port used by the broker
            Psw: Broker password for this user name
            qos: The quality of service level to use
            retain: True, will message set  "last known good message"
            topic: The topic we will listen for
            userName: Set a username for broker authentication
            ourClient (optional) A paho.mqtt.client object
    '''

    def __init__(self, fileName, broker, cn, msg, port, Psw, qos, retain,
                 topic, userName, ourClient=None):
        self.fileName = fileName
        self.broker = broker
        self.cn = cn
        self.msg = msg
        self.port = port
        self.psw = Psw
        self.qos = qos
        self.retain = retain
        self.topic = topic
        self.userName = userName
        self.ourClient = ourClient
        self.isNotConnected = True

        # Set up the client for runing
        self.ourClient.username_pw_set(self.userName, self.psw)
        self.ourClient.will_set(topic, payload=self.msg,
                                qos=self.qos, retain=self.retain)
        self.ourClient.on_connect = self.on_connect
        self.ourClient.on_disconnect = self.on_disconnect
        self.ourClient.on_message = self.on_message
        self.ourClient.on_publish = self.on_publish
        self._messagesReceivedCounter = 0
        self._mqttMsg = None

    @property
    def fileName(self):
        return self._fileName

    @fileName.setter
    def fileName(self, fileName):
        self._fileName = fileName

    @property
    def broker(self):
        return self._broker

    @broker.setter
    def broker(self, broker):
        self._broker = broker if broker else os.environ.get('MQTTNAME')

    @property
    def cn(self):
        return self._cn

    @cn.setter
    def cn(self, cn):
        self._cn = cn

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, msg):
        currentTime = self.timeStamp()
        self._msg = f'{msg} ({currentTime})'
        return

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        if port:
            self._port = port
        else:
            self._port = 1883   # Default value

    @property
    def psw(self):
        return self._psw

    @psw.setter
    def psw(self, Psw):
        self._psw = Psw if Psw else os.environ.get('PSWVAL')

    @property
    def qos(self):
        return self._qos

    @qos.setter
    def qos(self, qos):
        self._qos = qos

    @property
    def retain(self):
        return self._retain

    @retain.setter
    def retain(self, retain):
        self._retain = retain

    @property
    def topic(self):
        return self._topic

    @topic.setter
    def topic(self, topic):
        self._topic = topic

    @property
    def userName(self):
        return self._userName

    @userName.setter
    def userName(self, userName):
        self._userName = userName if userName else os.environ.get('USERNAME')

    @property
    def ourClient(self):
        return self._ourClient

    @ourClient.setter
    def ourClient(self, client=None):
        '''Create the mqttclient object for this class'''
        if client:
            self._ourClient = client
        else:
            self._ourClient = mqtt.Client(
                client_id=self.cn, userdata=self.topic)

    @property
    def messagesReceivedCounter(self):
        return self._messagesReceivedCounter

    @messagesReceivedCounter.setter
    def messagesReceivedCounter(self, messagesReceivedCounter):
        self._messagesReceivedCounter = messagesReceivedCounter

    def displayInit(self):
        '''Display the values sent to initialize this object
        Arguments:
            fileName: The name of the calling file
            broker: 'The name of the MQTT broker server'
            cn: The name of the subscriber
            msg: You may ignore this for subscribe_test.py
            Psw: Broker password for this user name
            qos: The quality of service level to use
            retain: True, will message set  "last known good message"
            topic: The topic we will listen for
            userName: Set a username for broker authentication
        '''
        confidential = '***'  # Print this instead of confidential info
        msg = f'broker: {self.broker}, cn: {self.cn}'
        if self.msg:
            msg += f', msg:{self.msg}'

        # msg += f'Psw:{confidential}, qos:{self.qos}, retain:{self.retain}'
        msg += f'Psw:{self.psw}, qos:{self.qos}, retain:{self.retain}'
        # msg += f', topic:{self.topic}, userName:{confidential}'
        msg += f', topic:{self.topic}, userName:{self.userName}'
        print(f'Running {self.fileName} with the following parameters\n',
              f'{msg}')

    def timeStamp(self, tFormat="%Y-%m-%d %H:%M:%S"):
        '''Create a timestamp string and return it
        Arguments:
            tFormat - (Optional)How to format the timestamp.
                    Default: "%Y-%m-%d %H:%M:%S"

        Returns a string with the current timestamp formatted as specified
        '''

        now = datetime.datetime.now()
        fnow = now.strftime(tFormat)
        return fnow

    def allDone(self):
        '''This implementation simply answers 'Done' and exits with a 0'''

        if self.ourClient:
            self.ourClient.loop_stop()
            self.ourClient.disconnect()
        print('Done')
        sys.exit(0)

    def on_connect(self, client, topic, flags, rc):
        '''Callback function called when the client connects.
        Simply prints a connection confirmation message.
        '''

        if rc:
            raise MQTTConnectionError(rc)

        fnow = self.timeStamp()

        self._out_connect(client, topic, flags, rc, fnow)

    @staticmethod
    def _out_connect(client, topic, flags, rc, fnow):
        '''This function can be replaced by an outside app and is called
        by the on_connect of this class.  Otherwise it displays the time
        we connected to the broker
        '''
        print(f"Connected with result code {rc} at {fnow}")

    def on_disconnect(self, client, userdata, rc):
        '''Callback function called when the client sends a disconnect.
        Simply prints a disconnect message
        '''
        fnow = self.timeStamp()
        print(f'\nDisconnected: {rc} at {fnow}')

        self._out_disconnect(client, userdata, rc)

    @staticmethod
    def _out_disconnect(client, userdata, rc):
        '''This function can be replaced by an outside app and is called
        by the on_disconnect of this class.  Otherwise is does nothing
        Parameters:
        client -
        '''
        pass

    def on_message(self, client, userdata, message):
        '''
        Message callback function
        This is the on message event.  The function will be
        '''

        self._messagesReceivedCounter += 1
        mDict = self.assembleMessage(client, userdata, message)
        self._out_message(client, userdata, self._messagesReceivedCounter,
                          self._messagesReceivedCounter, mDict)

    @staticmethod
    def _out_message(client, userdata, message, messagesReceivedCounter=None,
                     mDict=None):
        '''This function can be replaced by an outside app and is called
        by the on_message of this class.  Otherwise it prints the message with
        a timestamp
        '''
        print(f'#{messagesReceivedCounter} received at ',
              f'{mDict["time"]}',
              f'\nTopic: {mDict["topic"]}', f'Message: {mDict["message"]}\n')

    def on_publish(self, client, userdata, mid):
        '''Called when a message that was to be sent using the publish() call
        has completed transmission to the broker. For messages with QoS
        levels 1 and 2, this means that the appropriate handshakes have
        completed. For QoS 0, this simply means that the message has left the
        client. The mid variable matches the mid variable returned from the
        corresponding publish() call, to allow outgoing messages to be tracked.
    This callback is important because even if the publish() call returns
    success, it does not always mean that the message has been sent.
        '''
        # if self._mqttMsg.rc == mqtt.MQTT_ERR_SUCCESS:
        #     self._out_publish(client, userdata, mid)
        # else:
        #     raise Exception('Error publishing message ', self._mqttMsg.rc)
        self._out_publish(client, userdata, mid)

    @staticmethod
    def _out_publish(client, userdata, mid):
        '''This function can be replaced by an outside app and is called
        by the on_publish of this class.  Otherwise it prints Message sent...
        '''
        pass

    def publish(self, msg=None):
        '''Publish a message to the broker
        Parameters:
        topic - The topic for the message
        '''
        if self.isNotConnected:
            self.connect()

        msg = msg if msg else self._msg
        self._mqttMsg = self.ourClient.publish(
            self.topic, msg, self.qos, self.retain)

        if self._mqttMsg.rc:
            raise MQTTConnectionError(self._mqttMsg.rc)

        return self._mqttMsg

    def assembleMessage(self, client, userdata, message):
        '''This function will assemble a final dictionary to send to the database
            Usage:
                msgDictionary = assembleMessage(client, userdata, message)
            Where:
                client - client instance
                userdata - the private user data as set in Client() or
                           user_data_set()
                message - instance of MQTTMessage.  Contains topic, payload,
                          qos and retain
            '''

        topic = str(message.topic)
        message = str(message.payload.decode('utf-8'))
        fnow = self.timeStamp()
        return {'time': fnow, 'topic': topic, 'message': message}

    def set_out_connect(self, out_connect):
        self._out_connect = out_connect

    def set_out_disconnect(self, out_disconnect):
        self._out_disconnect = out_disconnect

    def set_out_message(self, out_message):
        self._out_message = out_message

    def set_out_publish(self, out_publish):
        self._out_publish = out_publish

    def signal_handler(self, sig, frame):
        '''Handler to handle when user presses ctrl-c'''

        self.allDone()

    def connect_async(self):
        '''Connect to the broker'''
        self.displayInit()
        self._ourClient.connect_async(self.broker, self.port)
        self.isNotConnected = False

    def connect(self):
        '''Connect to the broker'''
        self.displayInit()
        self._ourClient.connect(self.broker, self.port)
        self.isNotConnected = False

    def loop(self):
        '''Make it all work'''
        if self.isNotConnected:
            self.connect_async()
        """Calling loop_start() once, before or after connect*(), runs a thread in
        the background to call loop() automatically."""
        self.ourClient.loop_start()
