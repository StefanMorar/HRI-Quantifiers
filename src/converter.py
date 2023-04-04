import re
from itertools import combinations

import inflect
import nltk
from word2number import w2n

ambiguous_quantifiers = {
    'many': 10,
    'some': 2,
    'few': 2
}


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


def generate_exists_expression(positive_predicate_tagged_tokens, negative_predicate_tagged_tokens, no_variables):
    signs = ['+'] * len(positive_predicate_tagged_tokens) + ['-'] * len(negative_predicate_tagged_tokens)
    predicates = [get_predicate(t) for t in positive_predicate_tagged_tokens + negative_predicate_tagged_tokens]

    sign_predicates = list(zip(predicates, signs))
    no_predicates = len(sign_predicates) * no_variables
    if no_predicates == 0:
        return ''
    else:
        inner_expression = ''
        for iterator in range(no_variables):
            partial_inner_expression = ' & '.join(
                [('' if sign_predicate[1] == '+' else '-') + '{}(x{})'.format(sign_predicate[0], iterator) for
                 sign_predicate in sign_predicates])
            if iterator == 0:
                inner_expression = partial_inner_expression
            else:
                inner_expression = ' & '.join([inner_expression, partial_inner_expression])

        variables = ['x{}'.format(current_variable) for current_variable in range(no_variables)]
        if no_variables > 1:
            variable_combinations = list(combinations(variables, 2))
            c = ' & '.join(
                '{} != {}'.format(variable_combination[0], variable_combination[1]) for variable_combination in
                variable_combinations)
            inner_expression = '{} & {}'.format(inner_expression, c)

        outer_expression = 'exists ' + ' exists '.join(variables)
        return '{} ({}).'.format(outer_expression, inner_expression)


def validate_noun_phrase(tagged_tokens):
    noun_phrase_pattern = r'^(\<JJ\>)?\<NNS\>$'
    return True if re.match(noun_phrase_pattern, get_tag_string(tagged_tokens)) else False


def validate_quantifier(tagged_tokens):
    quantifier_pattern = r'^\<CD\>$'
    return True if re.match(quantifier_pattern, get_tag_string(tagged_tokens)) else False


def get_numeric_digits(word):
    match = re.match(r'^[0-9]*$', word)
    if match:
        return int(word)
    return w2n.word_to_num(word)


def generate_integer_quantifier(tagged_tokens):
    if tagged_tokens[0][0] == 'twice':
        return 2
    if tagged_tokens[0][0] == 'thrice':
        return 3


def generate_as_many_than_expression(match):
    quantifier = nltk.pos_tag(nltk.word_tokenize(match.group(1)))
    noun_phrase1 = nltk.pos_tag(nltk.word_tokenize(match.group(2)))
    noun_phrase2 = nltk.pos_tag(nltk.word_tokenize(match.group(3)))
    if (not validate_noun_phrase(noun_phrase1)) | (not validate_noun_phrase(noun_phrase2)):
        return None

    return '|{}| == {} * |{}|'.format(generate_exists_expression(noun_phrase1, [], 1),
                                      generate_integer_quantifier(quantifier),
                                      generate_exists_expression(noun_phrase2, [], 1))


def generate_times_more_than_expression(match):
    quantifier = nltk.pos_tag(nltk.word_tokenize(match.group(1)))
    noun_phrase1 = nltk.pos_tag(nltk.word_tokenize(match.group(2)))
    noun_phrase2 = nltk.pos_tag(nltk.word_tokenize(match.group(3)))
    if (not validate_quantifier(quantifier)) | (not validate_noun_phrase(noun_phrase1)) | (
            not validate_noun_phrase(noun_phrase2)):
        return None

    return '|{}| == {} * |{}|'.format(generate_exists_expression(noun_phrase1, [], 1),
                                      get_numeric_digits(quantifier[0][0]),
                                      generate_exists_expression(noun_phrase2, [], 1))


def generate_most_expression(match):
    noun_phrase1 = nltk.pos_tag(nltk.word_tokenize(match.group(1)))
    noun_phrase2 = nltk.pos_tag(nltk.word_tokenize(match.group(2)))
    if (not validate_noun_phrase(noun_phrase1)) | (not validate_noun_phrase(noun_phrase2)):
        return None
    return '|{}| > |{}|'.format(generate_exists_expression(noun_phrase1 + noun_phrase2, [], 1),
                                generate_exists_expression(noun_phrase1, noun_phrase2, 1))


def generate_numeric_expression(match, operator):
    quantifier = nltk.pos_tag(nltk.word_tokenize(match.group(1)))
    noun_phrase = nltk.pos_tag(nltk.word_tokenize(match.group(2)))
    if (not validate_quantifier(quantifier)) | (not validate_noun_phrase(noun_phrase)):
        return None
    return '|{}| {} {}'.format(generate_exists_expression(noun_phrase, [], 1), operator,
                               get_numeric_digits(quantifier[0][0]))


def generate_query_expression(match):
    noun_phrase = nltk.pos_tag(nltk.word_tokenize(match.group(1)))
    if not validate_noun_phrase(noun_phrase):
        return None
    return '|{}|'.format(generate_exists_expression(noun_phrase, [], 1))


def generate_ambiguous_quantifier_expression(match, operator, quantifier):
    noun_phrase = nltk.pos_tag(nltk.word_tokenize(match.group(1)))
    if not validate_noun_phrase(noun_phrase):
        return None
    return '|{}| {} {}'.format(generate_exists_expression(noun_phrase, [], 1), operator, quantifier)


def generate_more_expression(match, operator):
    noun_phrase1 = nltk.pos_tag(nltk.word_tokenize(match.group(1)))
    noun_phrase2 = nltk.pos_tag(nltk.word_tokenize(match.group(2)))
    if (not validate_noun_phrase(noun_phrase1)) | (not validate_noun_phrase(noun_phrase2)):
        return None
    return '|{}| {} |{}|'.format(generate_exists_expression(noun_phrase1, [], 1), operator,
                                 generate_exists_expression(noun_phrase2, [], 1))


def generate_expression(sentence):
    match = re.match(r'There are (.*) as many (.*) than (.*)', sentence)
    if match:
        return generate_as_many_than_expression(match)

    match = re.match(r'There are ([a-zA-Z0-9]*) times more (.*) than (.*)', sentence)
    if match:
        return generate_times_more_than_expression(match)

    match = re.match(r'Most (.*) are (.*)', sentence)
    if match:
        return generate_most_expression(match)

    match = re.match(r'There are exactly ([a-zA-Z0-9]*) (.*)', sentence)
    if match:
        return generate_numeric_expression(match, '==')

    match = re.match(r'There are at least ([a-zA-Z0-9]*) (.*)', sentence)
    if match:
        return generate_numeric_expression(match, '>=')

    match = re.match(r'There are at most ([a-zA-Z0-9]*) (.*)', sentence)
    if match:
        return generate_numeric_expression(match, '<=')

    match = re.match(r'There are more than ([a-zA-Z0-9]*) (.*)', sentence)
    if match:
        return generate_numeric_expression(match, '>')

    match = re.match(r'There are less than ([a-zA-Z0-9]*) (.*)', sentence)
    if match:
        return generate_numeric_expression(match, '>')

    match = re.match(r'There are more (.*) than (.*)', sentence)
    if match:
        return generate_more_expression(match, '>')

    match = re.match(r'There are less (.*) than (.*)', sentence)
    if match:
        return generate_more_expression(match, '<')

    match = re.match(r'There are many (.*)', sentence)
    if match:
        return generate_ambiguous_quantifier_expression(match, '>=', ambiguous_quantifiers['many'])

    match = re.match(r'There are few (.*)', sentence)
    if match:
        return generate_ambiguous_quantifier_expression(match, '>=', ambiguous_quantifiers['few'])

    match = re.match(r'There are ([a-zA-Z0-9]*) (.*)', sentence)
    if match:
        return generate_numeric_expression(match, '>=')

    match = re.match(r'How many (.*) are there?', sentence)
    if match:
        return generate_query_expression(match)

    return None
