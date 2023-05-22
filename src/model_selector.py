import os
import re

mace4_directory_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'mace4')
output_file_path = os.path.join(mace4_directory_path, 'result.out')

model_start_marker = '============================== MODEL ================================='
model_end_marker = '============================== end of model =========================='
number_of_models_marker = 'Exiting with'


def convert_line_to_portable_element(line):
    line = line.replace("\n", "").strip()
    word_match = r'\w+'
    arguments = re.findall(word_match, line)
    arguments = [int(arg) if arg.isdigit() else arg for arg in arguments]
    return arguments


def read_models():
    models = []
    current_model = []
    with open(output_file_path, 'r') as input_file:
        for line in input_file:
            if line.isspace():
                continue
            if model_start_marker in line:
                current_model = []
            elif model_end_marker in line:
                models.append(current_model)
            elif 'function' in line:
                current_model.append(convert_line_to_portable_element(line))
    return models


def get_number_of_models():
    no_of_models = 0
    with open(output_file_path, 'r') as file:
        for line in file:
            if number_of_models_marker in line:
                no_of_models = line.split()[2]
    if no_of_models.isdigit():
        return int(no_of_models)
    return 0


def get_constants_or_variables(functions, return_variables):
    variable_pattern = '^c\\d+$'
    dictionary = {}
    for function in functions:
        match = re.match(variable_pattern, function[1])
        if return_variables and match:
            dictionary[function[1]] = function[2]
        elif not return_variables and not match:
            dictionary[function[2]] = function[1]
    return dictionary


def get_constants(models):
    return get_constants_or_variables(models[0], False)


def get_variables(models):
    variable_dictionaries = []
    for model in models:
        variables = get_constants_or_variables(model, True)
        variable_dictionaries.append(variables)
    return variable_dictionaries


def get_variables_by_model(variable_dictionaries):
    return [list(variable_dictionary.values()) for variable_dictionary in variable_dictionaries]


def get_variables_by_key(variable_dictionaries):
    result_dictionary = {}
    for variable_dictionary in variable_dictionaries:
        for key, value in variable_dictionary.items():
            if key in result_dictionary:
                result_dictionary[key].append(value)
            else:
                result_dictionary[key] = [value]
    return [list(set(value)) for value in result_dictionary.values()]


def get_variables_as_constants_by_key():
    models = read_models()
    variables = get_variables_by_key(get_variables(models))
    constants = get_constants(models)
    return [[constants[variable] for variable in single_model_variables] for single_model_variables in variables]


def main():
    models = read_models()
    print(get_constants(models))
    print(get_variables(models))
    print(get_variables_as_constants_by_key())


if __name__ == "__main__":
    main()
