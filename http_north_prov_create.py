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
API_KEY = os.getenv("API_KEY")
URL_PROV = config['opengate']['url_prov']

session = requests.Session()
session.headers.update({'X-ApiKey': API_KEY})

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def randomString(stringLength=4):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def get_asset(identifier):

    return {
        "resourceType": {"_value": {"_current": {"value": "entity.asset"}}},
        "provision.asset.identifier": {"_value": {"_current": {"value": identifier}}},
        "provision.administration.organization": {
            "_value": {"_current": {"value": ORGANIZATION}}
        },
        "provision.administration.channel": {
            "_value": {"_current": {"value": CHANNEL}}
        },
        "provision.administration.serviceGroup": {
            "_value": {"_current": {"value": "emptyServiceGroup"}}
        },
        "provision.asset.location": {
            "_value": {
                "_current": {
                    "value": {"position": {"coordinates": [-3.6655122, 40.47799439]}}
                }
            }
        },
        "provision.ccare.firstname": {
            "_value": {"_current": {"value": '{0}-{1}-firstname'.format(identifier, randomString())}}
        },
        "provision.ccare.surname": {
            "_value": {"_current": {"value": '{0}-{1}-surname'.format(identifier, randomString())}}
        },
    }


def get_device(id, asset_id):
    return {
        "resourceType": {"_value": {"_current": {"value": "entity.device"}}},
        "provision.device.identifier": {
            "_value": {
                "_current": {
                    "value": id
                }
            }
        },
        "provision.administration.organization": {
            "_value": {
                "_current": {
                    "value": ORGANIZATION
                }
            }
        },
        "provision.administration.channel": {
            "_value": {
                "_current": {
                    "value": CHANNEL
                }
            }
        },
        "provision.administration.serviceGroup": {
            "_value": {
                "_current": {
                    "value": "emptyServiceGroup"
                }
            }
        },
        "provision.device.specificType": {
            "_value": {
                "_current": {
                    "value": "SENSOR"
                }
            }
        },
        "provision.device.administrativeState": {
            "_value": {
                "_current": {
                    "value": "ACTIVE"
                }
            }
        },
        "provision.device.operationalStatus": {
            "_value": {
                "_current": {
                    "value": "NORMAL"
                }
            }
        },
        "provision.device.related": {
            "_value": {
                "_current": {
                    "value": asset_id
                }
            }
        },
        "provision.device.name": {
            "_value": {
                "_current": {
                    "value": "Heart rate sensor"
                }
            }
        },
        "provision.device.description": {
            "_value": {
                "_current": {
                    "value": "Heart rate sensor"
                }
            }
        },
        "provision.device.serialNumber": {
            "_value": {
                "_current": {
                    "value": randomString(stringLength=8)
                }
            }
        }
    }


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0.0')
def asset():
    pass


@asset.command()
@click.argument('id')
def create_asset(**kwargs):
    print('Asset creation')
    identifier = str(kwargs['id'])
    asset_to_create = get_asset(identifier)
    response = session.post(URL_PROV, json=asset_to_create)
    print(json.dumps(response.json(), indent=2))


@asset.command()
@click.argument('id')
@click.argument('asset_id')
def create_device(**kwargs):
    print('Device creation')
    id = str(kwargs['id'])
    asset_id = str(kwargs['asset_id'])
    device_to_create = get_device(id, asset_id)
    response = session.post(URL_PROV, json=device_to_create)
    print(json.dumps(response.json(), indent=2))


if __name__ == '__main__':
    asset()
