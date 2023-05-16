import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()
abe_sim_url = os.getenv('ABE_SIM_URL')


def process_response(response):
    if response.status_code == 200:
        return response.json()['response']
    else:
        print('Request failed with status code:', response.status_code)
        return None


def to_get_state():
    payload = {'kitchenStateIn': '?kitchen-state-1'}
    response = requests.post(f'{abe_sim_url}/to-get-kitchen', data=json.dumps(payload))
    return process_response(response)


def to_fetch(kitchen_object):
    payload = {'object': kitchen_object, 'kitchenStateIn': None, 'setWorldState': False}
    print(payload)
    response = requests.post(f'{abe_sim_url}/to-fetch', data=json.dumps(payload))
    return process_response(response)


def to_cut(kitchen_object, cutting_tool):
    payload = {'object': kitchen_object, 'cuttingTool': cutting_tool, 'cutPattern': 'dice', 'kitchenStateIn': None,
               'setWorldState': False}
    response = requests.post(f'{abe_sim_url}/to-cut', data=json.dumps(payload))
    return process_response(response)


def to_bake(kitchen_object, oven, destination_container):
    payload = {'thingToBake': kitchen_object, 'oven': oven, 'inputDestinationContainer': destination_container,
               'kitchenStateIn': None, 'setWorldState': False}
    response = requests.post(f'{abe_sim_url}/to-bake', data=json.dumps(payload))
    return process_response(response)
