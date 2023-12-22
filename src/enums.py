from enum import Enum


class ExpressionType(Enum):
    query = 'query'
    command = 'command'


class EvaluationType(Enum):
    with_models = 'with_models'
    without_models = 'without_models'
