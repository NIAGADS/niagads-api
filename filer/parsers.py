import logging
from urllib.parse import unquote
from flask_restx import reqparse 
from types import SimpleNamespace

from shared_resources import constants
from shared_resources.parsers import arg_parsers
from filer.utils import make_request

logger = logging.getLogger(__name__)

filter_arg_parser = reqparse.RequestParser()
for name, description in constants.ALLOWABLE_FILER_TRACK_FILTERS.items():
    filter_arg_parser.add_argument(name, help=description)

