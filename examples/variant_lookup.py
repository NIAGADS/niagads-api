import requests
import argparse
import json
from sys import stderr
from urllib.parse import urlencode
from multiprocessing import Process

REQUEST_URI = "https://api.niagads.org"

def pretty_print(obj):
    ''' pretty print a dict obj'''
    if isinstance(obj, dict):
        print(json.dumps(obj, sort_keys=True, indent=4))
    else:
        print(obj)
    
    
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
        

def read_variants():
    with open(args.file) as fh:
        variants = fh.read().splitlines() 
    return variants


def lookup_variants():
    # p = Process(target=bubble_sort, args=([1,9,4,5,2,6,8,4],))
    1 
    
if __name__ == "main":
    parser = argparse.ArgumentParser(description="Look up a list of variants and retrieve annotation")
    parser.add_argument('--file', required=True,
                        help="new line separated list of variants, can be refSnpID or chr:pos:ref:alt")
    parser.add_argument('--format', default="json", choices=['tab', 'json'], 
                        help="output file format")
    args = parser.parse_args()
    
    variants = read_variants()
    print("Looking up", str(len(variants)), "variants", file=stderr)