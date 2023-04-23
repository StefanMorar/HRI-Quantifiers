import json
import os
import re

mace4_directory_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'mace4')
script_file_path = os.path.join(mace4_directory_path, 'run-mace4.py')
expression_file_path = os.path.join(mace4_directory_path, 'expression.in')
background_knowledge_file_path = os.path.join(mace4_directory_path, 'background-knowledge.in')
output_file_path = os.path.join(mace4_directory_path, 'result.out')


def prepare_expression_file(expression):
    with open(expression_file_path, 'w') as file:
        file.write('formulas(commands).\n')
        file.write('\t{}\n'.format(expression))
        file.write('end_of_list.')


def get_no_models():
    with open(output_file_path, 'r') as file:
        contents = file.read()
        try:
            models = json.loads(contents)
        except ValueError:
            return -1
        no_models = len(models)
    return no_models


def evaluate_fol_expression(expression):
    prepare_expression_file(expression)

    os.system('python ' + script_file_path)

    no_models = get_no_models()

    os.system('rm {}'.format(output_file_path))

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
        return None

    if not preprocess_predicates(expression):
        return -2

    fol_expressions = re.findall(r'\|([^|]+)\|', expression)

    if len(fol_expressions) == 0:
        return evaluate_fol_expression(expression)

    for fol_expression in fol_expressions:
        nr_models = evaluate_fol_expression(fol_expression)
        if nr_models == -1:
            return -1
        expression = re.sub(r'\|{}\|'.format(re.escape(fol_expression)), str(nr_models), expression)

    try:
        return eval(expression)
    except SyntaxError:
        return -1


def main():
    print(evaluate_fol_cardinality_expression('|exists x (box(x)).| == 2 * |exists x (tool(x)).|'))
    print(evaluate_fol_cardinality_expression('all x0 (box(x0) -> object(x0)).'))
    print(evaluate_fol_cardinality_expression('|exists x0 (object(x0) & ball(x0)).|'))


if __name__ == "__main__":
    main()
