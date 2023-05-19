''' api to retrieve all tracks associated with a dataset '''

from flask_restx import Namespace, Resource, fields
from schemas.datasets.metadata import base as metadata, genomicsdb as genomicsdb_metadata

api = Namespace(
    'genomics/dataset', description="Retrieve dataset (set of one or more tracks from the NIAGADS repository; a NIAGADS accession) metadata and track listing")

# create response schema from the base metadata schema
metadata_model = api.model('Dataset', metadata)
# extend w/GenomicsDB - only fields
genomicsdb_metadata_model = api.clone('GenomicsDBDataset', metadata_model, genomicsdb_metadata)


@api.route('/<id>', doc={"description": "Get meta-data for specified dataset"})
class Genomics(Resource):
    @api.marshal_with(genomicsdb_metadata_model, envelope="dataset")
    @api.doc(params={'id': 'unique dataset identifier or accession number in original datasource'})
    def get(self, id):
        return {"id": id}

