from evaluator import prepare_sensors_file
from service import get_kitchen_state


def command():
    response = get_kitchen_state()
    if response is None:
        return None
    kitchen_state = response['?kitchen-state-1']
    predicates = [(item['type'], item['name']) for item in kitchen_state.values()]
    prepare_sensors_file(predicates)


command()
