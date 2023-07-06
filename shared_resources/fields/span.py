"""
Custom Parameter Type: Span 
chrN:start-end or N:start-end

validates chr N is 1..22, X, Y, M, or MT 
adds 'chr' if missing
substitutes MT with M
"""

import re
from marshmallow import fields, ValidationError
from shared_resources.constants import CHROMOSOMES

PATTERN = '.+:\d+-\d+' # chr:start-enddddd


class Span(fields.Raw):
    """Field that captures a span as chr:start-end,
    where chr may be a single alphanumeric N or 'chr'+N
    where N = 1..22, X,Y,M,or MT
    additional validation checks start < end
    """

    def _validateChrm(self, chrm):
        """ validate the chromosome
             
        Keyword arguments:
        chrm -- chromosome (left of ':' in value)
        Return: 'chr' + N if valid
        """
        cN = chrm.replace('chr', '') if 'chr' in chrm else chrm
        if cN == 'MT':
            cN = 'M'
        if cN not in CHROMOSOMES:
            raise ValidationError("Invalid genomic span: invalid chromosome specified: " + cN)
        
        return 'chr' + str(cN)
        

    def _validate(self, value):
        """validate value (start < end, chrN valid), formatted as expected
        
        Keyword arguments:
        value -- field value
        Return: throw error or valid flag
        """
        
        # check against regexp
        if bool(re.match(PATTERN, value)) == False:
            raise ValidationError("Invalid genomic span: " + value + "- for a chromosome, N, please specify as chrN:start-end or N:start-end")
        
        # split on :
        [chrm, span] = value.split(':')
        
        # validate chr
        chrm = self._validateChrm(chrm)
        
        # validate start < end
        [start, end] = span.split('-')
        if (int(start) > int(end)):
            raise ValidationError("Invalid genomic span: " + value + " - start must be <= end")

        return chrm + ':' + span


    def _deserialize(self, value, attr, data, **kwargs):
        return self._validate(value)
 


