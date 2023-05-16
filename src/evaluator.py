import os
import re

from model_selector import get_no_models
from utils import to_lowercase_first_character_string, to_uppercase_first_character_string

mace4_directory_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'mace4')
script_file_path = os.path.join(mace4_directory_path, 'run_mace4.py')
expression_file_path = os.path.join(mace4_directory_path, 'expression.in')
sensors_file_path = os.path.join(mace4_directory_path, 'sensors.in')
background_knowledge_file_path = os.path.join(mace4_directory_path, 'background_knowledge.in')
output_file_path = os.path.join(mace4_directory_path, 'result.out')


def prepare_expression_file(expression):
    with open(expression_file_path, 'w') as file:
        file.write('formulas(commands).\n')
        file.write(f'\t{expression}\n')
        file.write('end_of_list.')


def prepare_sensors_file(predicates):
    with open(sensors_file_path, 'w') as file:
        file.write(f'assign(domain_size, {len(predicates)}).\n\n')
        file.write('formulas(sensors).\n')
        for item in predicates:
            predicate = to_lowercase_first_character_string(item[0])
            variable = to_uppercase_first_character_string(item[1])
            file.write(f'\t{predicate}({variable}).\n')
        file.write('\t')
        for i, item in enumerate(predicates):
            variable = to_uppercase_first_character_string(item[1])
            file.write(f'{variable} = {i}. ')
        file.write('\nend_of_list.')


def evaluate_fol_expression(expression):
    prepare_expression_file(expression)

    os.system('python3 ' + script_file_path)

    no_models = get_no_models()

    return no_models


def get_predicates(content):
    predicates = set()
    predicate_pattern = r'\b([a-zA-Z]+)\('
    matches = re.findall(predicate_pattern, content)
    for match in matches:
        predicates.add(match)
    return predicates


def get_background_knowledge_predicates():
    with open(background_knowledge_file_path, 'r') as file:
        content = file.read()

    start_pattern = r'formulas\(background_knowledge\)\.'
    end_pattern = r'end_of_list\.'
    start_pos = re.search(start_pattern, content).end()
    end_pos = re.search(end_pattern, content).start()

    return get_predicates(content[start_pos:end_pos])


def preprocess_predicates(expression):
    sensor_predicates = get_background_knowledge_predicates()
    expression_predicates = get_predicates(expression)
    difference_set = expression_predicates - sensor_predicates
    if len(difference_set) == 0:
        return True
    return False


def evaluate_fol_cardinality_expression(expression):
    if expression is None:
        return -3

    if not preprocess_predicates(expression):
        return -2

    fol_expressions = re.findall(r'\|([^|]+)\|', expression)

    if len(fol_expressions) == 0:
        return evaluate_fol_expression(expression)

    for fol_expression in fol_expressions:
        nr_models = evaluate_fol_expression(fol_expression)
        expression = re.sub(r'\|{}\|'.format(re.escape(fol_expression)), str(nr_models), expression)

    try:
        return eval(expression)
    except SyntaxError:
        return -3


def main():
    print(evaluate_fol_cardinality_expression('|exists x (onion(x)).| == 2 * |exists x (largeBowl(x)).|'))
    print(evaluate_fol_cardinality_expression('all x0 (food(x0) -> onion(x0)).'))
    print(evaluate_fol_cardinality_expression('|exists x0 (food(x0) & peeledRedOnion(x0)).|'))


if __name__ == "__main__":
    main()
