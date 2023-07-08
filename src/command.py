import service
from evaluator import prepare_sensors_file
from logger import logger
from utils import to_lowercase_first_character_string


def filter_predicates(kitchen_state):
    predicates = []
    for item in kitchen_state.values():
        object_type = item['type']
        object_name = item['name']
        if object_type == 'Abe':
            predicates.append(('Robot', object_name))
        elif 'owl:' not in object_type and 'Particle' not in object_type:
            predicates.append((object_type, object_name))
    return predicates


def set_state(response, state_out):
    if response is None:
        return None
    if not state_out:
        kitchen_state = response['?kitchen-state-1']
    else:
        kitchen_state = response['kitchenStateOut']
    predicates = filter_predicates(kitchen_state)
    prepare_sensors_file(predicates)


def initialize_state():
    if not service.has_state:
        logger.debug(f'Setting initial kitchen state...')
        response = service.to_get_state()
        set_state(response, False)
        service.has_state = True


def fetch(parameters):
    targets = parameters[1]
    for target in targets:
        response = service.to_fetch(target)
        set_state(response, True)


def cut(parameters):
    targets = parameters[1]
    cutting_tool = parameters[2][0]
    for target in targets:
        response = service.to_cut(target, cutting_tool)
        set_state(response, True)


def bake(parameters):
    targets = parameters[1]
    oven = parameters[2][0]
    destination_counter = parameters[3][0]
    for target in targets:
        response = service.to_bake(target, oven, destination_counter)
        set_state(response, True)


def line(parameters):
    baking_trays = parameters[1]
    baking_paper = parameters[2]
    for iterator in range(len(baking_trays)):
        response = service.to_line(baking_trays[iterator], baking_paper[iterator])
        set_state(response, True)


def mix(parameters):
    targets = parameters[1]
    mixing_tool = parameters[2]
    for target in targets:
        response = service.to_mix(target, mixing_tool[0])
        set_state(response, True)


def sprinkle(parameters):
    targets = parameters[1]
    topping_container = parameters[2]
    for target in targets:
        response = service.to_sprinkle(target, topping_container[0])
        set_state(response, True)


def shape(parameters):
    containers = parameters[1]
    destination = parameters[2][0]
    for container in containers:
        response = service.to_shape(container, destination)
        set_state(response, True)


def transfer(parameters):
    source_containers = parameters[1]
    target_containers = parameters[2]
    for iterator in range(len(source_containers)):
        response = service.to_transfer(source_containers[iterator], target_containers[iterator])
        set_state(response, True)


def execute_command(predicate, parameters):
    logger.debug(f'Executing command {predicate} with parameters {parameters}...')
    parameters = [[to_lowercase_first_character_string(item) for item in sublist] for sublist in parameters]

    initialize_state()

    command_functions = {
        'fetch': fetch,
        'cut': cut,
        'bake': bake,
        'line': line,
        'mix': mix,
        'sprinkle': sprinkle,
        'shape': shape,
        'transfer': transfer
    }

    if predicate in command_functions:
        command_functions[predicate](parameters)
    else:
        logger.error(f'Invalid command: {predicate}')


def main():
    execute_command('fetch', [['Abe'], ['RedOnion1', 'RedOnion2']])
    execute_command('cut', [['Abe'], ['RedOnion1'], ['CookingKnife']])
    execute_command('line', [['Abe'], ['BakingTray1', 'BakingTray2'], ['BakingSheet1', 'BakingSheet2']])
    # execute_command('transfer', [['Abe'], ['LargeBowl2'], ['LargeBowl']])
    # execute_command('transfer', [['Abe'], ['LargeBowl2'], ['LargeBowl']])
    # execute_command('line', [['Abe'], ['BakingTray1'], ['BakingSheet1']])
    # execute_command('sprinkle', [['Abe'], ['BakingTray1'], ['SugarBag']])
    execute_command('bake', [['Abe'], ['BakingTray1'], ['Oven'], ['KitchenCounter']])
    # execute_command('mix', [['Abe'], ['LargeBowl'], ['Whisk']])
    # execute_command('shape', [['Abe'], ['LargeBowl'], ['BakingTray1']])


if __name__ == "__main__":
    main()
