''' ADVP utils '''
import requests
from shared_resources import constants


def clean_response(obj):
    ''' clean the JSON response
    locus -> string to array
    remove genomicsdb id
    '''
    
    locus = obj['locusname']
    locus = locus.replace('; ', '//')
    locus = locus.replace('"', '')
    loci = locus.split('//')
    if 'NR' in loci: loci.remove('NR')
    obj['reported_loci'] = loci
    obj['location'] = obj['Genomic coordinates']
    obj['num_publications'] = obj['num_papers']
    obj['ref_snp_id'] = obj['variantID']
    
    del obj['variantID']
    del obj['locusname']
    del obj['num_papers']
    del obj['genomicsDbID']
    del obj['Genomic coordinates']
    
    return obj


def make_request(endpoint, returnSuccess=False):
    ''' map request params and submit to FILER API'''
    
    requestUrl = constants.URLS.advp + "/" + endpoint 
    try:
        response = requests.get(requestUrl)
        response.raise_for_status()      
        if returnSuccess:
            return True       
        return response.json()
    except requests.exceptions.HTTPError as err:
        if returnSuccess:
            return False
        return {"message": "Error accessing ADVP: " + err.args[0]}

