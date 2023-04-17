import re
import string
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


def get_inner_expression(sign_predicates, variable_number):
    return ' & '.join(
        [('' if sign_predicate[1] == '+' else '-') + '{}(x{})'.format(sign_predicate[0], variable_number) for
         sign_predicate in sign_predicates])


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
            partial_inner_expression = get_inner_expression(sign_predicates, iterator)
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


def generate_all_expression(premise_predicate_tagged_tokens, conclusion_predicate_tagged_tokens,
                            conclusion_predicate_sign):
    premise_predicates = [get_predicate(t) for t in premise_predicate_tagged_tokens]
    conclusion_predicates = [get_predicate(t) for t in conclusion_predicate_tagged_tokens]
    sign_premise_predicates = list(zip(premise_predicates, ['+'] * len(premise_predicates)))
    sign_conclusion_predicates = list(zip(conclusion_predicates,
                                          [conclusion_predicate_sign] * len(conclusion_predicates)))
    premise_inner_expression = get_inner_expression(sign_premise_predicates, 0)
    conclusion_inner_expression = get_inner_expression(sign_conclusion_predicates, 0)
    return 'all x0 ({} -> {}).'.format(premise_inner_expression, conclusion_inner_expression)


def validate_noun_phrase(tagged_tokens):
    noun_phrase_pattern = r'^(\<JJ\>)?\<(NNS|NN)\>$'
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


def generate_negated_exists_expression(match):
    noun_phrase1 = nltk.pos_tag(nltk.word_tokenize(match.group(1)))
    noun_phrase2 = nltk.pos_tag(nltk.word_tokenize(match.group(2)))
    if (not validate_noun_phrase(noun_phrase1)) | (not validate_noun_phrase(noun_phrase2)):
        return None

    return '|-({}).| > 0'.format(generate_exists_expression(noun_phrase1 + noun_phrase2, [], 1)[:-1])


def generate_simple_negated_exists_expression(match):
    noun_phrase = nltk.pos_tag(nltk.word_tokenize(match.group(1)))
    if not validate_noun_phrase(noun_phrase):
        return None

    return '|-({}).| > 0'.format(generate_exists_expression(noun_phrase, [], 1)[:-1])


def generate_all_every_expression(match, conclusion_sign):
    noun_phrase1 = nltk.pos_tag(nltk.word_tokenize(match.group(1)))
    noun_phrase2 = nltk.pos_tag(nltk.word_tokenize(match.group(2)))
    if (not validate_noun_phrase(noun_phrase1)) | (not validate_noun_phrase(noun_phrase2)):
        return None

    return generate_all_expression(noun_phrase1, noun_phrase2, conclusion_sign)


def preprocess_sentence(sentence):
    lowercase_no_extra_spaces_sentence = ' '.join(sentence.lower().split())
    return ''.join(char for char in lowercase_no_extra_spaces_sentence if char not in string.punctuation)


def generate_expression(sentence):
    sentence = preprocess_sentence(sentence)

    match = re.match(r'there are (.*) as many (.*) than (.*)', sentence)
    if match:
        return generate_as_many_than_expression(match)

    match = re.match(r'there are ([a-zA-Z0-9]*) times more (.*) than (.*)', sentence)
    if match:
        return generate_times_more_than_expression(match)

    match = re.match(r'most (.*) are (.*)', sentence)
    if match:
        return generate_most_expression(match)

    match = re.match(r'there are exactly ([a-zA-Z0-9]*) (.*)', sentence)
    if match:
        return generate_numeric_expression(match, '==')

    match = re.match(r'there are at least ([a-zA-Z0-9]*) (.*)', sentence)
    if match:
        return generate_numeric_expression(match, '>=')

    match = re.match(r'there are at most ([a-zA-Z0-9]*) (.*)', sentence)
    if match:
        return generate_numeric_expression(match, '<=')

    match = re.match(r'there are more than ([a-zA-Z0-9]*) (.*)', sentence)
    if match:
        return generate_numeric_expression(match, '>')

    match = re.match(r'there are less than ([a-zA-Z0-9]*) (.*)', sentence)
    if match:
        return generate_numeric_expression(match, '>')

    match = re.match(r'there are more (.*) than (.*)', sentence)
    if match:
        return generate_more_expression(match, '>')

    match = re.match(r'there are less (.*) than (.*)', sentence)
    if match:
        return generate_more_expression(match, '<')

    match = re.match(r'there are many (.*)', sentence)
    if match:
        return generate_ambiguous_quantifier_expression(match, '>=', ambiguous_quantifiers['many'])

    match = re.match(r'there are few (.*)', sentence)
    if match:
        return generate_ambiguous_quantifier_expression(match, '>=', ambiguous_quantifiers['few'])

    match = re.match(r'there are no (.*)', sentence)
    if match:
        return generate_simple_negated_exists_expression(match)

    match = re.match(r'there are ([a-zA-Z0-9]*) (.*)', sentence)
    if match:
        return generate_numeric_expression(match, '>=')

    match = re.match(r'how many (.*) are there', sentence)
    if match:
        return generate_query_expression(match)

    match = re.match(r'no (.*) is a (.*)', sentence)
    if match:
        return generate_negated_exists_expression(match)

    match = re.match(r'all (.*) are not (.*)', sentence)
    if match:
        return generate_all_every_expression(match, '-')

    match = re.match(r'all (.*) are (.*)', sentence)
    if match:
        return generate_all_every_expression(match, '+')

    match = re.match(r'every (.*) is not(?: an? )?(.*)', sentence)
    if match:
        return generate_all_every_expression(match, '-')

    match = re.match(r'every (.*) is(?: an? )?(.*)', sentence)
    if match:
        return generate_all_every_expression(match, '+')

    return None


def main():
    print(generate_expression('All boxes are objects'))
    print(generate_expression('All boxes are not objects'))
    print(generate_expression('Every object is a box'))
    print(generate_expression('Every object is not a box'))


if __name__ == "__main__":
    main()
