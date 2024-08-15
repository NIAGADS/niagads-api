from enum import Enum
from fastapi import Query
from niagads.reference.chromosomes import Human as Chromosome
from niagads.utils.reg_ex import matches
from .param_validation import clean

class Assembly(str, Enum):
    """enum for genome builds"""
    GRCh37 = "GRCh37"
    GRCh38 = "GRCh38"
    hg19 = "hg19"
    hg38 = "hg38"
        
    @classmethod
    def validate(self, value):
        for e in self:
            if e.value.lower() == value.lower(): # for GRCh37/38 -> value match
                return "GRCh37" if value.lower() == 'hg19' else "GRCh38" if value.lower() == 'hg38' else e.value
    
        raise ValueError("Invalid `assembly`: " + value)

async def assembly_param(assembly: Assembly = Query(Assembly.GRCh38, description="reference genome build (assembly)")): 
    return Assembly.validate(clean(assembly))


async def chromosome_param(chromosome: str = Query(Chromosome.chr19.value, enum=[c.name for c in Chromosome],
        description="chromosome, specificed as 1..22,X,Y,M,MT or chr1...chr22,chrX,chrY,chrM,chrMT")):
        return Chromosome.validate(clean(chromosome))

async def span_param(span: str = Query(alias="loc", description="genomic region to query; for a chromosome, N, please specify as chrN:start-end or N:start-end", examples=["chr19:10000-40000", "19:10000-40000"])):
    pattern ='.+:\d+-\d+' # chr:start-enddddd
    span = clean(span)
    
    # check against regexp
    if matches(pattern, span) == False:
        raise ValueError(f'Invalid genomic span: `{span}`; for a chromosome, N, please specify as chrN:start-end or N:start-end')

    # split on :
    [chrm, coords] = span.split(':')
    validChrm = Chromosome.validate(chrm)
    if validChrm is None:
        raise ValueError(f'Invalid genomic span: `{span}`; invalid chromosome `{chrm}`')

    # validate start < end
    [start, end] = coords.split('-')
    if (int(start) > int(end)):
        raise ValueError(f'Invalid genomic span: `{span}`; start coordinate must be <= end')
    
    return validChrm + ':' + coords




