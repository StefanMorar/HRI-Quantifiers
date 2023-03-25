import re

import inflect
import nltk

from src.evaluator import evaluate_fol_cardinality_expression


def get_predicate(tagged_token):
    match tagged_token[1]:
        case 'NN':
            return tagged_token[0]
        case 'JJ':
            return tagged_token[0]
        case 'NNS':
            p = inflect.engine()
            return p.singular_noun(tagged_token[0])


def get_tag_string(tagged_tokens):
    return ''.join('<{}>'.format(tagged_token[1]) for tagged_token in tagged_tokens)


def generate_exists_expression(tagged_tokens):
    predicates = [get_predicate(t) for t in tagged_tokens]
    no_predicates = len(predicates)
    if no_predicates == 0:
        return ''
    elif no_predicates == 1:
        return 'exists x ({}(x)).'.format(predicates[0])
    else:
        inner_expression = '{}(x) '.format(predicates[0]) + ' '.join(
            ['& {}(x)'.format(predicate) for predicate in predicates[1:]])
        return 'exists x ({}).'.format(inner_expression)


def validate_noun_phrase(tagged_tokens):
    noun_phrase_pattern = r'^(\<JJ\>)?\<NNS\>$'
    return True if re.match(noun_phrase_pattern, get_tag_string(tagged_tokens)) else False


def generate_integer_quantifier(tagged_tokens):
    if tagged_tokens[0][0] == 'twice':
        return 2
    if tagged_tokens[0][0] == 'thrice':
        return 3


def generate_predicate_comparison_expression(sentence):
    regex_pattern = r'There are (.*) as many (.*) than (.*)'
    match = re.match(regex_pattern, sentence)
    if match:
        quantifier = nltk.pos_tag(nltk.word_tokenize(match.group(1)))
        noun_phrase1 = nltk.pos_tag(nltk.word_tokenize(match.group(2)))
        print(noun_phrase1)
        noun_phrase2 = nltk.pos_tag(nltk.word_tokenize(match.group(3)))
        if (not validate_noun_phrase(noun_phrase1)) | (not validate_noun_phrase(noun_phrase2)):
            return None

        return '|{}| == {} * |{}|'.format(generate_exists_expression(noun_phrase1),
                                          generate_integer_quantifier(quantifier),
                                          generate_exists_expression(noun_phrase2))
    else:
        return None


expression = generate_predicate_comparison_expression('There are twice as many boxes than tools')
print(expression)
print(evaluate_fol_cardinality_expression(expression))
