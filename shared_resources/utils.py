def extract_json_value(attribute, field):
    """extract value from field in a JSON attribute

    Args:
        attribute (dict): JSON/B attribute
        field (string): field name
    
    """
    
    if attribute is None:
        return None
    
    return attribute[field] if field in attribute else None

def extract_result_data(queryResult):
    return  [ r._data[0] for r in queryResult ]

