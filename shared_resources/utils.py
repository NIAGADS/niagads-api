import re

def extract_json_value(attribute, field):
    """extract value from field in a JSON attribute

    Args:
        attribute (dict): JSON/B attribute
        field (string): field name
    
    """
    
    if attribute is None:
        return None
    
    return attribute[field] if field in attribute else None


def extract_row_data(queryResultRow):
    data = queryResultRow._data
    fields = queryResultRow._fields
    # add in literals
    result = data[0]
    for index, d in enumerate(queryResultRow._data):
        if index == 0:
            continue
        result.__setattr__(fields[index], data[index])
        
    return result
        

def extract_result_data(queryResult):
    return [ extract_row_data(r) for r in queryResult ]


def is_number(value):
    return is_integer(value) or is_float(value)


def is_integer(value):
    if isinstance(value, (float, bool)):
        return False
    try:
        int(value)
        return True
    except ValueError:
        return False


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    

def is_non_numeric(value):
    if True in [char.isdigit() for char in value]:
        return False
    return True


def to_numeric(value):
    ''' convert string to appropriate numeric '''
    try:
        return int(value)
    except ValueError:
        return float(value) # raises ValueError again that will be thrown


def is_null(value, naIsNull=False):
    if value is None:
        return True
    if naIsNull and value in ['NA', 'not applicable', 'Not applicable', '.']:
        return True
    return False


def to_snake_case(key):
    ''' from https://stackoverflow.com/a/1176023 / advanced cases'''
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', key).lower()


def regex_replace(pattern, replacement, value):
    return re.sub(pattern, replacement, value)