"""
Custom Parameter Type: GenomeBuild 
GRCh37 or GRCh38

"""

import re
from marshmallow import fields
from werkzeug.exceptions import BadRequest

PATTERN = 'GRCh(37|38)'

class GenomeBuild(fields.Raw):
    """Field that captures the genome build
    """

    def _validate(self, value):
        """validate value and fix case
        
        Keyword arguments:
        value -- field value
        Return: throw error or valid flag
        """

        # check against regexp
        return bool(re.match(PATTERN, value))


    def _deserialize(self, value, attr, data, **kwargs):             
        value = value.lower()
        value = value.replace('grch', 'GRCh')
        if self._validate(value):
            return value
        else:
            raise BadRequest("Invalid genome build in route: '" + value + "'; Genome Build should be one of: GRCh37, GRCh38")
        
    def format(self, value):
        return value
    
    def output(self, key, obj, **kwargs):
        return getattr(obj, key)
