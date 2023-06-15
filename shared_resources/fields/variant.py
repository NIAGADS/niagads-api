"""
Custom Parameter Type: Variant 
refSNP ID (rs + number) 
or chrN:pos:ref:alt or chrB:pos:ref/alt or chrN:pos:ref_alt

validates chr N is 1..22, X, Y, M, or MT 
adds 'chr' if missing
substitutes MT with M
"""

import re
from marshmallow import fields, ValidationError

RS_PATTERN = 'rs\d+' # rsN
LOCUS_PATTERN = '^.+:\d+:(A|C|G|T)+(:|_|\/)(A|C|G|T)+'
VALID_CHROMOSOMES = list(range(1,22)) + [ 'X', 'Y', 'M', 'MT']

class Variant(fields.Raw):
    """Field that captures a variant by its refSNP ID or position/
    allelic identifier
    where chr may be a single alphanumeric N or 'chr'+N
    where N = 1..22, X,Y,M,or MT
    """

    def _validateChrm(self, chrm):
        """ validate the chromosome
             
        Keyword arguments:
        chrm -- chromosome (left of ':' in value)
        Return: N if valid
        """
        cN = chrm.replace('chr', '') if 'chr' in chrm else chrm
        if cN == 'MT':
            cN = 'M'
        if cN not in VALID_CHROMOSOMES:
            raise ValueError("invalid chromosome specified: " + cN)
        
        return str(cN)
        

    def _validate(self, value):
        """validate value (start < end, chrN valid), formatted as expected
        
        Keyword arguments:
        value -- field value
        Return: throw error or valid flag
        """
        
        # check against regexp
        if value.lower().startsWith('rs') and bool(re.match(RS_PATTERN, value)) == False:
            raise ValueError("variant identifier starts with 'rs' but is invalid refSNP identifier")
        
        if bool(re.match(LOCUS_PATTERN, value)) == False:
            raise ValueError("unexpected characters")
        
        # replace _ or / with :
        value = value.replace('_', ':').replace('/', ':')
        
        # split on :
        [chrm, pos, ref, alt] = value.split(':')
        
        # validate chr
        chrm = self._validateChr(chrm)
        
        return ':'.join(chrm, pos, ref, alt)
    

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            self._validate(value)
        except ValueError as error:
            raise ValidationError("Invalid variant - " + value) from error
