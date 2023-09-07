
from flask.json import jsonify
from shared_resources.fields import Span, GenomeBuild
from niagads.utils import string_utils, array_utils


def error_message(message=None, errorType="error"):
    if errorType == 'bad_arg':
            return { "error": "Invalid value (" + array_utils.list_to_string(message['bad_value']) 
                + ") provided for: " + message['arg'] + ". Valid values are: " 
                + array_utils.list_to_string(message['valid_values'])}
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

        
def extract_row_data(queryResultRow, tableValued, hasLiterals):
    data = []
    fields = []
    try:
        data = getattr(queryResultRow, '_data')
        fields = getattr(queryResultRow, '_fields')

        if tableValued:
            return dict(zip(fields, data))
        
        # add in literals  
        result = data[0] if hasLiterals else {}
        for index, d in enumerate(data):
            if index == 0 and hasLiterals:
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


def extract_result_data(queryResult, tableValued=False, hasLiterals=False):
    return [ extract_row_data(r, tableValued, hasLiterals) for r in queryResult ]


def remove_extra_variant_annotations(result, keepFullAnnotation):
    if result['mapping'] is not None and not keepFullAnnotation:
        mapping = result['mapping']['annotation']
        del mapping['ADSP_QC']
        del mapping['ranked_consequences']
        del mapping['mapped_coordinates']
    result['mapping']['queried_variant'] = result['lookup_variant_id']
    return result['mapping']
    
    
def extract_variant_result_data(queryResult, fullAnnotation=False):
    tableValued = True
    hasLiterals = False
    return [ remove_extra_variant_annotations(extract_row_data(r, tableValued, hasLiterals), fullAnnotation) for r in queryResult ]
