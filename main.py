import json
import os

from src.converter import generate_expression
from src.evaluator import evaluate_fol_cardinality_expression

directory_path = os.path.dirname(os.path.realpath(__file__))
queries_input_file_path = os.path.join(directory_path, 'input/queries.in')
commands_input_file_path = os.path.join(directory_path, 'input/commands.in')
queries_output_file_path = os.path.join(directory_path, 'output/queries.out')
commands_output_file_path = os.path.join(directory_path, 'output/commands.out')

count = 0
with open(queries_input_file_path, 'r') as input_file, open(queries_output_file_path, 'w') as output_file:
    for sentence in input_file:
        expression = generate_expression(sentence)
        evaluation = evaluate_fol_cardinality_expression(expression)
        data = {'expression': expression, 'evaluation': evaluation}
        output_file.write(json.dumps(data) + '\n')
        count += 1
print('Processed {} queries. Output saved to output/queries.out'.format(count))
