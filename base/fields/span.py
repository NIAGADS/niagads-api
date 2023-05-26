"""
Custom Parameter Type: Span 
chrN:start-end or N:start-end

validates chr N is 1..22, X, Y, M, or MT 
adds 'chr' if missing
substitutes MT with M
"""

import re
from marshmallow import fields, ValidationError

PATTERN = '.+:\d+-\d+' # chr:start-enddddd
VALID_CHROMOSOMES = list(range(1,22)) + [ 'X', 'Y', 'M', 'MT']

class Span(fields.Field):
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
        if cN not in VALID_CHROMOSOMES:
            raise ValueError("invalid chromosome specified: " + cN)
        
        return 'chr' + str(cN)
        

    def _validate(self, value):
        """validate value (start < end, chrN valid), formatted as expected
        
        Keyword arguments:
        value -- field value
        Return: throw error or valid flag
        """
        
        # check against regexp
        if bool(re.match(PATTERN, value)) == False:
            raise ValueError("for a chromosome, N, please specify as chrN:start-end or N:start-end")
        
        # split on :
        [chrm, span] = value.split(':')
        
        # validate chr
        chrm = self._validateChr(chrm)
        
        # validate start < end
        [start, end] = span.split('-')
        if (int(end) >= int(start)):
            raise ValueError("start must be < end")

        return chrm + ':' + span


    def _deserialize(self, value, attr, data, **kwargs):
        try:
            self._validate(value)
        except ValueError as error:
            raise ValidationError("Invalid genomic span - " + value) from error
