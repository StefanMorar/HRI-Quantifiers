import json
import os
from functools import wraps

import requests
from dotenv import load_dotenv

load_dotenv()
abe_sim_url = os.getenv('ABE_SIM_URL')
has_state = False


def exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            print(f'Error occurred during {abe_sim_url} call in function {func.__name__}')
            raise SystemExit(e)

    return wrapper


def process_response(response):
    if response.status_code == 200:
        return response.json()['response']
    else:
        print('Request failed with status code:', response.status_code)
        return None


@exception_handler
def to_get_state():
    payload = {'kitchenStateIn': '?kitchen-state-1'}
    response = requests.post(f'{abe_sim_url}/to-get-kitchen', data=json.dumps(payload))
    return process_response(response)


@exception_handler
def to_fetch(target):
    payload = {'object': target, 'kitchenStateIn': None, 'setWorldState': False}
    response = requests.post(f'{abe_sim_url}/to-fetch', data=json.dumps(payload))
    return process_response(response)


@exception_handler
def to_cut(target, cutting_tool):
    payload = {'object': target, 'cuttingTool': cutting_tool, 'cutPattern': 'dice', 'kitchenStateIn': None,
               'setWorldState': False}
    response = requests.post(f'{abe_sim_url}/to-cut', data=json.dumps(payload))
    return process_response(response)


@exception_handler
def to_bake(target, oven, destination_container):
    payload = {'thingToBake': target, 'oven': oven, 'inputDestinationContainer': destination_container,
               'kitchenStateIn': None, 'setWorldState': False}
    response = requests.post(f'{abe_sim_url}/to-bake', data=json.dumps(payload))
    return process_response(response)


@exception_handler
def to_line(baking_tray, baking_paper):
    payload = {'bakingTray': baking_tray, 'bakingPaper': baking_paper, 'kitchenStateIn': None, 'setWorldState': False}
    response = requests.post(f'{abe_sim_url}/to-line', data=json.dumps(payload))
    return process_response(response)


@exception_handler
def to_mix(container, mixing_tool):
    payload = {'containerWithInputIngredients': container, 'mixingTool': mixing_tool, 'kitchenStateIn': None,
               'setWorldState': False}
    response = requests.post(f'{abe_sim_url}/to-mix', data=json.dumps(payload))
    return process_response(response)


@exception_handler
def to_sprinkle(target, topping_container):
    payload = {'object': target, 'toppingContainer': topping_container, 'kitchenStateIn': None, 'setWorldState': False}
    response = requests.post(f'{abe_sim_url}/to-sprinkle', data=json.dumps(payload))
    return process_response(response)


@exception_handler
def to_shape(container, destination):
    payload = {'containerWithDough': container, 'destination': destination, 'kitchenStateIn': None,
               'setWorldState': False}
    response = requests.post(f'{abe_sim_url}/to-shape', data=json.dumps(payload))
    return process_response(response)


@exception_handler
def to_transfer(source_container, target_container):
    payload = {'containerWithInputIngredients': source_container, 'targetContainer': target_container,
               'kitchenStateIn': None,
               'setWorldState': False}
    response = requests.post(f'{abe_sim_url}/to-transfer', data=json.dumps(payload))
    return process_response(response)
