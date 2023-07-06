"""
Custom Parameter Type: GenomeBuild 
GRCh37 or GRCh38
"""

import re
from marshmallow import fields, ValidationError


PATTERN = re.compile('GRCh(37|38)') # saves a little time

class GenomeBuild(fields.Raw):
    """Field that captures the genome build
    """
    
    def _deserialize(self, value, attr, data, **kwargs):             
        return self._validate(value)
    
    def _validate(self, value):
        value = value.lower().replace('grch', 'GRCh')
        match value:
            case 'hg38':
                return 'GRCh38'
            case 'hg19':
                return 'GRCh37'
            case _:
                test = re.match(PATTERN, value)
                if bool(test):
                    return test.group(0)
                else:
                    raise ValidationError("Invalid genome build (assembly): '" + value
                            + "'; assembly should be one of: GRCh37, GRCh38 or hg19, hg38")
        
        
    def format(self, value):
        return value
    
    def output(self, key, obj, **kwargs):
        value = None
        try:
            value = getattr(obj, key)
        except:
            value = getattr(obj, 'genome_build') if key == 'assembly' else getattr(obj, 'assembly')
        finally:
            if value == 'hg19':
                return 'GRCh37' 
            if value == 'hg38': 
                return 'GRCh38'
            return value
        
