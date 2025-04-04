import nh3 # XSS protection
# TODO: investigate nh3 and alternatives to set cleaning options more accurately
from niagads.utils.string import is_camel_case

def id2title(columnId: str):
    
    if columnId == 'url':
        return 'File Download'

    if columnId == 'p_value':
        return 'p-Value'
    
    if columnId == 'chrom': # bed file
        return 'chrom'
    if is_camel_case(columnId): # bed file
        return columnId
    
    if columnId == 'biosample_term':
        return 'Biosample'
    
    title = columnId.title().replace('_', ' ')
    title = title.replace('Id', 'ID').replace('Of', 'of').replace('Md5Sum', 'md5sum')
    title = title.replace('Url', 'URL').replace('Bp ', 'BP ')
    if title.startswith('Is '):
        title = title + '?'
    
    return title

def clean(value: str):
    if value is None:
        return value
    return nh3.clean_text(value.strip())

def print_enum_values(enumClass):
    return ','.join([f'`{m.value}`' for m in enumClass])