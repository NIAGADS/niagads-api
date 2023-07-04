import re
from dateutil.parser import parse as parse_date
from datetime import datetime


def error_message(arg, badValue, allowableValues, message=None):
    if message is not None:
        return { "error": message}
    else:
        return { "error": "Invalid value (" + to_string(badValue) 
                + ") provided for: " + arg + ". Valid values are: " + to_string(allowableValues)}
        

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
        
        
def drop_nulls(obj):
    if isinstance(obj, list):
        return list(filter(None, obj))
    if isinstance(obj, dict):
        return {k: v for k, v in obj.items() if v}
        

def extract_result_data(queryResult):
    return [ extract_row_data(r) for r in queryResult ]


def to_string(value, nullVal="NULL", delim=','):
    """ checks if list, if so, converts to string; 
    None -> nullVal; 
    all other return str(value) 
    """
    if value is None:
        return nullVal
    
    if isinstance(value, list):
        return delim.join(value)
    
    return str(value)


def to_date(value, pattern='%m-%d-%Y'):
    return parse_date(value, fuzzy=True) # datetime.strptime(value, pattern).date()


def is_date(value, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.
    from https://stackoverflow.com/a/25341965
    :param value: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
   
    """
    try: 
        parse_date(value, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


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


# regex wrappers to re calls to reduce re imports
# =================================================
def regex_replace(pattern, replacement, value):
    return re.sub(pattern, replacement, value)


def regex_extract(pattern, value):
    ''' assumes one extract subset only '''
    result = re.search(pattern, value)
    if result is not None:
        return result.group(1)
    return None