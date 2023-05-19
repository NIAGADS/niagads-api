from flask import Blueprint, request

variant_bp = Blueprint('variant', __name__, url_prefix='/variant')

@variant_bp.route('/', methods=['GET'])
def lookup():
    return {'message': "SUCCESS: You've looked up a variant"}

