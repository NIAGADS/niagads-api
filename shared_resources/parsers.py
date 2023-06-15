""" common parsers """
from flask_restx import reqparse 
from types import SimpleNamespace
from shared_resources.fields import Span

CHROMOSOMES = range(1,22) + ['X', 'Y', 'N']

_parsers = {}

_parsers['id'] = reqparse.RequestParser()
_parsers['id'].add_argument('id', help="comma separated list of one or more identifiers", required=True)

_parsers['id_enum'] = _parsers['id'].copy()
_parsers['id_enum'].replace_argument('id', action='split', help="comma separated list of one or more identifiers", required=True)

_parsers['span'] = reqparse.RequestParser(help="", )
_parsers['span'].add_argument('span', type=Span, help="a genomic span in the format chrN:start-end, where N is one of 1..22,X,Y,M")
_parsers['span'].add_argument('chr', help="chromosome, in the format chrN or N, where N is one of 1..22,X,Y,M", choices=CHROMOSOMES)
_parsers['span'].add_argument('start', type=int, help="start location for the interval of interest")
_parsers['span'].add_argument('end', type=int, help="start location for the interval of interest")

_parsers['track'] = _parsers['span'].copy()


# for inheritence, use parser.copy(), .replace_argument, .remove_argument, see 
# https://flask-restx.readthedocs.io/en/latest/parsing.html#parser-inheritance


parser = SimpleNamespace(**_parsers)