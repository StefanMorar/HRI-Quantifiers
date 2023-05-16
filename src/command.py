from evaluator import prepare_sensors_file
from service import to_get_state, to_fetch, to_cut
from utils import to_lowercase_first_character_string


def set_state():
    response = to_get_state()
    if response is None:
        return None
    kitchen_state = response['?kitchen-state-1']
    predicates = [(item['type'], item['name']) for item in kitchen_state.values()]
    prepare_sensors_file(predicates)


def fetch(parameters):
    set_state()
    for kitchen_object in parameters[1]:
        to_fetch(kitchen_object)


def cut(parameters):
    set_state()
    for kitchen_object in parameters[1]:
        to_cut(kitchen_object, parameters[2])


def bake(parameters):
    set_state()
    print('TODO')


def line(parameters):
    set_state()
    print('TODO')


def mix(parameters):
    set_state()
    print('TODO')


def transfer(parameters):
    set_state()
    print('TODO')


def sprinkle(parameters):
    set_state()
    print('TODO')


def shape(parameters):
    set_state()
    print('TODO')


def execute_command(predicate, parameters):
    print(f'Executing command is {predicate} with parameters {parameters}')
    parameters = [to_lowercase_first_character_string(parameter) for parameter in parameters]
    if predicate == 'fetch':
        fetch(parameters)
    elif predicate == 'cut':
        cut(parameters)


def main():
    print(execute_command('fetch', ['Abe', ['RedOnion1', 'RedOnion2']]))


if __name__ == "__main__":
    main()
