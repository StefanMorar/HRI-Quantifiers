from src.converter import generate_expression
from src.evaluator import evaluate_fol_cardinality_expression

sentences = ['There are twice as many boxes than tools', 'Most objects are boxes', 'There are two boxes',
             'There are exactly 2 boxes', 'There are at least 2 boxes', 'There are at most three boxes',
             'There are less than 10 boxes', 'There are more boxes than tools', 'There are less tools than boxes',
             'There are many boxes', 'There are few boxes', 'There are 2 times more boxes than tools',
             'How many boxes are there?']

for sentence in sentences:
    expression = generate_expression(sentence)
    print(expression)
    print(evaluate_fol_cardinality_expression(expression))
