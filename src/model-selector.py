import json
import os
import re

mace4_directory_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'mace4')
output_file_path = os.path.join(mace4_directory_path, 'result.out')


def read_models():
    with open(output_file_path, 'r') as file:
        contents = file.read()
        try:
            models = json.loads(contents)
        except ValueError:
            return -1
    return models


def get_constants_or_variables(functions_and_relations, return_variables):
    functions = [element for element in functions_and_relations if element[0] == 'function']
    variable_pattern = '^c\\d+$'
    dictionary = {}
    for function in functions:
        match = re.match(variable_pattern, function[1])
        if return_variables and match:
            dictionary[function[1]] = function[3]
        elif not return_variables and not match:
            dictionary[function[3]] = function[1]
    return dictionary


def get_constants(functions_and_relations):
    return get_constants_or_variables(functions_and_relations, False)


def get_variables(functions_and_relations):
    return get_constants_or_variables(functions_and_relations, True)


def get_predicates(functions_and_relations):
    relations = [element for element in functions_and_relations if element[0] == 'relation']
    predicates = ()
    for relation in relations:
        predicates = predicates + ((relation[1], relation[3]),)
    return predicates


def get_predicates_by_constant(predicates, constant):
    true_predicates = []
    for predicate in predicates:
        if predicate[1][constant] == 1:
            true_predicates.append(predicate[0])
    return true_predicates


def get_processed_variables(variable_dictionaries):
    result_dictionary = {}
    for variable_dictionary in variable_dictionaries:
        for key, value in variable_dictionary.items():
            if key in result_dictionary:
                result_dictionary[key].append(value)
            else:
                result_dictionary[key] = [value]
    return result_dictionary


def process_models():
    models = read_models()
    predicates = get_predicates(models[0][2])
    constants = get_constants(models[0][2])
    print(constants)
    print(predicates)
    variable_dictionaries = []
    for model in models:
        variables = get_variables(model[2])
        variable_dictionaries.append(variables)
    print(get_processed_variables(variable_dictionaries))
    print(get_predicates_by_constant(predicates, 4))


process_models()
