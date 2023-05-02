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
            return None
    return models


def get_no_models():
    models = read_models()
    if models is None:
        return -1
    return len(models)


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


def get_constants(models):
    return get_constants_or_variables(models[0][2], False)


def get_variables(models):
    variable_dictionaries = []
    for model in models:
        variables = get_constants_or_variables(model[2], True)
        variable_dictionaries.append(variables)
    return variable_dictionaries


def get_variables_by_model(variable_dictionaries):
    return [list(variable_dictionary.values()) for variable_dictionary in variable_dictionaries]


def get_predicates(models):
    functions_and_relations = models[0][2]
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


def get_variables_by_key(variable_dictionaries):
    result_dictionary = {}
    for variable_dictionary in variable_dictionaries:
        for key, value in variable_dictionary.items():
            if key in result_dictionary:
                result_dictionary[key].append(value)
            else:
                result_dictionary[key] = [value]
    return [list(value) for value in result_dictionary.values()]


def choose_models(nr_models):
    models = read_models()
    if nr_models > len(models):
        return None
    variables = get_variables_by_model(get_variables(models))
    # TODO: choose models based on some rules instead of always returning the first ones
    constants = get_constants(models)
    return [[constants[variable] for variable in single_model_variables] for single_model_variables in
            variables[:nr_models]]


def main():
    # models = read_models()
    # predicates = get_predicates(models)
    # print(predicates)
    # print(get_constants(models))
    # variables = get_variables(models)
    # print(variables)
    # print(get_variables_by_model(variables))
    # print(get_variables_by_key(variables))
    # print(get_predicates_by_constant(predicates, 5))
    # print(get_predicates_by_constant(predicates, 6))
    print(choose_models(2))


if __name__ == "__main__":
    main()
