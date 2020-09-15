#!/usr/bin/env python
import json
import configparser
import random
import string
import os

from dotenv import load_dotenv
import requests
import click


load_dotenv()

config = configparser.ConfigParser()
config._interpolation = configparser.ExtendedInterpolation()
config.read('opengate.ini')

HOST = config['opengate']['host']
PORT = config['opengate']['port']
ORGANIZATION = config['admin']['organization']
CHANNEL = config['admin']['channel']
API_KEY = config['admin']['api_key']
URL_OPS = config['opengate']['url_ops']

session = requests.Session()
session.headers.update({'X-ApiKey': API_KEY})

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def get_job(device_id):
    return {
        "job": {
            "request": {
                "operationParameters": {
                    "timeout": 90000,
                    "retries": 0,
                    "retriesDelay": 0
                },
                "name": "SET_DEVICE_PARAMETERS",
                "schedule": {
                    "stop": {
                        "delayed": 120000
                    }
                },
                "parameters": {
                    "variableList": [
                        {
                            "name": "q",
                            "value": "180"
                        }
                    ]
                },
                "target": {
                    "append": {
                        "entities": ["sensehat01"]
                    }
                },
                "active": True
            }
        }
    }


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0.0')
def op():

    pass


@op.command()
@click.argument('id')
def send_op(**kwargs):
    print('Operation execution')
    identifier = str(kwargs['id'])
    json_to_send = get_job(identifier)
    response = session.post(URL_OPS, json=json_to_send)
    print(json.dumps(response.json(), indent=2))


if __name__ == '__main__':
    op()
