""" common parsers """
from flask_restx import reqparse 
from types import SimpleNamespace

from shared_resources.fields import Span, GenomeBuild
from shared_resources.constants import CHROMOSOMES, DATASET_TYPES, GENOME_BUILDS

def merge_parsers(parser1, parser2):
    """ merge two parsers """
    newParser = parser1.copy()
    newParser.args = newParser.args + parser2.args
    return newParser

_parsers = {}

_parsers['genome_build'] = reqparse.RequestParser()
_parsers['genome_build'].add_argument('assembly', help="reference genome build",
        default="GRCh38", choices=GENOME_BUILDS)

_parsers['id'] = reqparse.RequestParser()
_parsers['id'].add_argument('id', help="comma separated list of one or more identifiers", required=True)

_parsers['id_enum'] = _parsers['id'].copy()
_parsers['id_enum'].replace_argument('id', action='split', help="comma separated list of one or more identifiers", required=True)

_parsers['span'] = reqparse.RequestParser()
_parsers['span'].add_argument('span', type=Span, help="a genomic span in the format chrN:start-end, where N is one of 1..22,X,Y,M")
_parsers['span'].add_argument('chr', help="chromosome, in the format chrN or N, where N is one of 1..22,X,Y,M", choices=CHROMOSOMES)
_parsers['span'].add_argument('start', type=int, help="start location for the interval of interest")
_parsers['span'].add_argument('end', type=int, help="start location for the interval of interest")

_parsers['track'] = _parsers['span'].copy()

_parsers['filters'] = reqparse.RequestParser()
_parsers['filters'].add_argument('type', help="type of dataset or track; what kind of information")

_parsers['extended_filters'] = _parsers['filters'].copy()
_parsers['extended_filters'].add_argument('source', help="original source of the data; e.g., NIAGADS, ENCODE, FANTOM5")
_parsers['extended_filters'].add_argument('assay', help="assay type")



# for inheritence, use parsers.copy(), .replace_argument, .remove_argument, see 
# https://flask-restx.readthedocs.io/en/latest/parsing.html#parser-inheritance


parsers = SimpleNamespace(**_parsers)