#!/usr/bin/env python
import json
import time
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
API_KEY = os.getenv("API_KEY")
URL_SOUTH = config['opengate']['url_south']

session = requests.Session()
session.headers.update({'X-ApiKey': API_KEY})

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def print_json(json_as_dict, indent=2):
    if isinstance(json_as_dict, dict):
        print(json.dumps(json_as_dict, indent=indent))
    else:
        print(json_as_dict)


def randomString(stringLength=4):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def get_data_points(id, bps=72, presence=True):
    """
    Epoch or Unix time: https://en.wikipedia.org/wiki/Unix_time
    On-line tool: https://www.epochconverter.com/
    Example: 1593099453
    Assuming that this timestamp is in seconds:
    GMT: Thursday, June 25, 2020 3:37:33 PM
    Your time zone: Thursday, June 25, 2020 5:37:33 PM GMT+02:00 DST
    """
    epoch_time = int(time.time())

    return{
        "version": "1.0.0",
        "device": id,
        "datastreams": [
            {
                "id": "ccare.bps",
                "datapoints": [{"at": epoch_time, "value": bps}]
            },
            {
                "id": "ccare.presence",
                "datapoints": [{"at": epoch_time, "value": presence}]
            }
        ]
    }


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0.0')
def south():
    pass


@south.command()
@click.argument('id')
@click.option('-b', '--bps', default=72, help='Beats per second')
@click.option('-p', '--presence', is_flag=True, help='Presence detection')
def send(id, bps, presence):
    print('Send data points')
    data_points = get_data_points(id, bps, presence)
    print_json(data_points)
    response = session.post(URL_SOUTH.format(device_id=id), json=data_points)
    print_json(response)


if __name__ == '__main__':
    south()
