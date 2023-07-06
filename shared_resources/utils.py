import re
from flask.json import jsonify
from dateutil.parser import parse as parse_date
from datetime import datetime

from shared_resources.fields import Span, GenomeBuild



def error_message(message=None, errorType="error"):
    if errorType == 'bad_arg':
            return { "error": "Invalid value (" + to_string(message['bad_value']) 
                + ") provided for: " + message['arg'] + ". Valid values are: " + to_string(message['valid_values'])}
   
    return { errorType: message}

    

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
    data = []
    fields = []
    try:
        data = getattr(queryResultRow, '_data')
        fields = getattr(queryResultRow, '_fields')
        # add in literals  
        result = data[0]
        for index, d in enumerate(data):
            if index == 0:
                continue
            if fields[index].startswith('_'):
                continue
            result.__setattr__(fields[index], d)
        return result
    except:
        return queryResultRow        
    
    
def validate_assembly(assembly):
    """ validate assembly / genome build"""
    return GenomeBuild().deserialize(assembly)
        

def validate_span(args):
    """ parse span out of request args & validate """

    if args.span:
        return Span().deserialize(args.span)
    else:
        if args.chr is None or args.start is None or args.end is None:
            return error_message("if not specifying 'span' as 'chrN:start-end', must supply 'chr', 'start', and 'end' parameters",
                    errorType='missing_required_parameter')
        span = str(args.chr) + ':' + str(args.start) + '-' + str(args.end)
        return Span()._validate(span)

    
def drop_nulls(obj):
    if isinstance(obj, list):
        return list(filter(None, obj))
    if isinstance(obj, dict):
        return {k: v for k, v in obj.items() if v}
        

def dict_to_string(obj):
    """ translate dict to attr=value; list"""
    pairs = [ k + "=" + str(v) for k,v in obj.items()]
    return ';'.join(pairs)

def extract_result_data(queryResult):
    return [ extract_row_data(r) for r in queryResult ]


def remove_duplicates(array):
    """ remove duplicates from a list by transforming to set and back """
    return [*set(array)]


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

def is_searchable_string(key, value, skipFieldsWith):
        if array_in_string(key, skipFieldsWith):
            return False
        
        if value is None:
            return False
        
        if is_bool(value):
            return False
        
        if is_number(value):
            return False
        
        return True
    

def array_in_string(value, array):
    """ check if any element in the array is the string """
    for elem in array:
        if elem in value:
            return True
    return False


def to_date(value, pattern='%m-%d-%Y'):
    return parse_date(value, fuzzy=True) # datetime.strptime(value, pattern).date()

def to_bool(val):
    """Convert a string representation of truth to true (1) or false (0).
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    modified from https://stackoverflow.com/a/18472142
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true',  '1'):
        return 1
    elif val in ('n', 'no', 'f', 'false', '0'):
        return 0
    else:
        raise ValueError("Invalid boolean value %r" % (val,))
    
    
def is_bool(value):
    if isinstance(value, bool):
        return True
    
    try:
        to_bool(value)
        return True
    except:
        return False
    

def is_date(value, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.
    from https://stackoverflow.com/a/25341965
    :param value: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
   
    """
    if isinstance(value, datetime):
        return True
    
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