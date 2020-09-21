#!/usr/bin/env python
'''
This module emulates a device connected to OpenGate
using MQTT protocol.
'''

import json
import configparser
import threading
import os

from dotenv import load_dotenv
import click
import paho.mqtt.client as mqtt

from device_emulator_common import operation_step_response, reboot, update, set_device_parameters, refresh_info

load_dotenv()

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


class OpenGateMqtt():
    def __init__(self, host, port, user, password):
        super().__init__()
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self.ODM_SUBSCRIBE_TOPIC = 'odm/request/{0}'
        self.ODM_PUBLISH_RESPONSE_TOPIC = 'odm/response/{0}'
        self.ODM_PUBLISH_IOT_TOPIC = 'odm/iot/{0}'
        self.ODM_PUBLISH_ON_DEMAND = 'odm/operationOnDemand/{0}'
        self._client = None

    def on_connect(self, caller_mqtt_client, userdata, flags, result_code):
        '''`on_connect` callback implementation'''
        print('OpenGate MQTT client Connected with result code ' + str(result_code))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        request_topic = self.ODM_SUBSCRIBE_TOPIC.format(self._user)
        caller_mqtt_client.subscribe(request_topic, qos=1)
        print('Subscribed to "{}" topic'.format(request_topic))

    def on_message(self, caller_mqtt_client, userdata, message):
        '''`on_message` callback implementation'''

        print(message.topic + ' ' + str(message.payload))

        def publish_operation_step_response(content, device_id, name, result, close_operation):
            '''MQTT specific callback function to publish responses asynchronously'''
            step_response = operation_step_response(
                content, name, result, close_operation)
            step_response_as_json = json.dumps(step_response, indent=2)
            print('Publishing {0} step status {1}...'.format(name, result))
            print(step_response_as_json)
            caller_mqtt_client.publish(ODM_PUBLISH_RESPONSE_TOPIC.format(
                device_id), step_response_as_json, qos=1)
            print('...done')

        content = json.loads(message.payload)
        print('====================================')
        print('Request received with for device {0} with the following content'.format(
            self._user))
        print(json.dumps(content, indent=2))
        operation_name = content['operation']['request']['name']
        print('Operation name got: {0}'.format(operation_name))

        print('Response:')
        response_as_json = ''
        if operation_name == 'REBOOT_EQUIPMENT':
            response_as_json = json.dumps(
                reboot(content, self._user), indent=2)
        elif operation_name == 'REFRESH_INFO':
            response_as_json = json.dumps(
                refresh_info(content, self._user), indent=2)
        elif operation_name == 'SET_DEVICE_PARAMETERS':
            response_as_json = json.dumps(
                set_device_parameters(content, self._user), indent=2)
        elif operation_name == 'UPDATE':
            response_as_json = json.dumps(
                update(content, self._user, publish_operation_step_response), indent=2)

        print(response_as_json)
        # Message reception ACK
        caller_mqtt_client.publish(self.ODM_PUBLISH_RESPONSE_TOPIC.format(
            self._user), response_as_json, qos=1)

    def connect(self):
        client = mqtt.Client(client_id=self._user)
        client.username_pw_set(self._user, self._password)
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect(self._host, self._port, 60)
        print('Connecting to {}:{}'.format(self._host, self._port))
        # Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a manual interface.
        client.loop_forever()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0.0')
def op():
    pass


@op.command()
@click.argument('id')
def connect(**kwargs):
    device_id = str(kwargs['id'])
    api_key = os.getenv("API_KEY")

    config = configparser.ConfigParser()
    config._interpolation = configparser.ExtendedInterpolation()
    config.read('opengate.ini')

    host = config['opengate']['host']
    port = config.getint('opengate', 'mqtt_port')

    print('OpenGate MQTT client test')
    print('Device ID:{}'.format(device_id))
    mqtt_opengate = OpenGateMqtt(host, port, device_id, api_key)
    mqtt_opengate.connect()

    print('Bye')


if __name__ == '__main__':
    op()
