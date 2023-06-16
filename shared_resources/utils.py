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

