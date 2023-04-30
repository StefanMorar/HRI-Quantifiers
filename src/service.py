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


def get_kitchen_state():
    payload = {'kitchenStateIn': '?kitchen-state-1'}
    response = requests.post(f'{abe_sim_url}/to-get-kitchen', data=json.dumps(payload))
    return process_response(response)
