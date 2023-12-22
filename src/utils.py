def to_lowercase_first_character_string(item):
    return item[0].lower() + item[1:]


def to_uppercase_first_character_string(item):
    return item[0].upper() + item[1:]


def string_to_bool(string):
    if string.lower() in ['true', 'yes', '1']:
        return True
    elif string.lower() in ['false', 'no', '0']:
        return False
    else:
        raise ValueError("Invalid boolean string")
