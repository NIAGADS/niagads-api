from flask import Blueprint, request
from blueprints.genomics.entities import dataset_bp, variant_bp

genomics_bp = Blueprint('genomics', __name__, url_prefix='/genomics')

# register child blueprints
genomics_bp.register_blueprint(dataset_bp)
genomics_bp.register_blueprint(variant_bp)

@genomics_bp.route('/')
def hello():
    return {'message': "SUCCESS: You've reached the the Genomics API -- link to documentation"}

