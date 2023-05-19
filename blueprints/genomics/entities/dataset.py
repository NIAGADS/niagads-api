from flask import Blueprint, request

dataset_bp = Blueprint('dataset', __name__, url_prefix='/dataset')

@dataset_bp.route('/', methods=['GET'])
def lookup():
    return {'message': "SUCCESS: You've looked up a dataset"}

