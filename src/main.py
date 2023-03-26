from src.converter import generate_expression
from src.evaluator import evaluate_fol_cardinality_expression

sentences = ['There are twice as many boxes than tools', 'Most objects are boxes', 'There are two boxes']
for sentence in sentences:
    expression = generate_expression(sentence)
    print(expression)
    print(evaluate_fol_cardinality_expression(expression))
