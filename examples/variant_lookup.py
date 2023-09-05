# looks up a list of variants provided in a file
# returns as JSON or tab-delimited text
# output is to STDOUT

import requests
import argparse
import json
from types import SimpleNamespace
from sys import stderr, stdout, exit
from urllib.parse import urlencode
from multiprocessing import Pool

REQUEST_URI = "https://api.niagads.org"

def pretty_print(obj):
    ''' pretty print a dict obj'''
    if isinstance(obj, dict):
        print(json.dumps(obj, sort_keys=True, indent=4))
    else:
        print(obj)
    
    
def chunker(seq, size):
    """ for a given sequence, splits into even + residual chunks.  returns an iterator 
    see: https://stackoverflow.com/a/434328
    using this to page the queries as paging is not yet implemented in the API
    """
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

    
def make_request(endpoint, params):
    ''' wrapper to build and make a request '''
    requestUrl = REQUEST_URI + "/" + endpoint 
    if params is not None:
        requestUrl += '?' + urlencode(params)

    try:
        response = requests.get(requestUrl)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        print("HTTP Error: " + err.args[0])
        raise requests.exceptions.HTTPError
        

def read_variants():
    with open(args.file) as fh:
        variants = fh.read().splitlines() 
        hasChr = True if 'chr' in variants[3] else False
        variants = [ v.replace('chr', '').replace('MT', 'M') for v in variants ]
        if variants[0].lower() in ['id', 'variant']:
            variants.pop(0)
    return tuple(variants), hasChr


def lookup(ids):
    """ loookup a list of variants by ID"""
    return make_request("genomics/variant/", {"id": ','.join(ids), "full": args.full})


def run():
    chunks = chunker(variants, args.pageSize)
    with Pool() as pool:
        response = pool.map(lookup, chunks)
        return sum(response, []) # concatenates the individual responses


def extract_associations(annotation):
    associations = [ key + '=' + str(value['p_value'])
                        for key, value in annotation['associations'].items()]
    return [';'.join(associations), len(associations)]
        

def extract_most_severe_consequence(annotation):
    fields = ['biotype', 'consequence_is_coding', 'impact', 'gene_id', 'gene_symbol', 'protein_id']
    conseqAnnotations = annotation['most_severe_consequence']
    conseq = ','.join(conseqAnnotations['consequence_terms'])
    qualifiers = [ key + '=' + str(value) 
                    for key, value in conseqAnnotations.items() if key in fields]
    
    return [conseq, ';'.join(qualifiers)]
# CADD
# def extract_allele_frequencies(annotation)
        

def print_table(resultJson, reqChr):
    ''' 
    id
    ref_snp_id
    associations (sum stats), one column per dataset
    is_adsp_variant
    1000 genomes allele frequencies
    MSC
    regulatory consequences
    '''
    header = ['queried_variant', 'mapped_variant', 'ref_snp_id', 'is_adsp_variant',
              'associations', 'num_associations']
    
    for vJson in resultJson:
        variant = SimpleNamespace(**vJson)
        values = ['chr' + variant.queried_variant if reqChr else variant.queried_variant,
                  variant.metaseq_id, variant.ref_snp_id, variant.is_adsp_variant] \
                  + extract_associations(variant.annotation) \
                  + extract_most_severe_consequence(variant.annotation)  
        print(values)
        exit()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Look up a list of variants and retrieve annotation")
    parser.add_argument('--file', required=True,
                        help="new line separated list of variants, can be refSnpID or chr:pos:ref:alt")
    parser.add_argument('--format', default="json", choices=['tab', 'json'], 
                        help="output file format")
    parser.add_argument('--pageSize', default=500, choices = [50, 200, 300, 400, 500], type=int)
    parser.add_argument('--full', help="retrieve full annotation", action="store_true")
    args = parser.parse_args()
    
    
    [variants, removeChr] = read_variants()
  
    print("Looking up", str(len(variants)), "variants.", file=stderr)

    result = run()
    if args.format == 'json':
        pretty_print(result)
    else:
        print_table(result, removeChr)