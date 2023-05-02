import re

from evaluator import prepare_sensors_file, evaluate_fol_cardinality_expression
from model_selector import choose_models
from service import get_kitchen_state, fetch_kitchen_object
from utils import to_lowercase_first_character_string


def set_state():
    response = get_kitchen_state()
    if response is None:
        return None
    kitchen_state = response['?kitchen-state-1']
    predicates = [(item['type'], item['name']) for item in kitchen_state.values()]
    prepare_sensors_file(predicates)


def generate_expression(sentence):
    match = re.match(r'Fetch an onion', sentence)
    if match:
        return 'exists y exists x (onion(x) & fetch(y, x)).'


def process_command(sentence):
    set_state()
    if evaluate_fol_cardinality_expression(generate_expression(sentence)) < 0:
        return None
    objects = choose_models(1)
    print('Fetching', objects[0][1])
    return fetch_kitchen_object(to_lowercase_first_character_string(objects[0][1]))


def main():
    print(process_command('Fetch an onion'))


if __name__ == "__main__":
    main()
