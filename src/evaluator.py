import os
import re

sensors_file_name = '../mace4/sensors.in'
background_knowledge_file_name = '../mace4/background_knowledge.in'
expression_file_name = '../mace4/expression.in'
output_file_name = '../mace4/result.out'


def prepare_expression_file(expression):
    with open(expression_file_name, 'w') as file:
        file.write('formulas(commands).\n')
        file.write('\t{}\n'.format(expression))
        file.write('end_of_list.')
    file.close()


def get_no_models():
    no_models = -1
    with open(output_file_name, 'r') as file:
        for line in file:
            if 'Exiting with' in line:
                no_models = line.split()[2]
    file.close()
    return no_models


def evaluate_fol_expression(expression):
    prepare_expression_file(expression)

    os.system('mace4 -f {} {} {} > {}'.format(sensors_file_name, background_knowledge_file_name, expression_file_name,
                                              output_file_name))
    no_models = get_no_models()

    os.system('rm {}'.format(output_file_name))

    return no_models


def evaluate_fol_cardinality_expression(expression):
    fol_expressions = re.findall(r'\|([^|]+)\|', expression)

    for fol_expression in fol_expressions:
        nr_models = evaluate_fol_expression(fol_expression)
        expression = re.sub(r'\|{}\|'.format(re.escape(fol_expression)), str(nr_models), expression)

    try:
        return eval(expression)
    except SyntaxError:
        return -1


print(evaluate_fol_cardinality_expression('|exists x (box(x)).| == 2 * |exists y (tool(y)).|'))
