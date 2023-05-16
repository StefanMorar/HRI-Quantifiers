import json
import os
import re

import openai
from dotenv import load_dotenv

from command import execute_command
from evaluator import evaluate_fol_cardinality_expression, evaluate_fol_expression
from model_selector import get_variables_as_constants_by_key

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
model = os.getenv('OPENAI_FINE_TUNED_MODEL')
max_tokens = int(os.getenv('OPENAI_FINE_TUNED_MAX_TOKENS'))


def generate_completion(sentence):
    res = openai.Completion.create(model=model, prompt=sentence + ' ->', stop=']}', max_tokens=max_tokens)
    # print(res.choices[0].text + ']}')
    # return res.choices[0].text + ']}'
    # hardcoded conversion to reduce usage costs
    return "{'type':'command','expressions':[['|exists x1 (onion(x1)).| >= 2']],'commands':['abe(x0) & onion(x1) -> fetch(x0, x1).']}"


def create_variable_restrictions_dictionary(expressions):
    dictionary = {}
    for expression in expressions:
        variable_match = re.search(r'exists\s(\w+)', expression)
        if not variable_match:
            return None

        quantifier_match = re.search(r'\d+$', expression)
        if quantifier_match:
            digits = quantifier_match.group()
            dictionary[variable_match.group(1)] = int(digits)
        else:
            dictionary[variable_match.group(1)] = 'INF'
    return dictionary


def get_command_predicate(command_conclusion):
    command_conclusion = command_conclusion.replace(' ', '')
    predicate_pattern = r'\b([a-zA-Z]+)\('
    predicate_matches = re.findall(predicate_pattern, command_conclusion)
    return predicate_matches[0]


def get_command_predicate_arguments(command_conclusion):
    arguments_pattern = r'\((.*?)\)'
    arguments_match = re.search(arguments_pattern, command_conclusion)
    return arguments_match.group(1).split(',')


def get_command_variables(predicate_arguments):
    return [item for item in predicate_arguments if item[0].islower()]


def create_exists_expression(command_premise, command_conclusion):
    arguments = get_command_predicate_arguments(command_conclusion.replace(' ', ''))
    variables = get_command_variables(arguments)
    outer_expression = ' '.join(['exists ' + variable for variable in variables])
    inner_expression = '&'.join([command_premise, command_conclusion])
    return f'{outer_expression} ({inner_expression}).', arguments


def preprocess_command(command):
    command_premise, command_conclusion = command.split('->')
    expression, arguments = create_exists_expression(command_premise, command_conclusion[:-1])
    return get_command_predicate(command_conclusion), expression, arguments


def create_variable_values_dictionary(variables):
    variable_values = get_variables_as_constants_by_key()
    if len(variables) != len(variable_values):
        return None
    dictionary = {}
    for iterator in range(len(variables)):
        dictionary[variables[iterator]] = variable_values[iterator]
    return dictionary


def get_command_parameters(predicate_arguments, variable_values_dictionary, variable_restrictions_dictionary):
    command_parameters = []
    for predicate_argument in predicate_arguments:
        if predicate_argument[0].isupper():
            command_parameters.append([predicate_argument])
        elif predicate_argument in variable_restrictions_dictionary:
            nr_models = variable_restrictions_dictionary[predicate_argument]
            if nr_models == 'INF':
                command_parameters.append(variable_values_dictionary[predicate_argument])
            elif nr_models > len(variable_values_dictionary[predicate_argument]):
                return None
            else:
                command_parameters.append(variable_values_dictionary[predicate_argument][:nr_models])
        else:
            command_parameters.append(variable_values_dictionary[predicate_argument][0])
    return command_parameters


def process_command(expressions, command):
    predicate, expression, predicate_arguments = preprocess_command(command)
    print(expression)

    if evaluate_fol_expression(expression) < 1:
        return None

    variables = get_command_variables(predicate_arguments)

    restrictions_dictionary = create_variable_restrictions_dictionary(expressions)
    print(restrictions_dictionary)

    values_dictionary = create_variable_values_dictionary(variables)
    print(values_dictionary)

    command_parameters = get_command_parameters(predicate_arguments, values_dictionary, restrictions_dictionary)
    print(command_parameters)

    execute_command(predicate, command_parameters)


def process_commands(expressions, commands):
    if len(expressions) != len(commands):
        return None
    for iterator in range(len(commands)):
        process_command(expressions[iterator], commands[iterator])


def process_queries(expressions):
    results = []
    for expression in expressions:
        evaluation = evaluate_fol_cardinality_expression(expression)
        if evaluation == -3:
            results.append('Syntax error while processing the query')
        elif evaluation == -2:
            results.append('Query contains unknown predicates')
        else:
            results.append(evaluation)
    return results


def process_completion(completion):
    completion = completion.replace("'", "\"")
    json_completion = json.loads(completion)
    if json_completion['type'] == 'query':
        process_queries(json_completion['expressions'])
    elif json_completion['type'] == 'command':
        process_commands(json_completion['expressions'], json_completion['commands'])
    return None


def main():
    process_completion(generate_completion('Fetch 2 onions'))


if __name__ == "__main__":
    main()
